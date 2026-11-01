import numpy as np
import numpy as np
import matplotlib.pyplot as plt
# 1. FUNGSI KEANGGOTAAN
def bahu_kiri(v, a, b):
    """Bahu kiri : 1 sampai a, turun linear ke 0 di b."""
    if v <= a: return 1.0
    if v >= b: return 0.0
    return (b - v) / (b - a)
 
def segitiga(v, a, b, c):
    """Segitiga : 0 di a, puncak 1 di b, 0 di c (boleh tidak simetris)."""
    if v <= a or v >= c: return 0.0
    if v <= b: return (v - a) / (b - a)
    return (c - v) / (c - b)
 
def bahu_kanan(v, a, b):
    """Bahu kanan : 0 sampai a, naik linear ke 1 di b."""
    if v <= a: return 0.0
    if v >= b: return 1.0
    return (v - a) / (b - a)
 
def fuzzifikasi_permintaan(x):
    return {"Sedikit": bahu_kiri(x, 120, 142),
            "Sedang":  segitiga(x, 120, 142, 164),
            "Banyak":  bahu_kanan(x, 142, 164)}
 
def fuzzifikasi_persediaan(y):
    
    return {"Sedikit": bahu_kiri(y, 69, 79),
            "Sedang":  segitiga(y, 69, 79, 88),
            "Banyak":  bahu_kanan(y, 79, 88)}
 
# 2. BASIS ATURAN (Tabel 5 jurnal)
# (Permintaan, Persediaan) -> Produksi
ATURAN = [
    ("Sedikit", "Sedikit", "Sedikit"),   # R1
    ("Sedikit", "Sedang",  "Sedikit"),   # R2
    ("Sedikit", "Banyak",  "Sedikit"),   # R3
    ("Sedang",  "Sedikit", "Banyak"),    # R4
    ("Sedang",  "Sedang",  "Sedang"),    # R5
    ("Sedang",  "Banyak",  "Sedang"),    # R6
    ("Banyak",  "Sedikit", "Banyak"),    # R7
    ("Banyak",  "Sedang",  "Banyak"),    # R8
    ("Banyak",  "Banyak",  "Banyak"),    # R9
]
 
def kekuatan_aturan(x, y):
    """Fire strength (alpha-predikat) tiap aturan memakai operator AND = min."""
    mx, my = fuzzifikasi_permintaan(x), fuzzifikasi_persediaan(y)
    return [min(mx[a], my[b]) for a, b, _ in ATURAN]
 
# 3. SUGENO ORDE 0
# Konsekuen = konstanta (singleton), diambil titik tengah rentang himpunan output jurnal
KONSTANTA_SUGENO = {"Sedikit": 203.0, "Sedang": 226.0, "Banyak": 248.5}
 
def sugeno_orde0(x, y):
    alpha = kekuatan_aturan(x, y)
    zi = [KONSTANTA_SUGENO[c] for _, _, c in ATURAN]
    pembagi = sum(alpha)
    return sum(a * z for a, z in zip(alpha, zi)) / pembagi if pembagi else float("nan")
 
# 4. TSUKAMOTO
# Konsekuen WAJIB monoton. Invers fungsi keanggotaan: z = f^-1(alpha)
def z_tsukamoto(label, alpha):
    if label == "Sedikit":   # monoton TURUN : mu=1 di z=214, mu=0 di z=237
        return 237.0 - alpha * (237.0 - 214.0)
    if label == "Sedang":    # monoton NAIK  : mu=0 di z=214, mu=1 di z=237 (lengan kiri segitiga)
        return 214.0 + alpha * (237.0 - 214.0)
    if label == "Banyak":    # monoton NAIK  : mu=0 di z=237, mu=1 di z=259
        return 237.0 + alpha * (259.0 - 237.0)
    raise ValueError(label)
 
def tsukamoto(x, y):
    alpha = kekuatan_aturan(x, y)
    zi = [z_tsukamoto(c, a) for (_, _, c), a in zip(ATURAN, alpha)]
    pembagi = sum(alpha)
    return sum(a * z for a, z in zip(alpha, zi)) / pembagi if pembagi else float("nan")
 
# 5. MAMDANI (pembanding, centroid numerik)
def mamdani_centroid(x, y, n=2001):
    alpha = kekuatan_aturan(x, y)
    z = np.linspace(192, 259, n)
    mu = {"Sedikit": np.array([bahu_kiri(v, 214, 237) for v in z]),
          "Sedang":  np.array([segitiga(v, 214, 237, 259) for v in z]),
          "Banyak":  np.array([bahu_kanan(v, 237, 259) for v in z])}
    agregat = np.zeros_like(z)
    for (_, _, c), a in zip(ATURAN, alpha):
        agregat = np.maximum(agregat, np.minimum(a, mu[c]))   # implikasi min, agregasi max
    return float((z * agregat).sum() / agregat.sum())
 
# 6. DATA UJI
# (x, y, aktual jurnal, Mamdani jurnal)  -> Data 5 tidak ada di jurnal (None)
DATA_UJI = [
    (141, 71, 234, 242),   # Data 1 : 02-06-18
    (122, 66, 214, 211),   # Data 2 : 04-06-18
    (126, 68, 211, 216),   # Data 3 : 30-08-18
    (161, 61, 248, 252),   # Data 4 : 31-08-18
    (100, 85, None, None), # Data 5 : skenario ekstrem (permintaan rendah, stok tinggi)
]
 
def cetak_detail(x, y):
    mx, my = fuzzifikasi_permintaan(x), fuzzifikasi_persediaan(y)
    print(f"  Permintaan {x}: " + ", ".join(f"{k}={v:.4f}" for k, v in mx.items()))
    print(f"  Persediaan {y}: " + ", ".join(f"{k}={v:.4f}" for k, v in my.items()))
    for i, (a, (p, q, c)) in enumerate(zip(kekuatan_aturan(x, y), ATURAN), 1):
        if a > 0:
            print(f"    R{i}: {p}-{q} -> {c:<7} alpha={a:.4f} | "
                  f"Sugeno z={KONSTANTA_SUGENO[c]:.1f} | Tsukamoto z={z_tsukamoto(c, a):.3f}")
# 7. GRAFIK 
WARNA = {"Sedikit": "tab:red", "Sedang": "tab:blue", "Banyak": "tab:green"}

def grafik_keanggotaan():
    """Gambar 1: fungsi keanggotaan input Permintaan dan Persediaan."""
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    xs, ys = np.linspace(99, 164, 400), np.linspace(60, 88, 400)
    for k, w in WARNA.items():
        ax[0].plot(xs, [fuzzifikasi_permintaan(v)[k] for v in xs], w, label=k)
        ax[1].plot(ys, [fuzzifikasi_persediaan(v)[k] for v in ys], w, label=k)
    ax[0].set_title("Permintaan (x)"); ax[0].set_xlabel("pack"); ax[0].set_ylabel("derajat keanggotaan")
    ax[1].set_title("Persediaan (y)"); ax[1].set_xlabel("pack")
    ax[0].legend(); ax[1].legend()
    fig.tight_layout(); fig.savefig("grafik_1_keanggotaan_input.png", dpi=170)

def grafik_konsekuen():
    """Gambar 2: output Mamdani (jurnal) vs konsekuen monoton Tsukamoto."""
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    zs = np.linspace(192, 259, 400)
    ax[0].plot(zs, [bahu_kiri(v, 214, 237) for v in zs], "tab:red", label="Sedikit (turun)")
    ax[0].plot(zs, [segitiga(v, 214, 237, 259) for v in zs], "tab:blue", label="Sedang (segitiga)")
    ax[0].plot(zs, [bahu_kanan(v, 237, 259) for v in zs], "tab:green", label="Banyak (naik)")
    ax[0].set_title("Output Mamdani/jurnal")
    ax[1].plot([214, 237], [1, 0], "tab:red", label="Sedikit (turun)")
    ax[1].plot([214, 237], [0, 1], "tab:blue", label="Sedang (lengan naik)")
    ax[1].plot([237, 259], [0, 1], "tab:green", label="Banyak (naik)")
    ax[1].set_title("Konsekuen Tsukamoto (monoton)")
    for a in ax:
        a.set_xlabel("produksi (pack)"); a.legend(fontsize=8)
    fig.tight_layout(); fig.savefig("grafik_2_konsekuen.png", dpi=170)

def grafik_perbandingan():
    """Gambar 3: perbandingan hasil kelima data uji."""
    n = len(DATA_UJI)
    aktual = [d[2] if d[2] else np.nan for d in DATA_UJI]
    mam = [mamdani_centroid(x, y) for x, y, _, _ in DATA_UJI]
    sug = [sugeno_orde0(x, y) for x, y, _, _ in DATA_UJI]
    tsu = [tsukamoto(x, y) for x, y, _, _ in DATA_UJI]
    i, w = np.arange(n), 0.2
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.bar(i - 1.5 * w, aktual, w, label="Aktual jurnal", color="#999999")
    ax.bar(i - 0.5 * w, mam, w, label="Mamdani (hitung)", color="tab:purple")
    ax.bar(i + 0.5 * w, sug, w, label="Sugeno Orde 0", color="tab:blue")
    ax.bar(i + 1.5 * w, tsu, w, label="Tsukamoto", color="tab:orange")
    ax.set_xticks(i); ax.set_xticklabels([f"D{k}" for k in range(1, n + 1)])
    ax.set_ylim(180, 260); ax.set_ylabel("produksi (pack)")
    ax.legend(ncol=4, fontsize=8, loc="upper left")
    fig.tight_layout(); fig.savefig("grafik_3_perbandingan.png", dpi=170)

def tampilkan_grafik():
    """Simpan ketiga grafik sebagai PNG lalu tampilkan di layar."""
    grafik_keanggotaan(); grafik_konsekuen(); grafik_perbandingan()
    print("\nGrafik disimpan: grafik_1_keanggotaan_input.png, "
          "grafik_2_konsekuen.png, grafik_3_perbandingan.png")
    plt.show()
def main():
    print("=" * 96)
    print("DETAIL FUZZIFIKASI DAN ATURAN AKTIF")
    print("=" * 96)
    for i, (x, y, _, _) in enumerate(DATA_UJI, 1):
        print(f"Data {i} (x={x}, y={y})")
        cetak_detail(x, y)
 
    print("\n" + "=" * 96)
    print("TABEL PERBANDINGAN HASIL PRODUKSI ROTI (pack)")
    print("=" * 96)
    kepala = (f"{'Data':<5}{'x':>5}{'y':>5}{'Aktual':>8}{'Mamdani':>9}{'Mamdani':>9}"
              f"{'Sugeno0':>9}{'Tsukamoto':>10}{'|S0-T|':>8}")
    print(kepala)
    print(f"{'':<5}{'':>5}{'':>5}{'':>8}{'(jurnal)':>9}{'(hitung)':>9}{'':>9}{'':>10}{'':>8}")
    print("-" * 96)
    for i, (x, y, akt, mj) in enumerate(DATA_UJI, 1):
        s0, ts, mh = sugeno_orde0(x, y), tsukamoto(x, y), mamdani_centroid(x, y)
        print(f"{i:<5}{x:>5}{y:>5}{(akt if akt else '-'):>8}{(mj if mj else '-'):>9}"
              f"{mh:>9.2f}{s0:>9.2f}{ts:>10.2f}{abs(s0 - ts):>8.2f}")
 
    print("\n" + "=" * 96)
    print("GALAT TERHADAP DATA AKTUAL JURNAL (Data 1-4) -- AE dan APE")
    print("=" * 96)
    print(f"{'Data':<5}{'Aktual':>8}{'Mam.jrnl':>10}{'Sugeno0':>10}{'Tsukamoto':>11}"
          f"{'APE Mam':>9}{'APE S0':>9}{'APE Ts':>9}")
    ape = {"mam": [], "s0": [], "ts": []}
    for i, (x, y, akt, mj) in enumerate(DATA_UJI, 1):
        if akt is None:
            continue
        s0, ts = sugeno_orde0(x, y), tsukamoto(x, y)
        a_m, a_s, a_t = (abs(akt - v) / akt * 100 for v in (mj, s0, ts))
        ape["mam"].append(a_m); ape["s0"].append(a_s); ape["ts"].append(a_t)
        print(f"{i:<5}{akt:>8}{mj:>10}{s0:>10.2f}{ts:>11.2f}{a_m:>8.2f}%{a_s:>8.2f}%{a_t:>8.2f}%")
    print("-" * 96)
    print(f"MAPE  Mamdani (jurnal) = {np.mean(ape['mam']):.2f}% | "
          f"Sugeno Orde 0 = {np.mean(ape['s0']):.2f}% | Tsukamoto = {np.mean(ape['ts']):.2f}%")
    print(f"MAPE  Mamdani (jurnal) = {np.mean(ape['mam']):.2f}% | "
          f"Sugeno Orde 0 = {np.mean(ape['s0']):.2f}% | Tsukamoto = {np.mean(ape['ts']):.2f}%")
    tampilkan_grafik() 
if __name__ == "__main__":
    main()