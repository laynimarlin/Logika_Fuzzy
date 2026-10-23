import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
 
 
# ==========================================================
# 1. FUNGSI KEANGGOTAAN SEGITIGA (mendukung bahu a == b / b == c)
# ==========================================================
def trimf(x, params):
    a, b, c = params
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    # sisi naik
    if b != a:
        idx = (x > a) & (x < b)
        y[idx] = (x[idx] - a) / (b - a)
    # sisi turun
    if c != b:
        idx = (x > b) & (x < c)
        y[idx] = (c - x[idx]) / (c - b)
    y[x == b] = 1.0
    return np.clip(y, 0.0, 1.0)
 
 
# ==========================================================
# 2. KELAS FUZZY INFERENCE SYSTEM
# ==========================================================
class FuzzyInferenceSystem:
    def __init__(self, implication="min", fallback=None):
        """
        implication: 'min' (clipping) atau 'prod' (scaling)
        fallback   : nilai crisp jika tidak ada aturan aktif
                     (default: titik tengah semesta output)
        """
        self.inputs = {}      # nama -> (universe, {label: params})
        self.output = None    # (nama, universe, {label: params})
        self.rules = []       # list (antecedent_dict, consequent_label, operator)
        self.implication = implication
        self.fallback = fallback
        self.last = {}        # menyimpan hasil terakhir untuk visualisasi
 
    def add_input_variable(self, name, universe, mf_dict):
        self.inputs[name] = (np.asarray(universe), mf_dict)
 
    def set_output_variable(self, name, universe, mf_dict):
        self.output = (name, np.asarray(universe), mf_dict)
 
    def add_rule(self, rule_tuple):
        """rule_tuple = ({'permintaan': 'Rendah', 'stok': 'Sedikit'}, 'Sedang')
        atau dengan operator ketiga: (..., ..., 'OR')"""
        antecedent, consequent = rule_tuple[0], rule_tuple[1]
        op = rule_tuple[2].upper() if len(rule_tuple) > 2 else "AND"
        self.rules.append((antecedent, consequent, op))
 
    # ---- Tahap 1: Fuzzifikasi ----
    def fuzzify(self, input_values):
        deg = {}
        for var, (_, mfs) in self.inputs.items():
            x = float(input_values[var])
            deg[var] = {lbl: float(trimf(np.array([x]), p)[0]) for lbl, p in mfs.items()}
        return deg
 
    # ---- Tahap 2: Evaluasi aturan, implikasi, agregasi ----
    def compute(self, input_values):
        deg = self.fuzzify(input_values)
        out_name, z, out_mfs = self.output
 
        alphas = []
        agregasi = np.zeros_like(z, dtype=float)
        implikasi = []
        for ant, cons, op in self.rules:
            vals = [deg[v][l] for v, l in ant.items()]
            alpha = min(vals) if op == "AND" else max(vals)
            alphas.append(alpha)
            mf = trimf(z, out_mfs[cons])
            if self.implication == "min":
                imp = np.minimum(alpha, mf)
            else:
                imp = alpha * mf
            implikasi.append(imp)
            agregasi = np.maximum(agregasi, imp)
 
        # ---- Tahap 4: Defuzzifikasi Centroid ----
        total = np.sum(agregasi)
        if total == 0:
            crisp = self.fallback if self.fallback is not None else float((z[0] + z[-1]) / 2)
        else:
            crisp = float(np.sum(z * agregasi) / total)
 
        self.last = dict(deg=deg, alphas=alphas, implikasi=implikasi,
                         agregasi=agregasi, crisp=crisp)
        return crisp
 
 
# ==========================================================
# 3. KNOWLEDGE BASE: SISTEM PENENTUAN PRODUKSI ROTI
# ==========================================================
def bangun_fis(implication="min"):
    fis = FuzzyInferenceSystem(implication=implication)
 
    u_perm = np.linspace(0, 200, 401)   # permintaan (roti/hari)
    u_stok = np.linspace(0, 100, 201)   # stok (roti)
    u_prod = np.linspace(0, 200, 401)   # produksi (roti)
 
    fis.add_input_variable("permintaan", u_perm, {
        "Rendah": [0, 0, 100], "Sedang": [50, 100, 150], "Tinggi": [100, 200, 200]})
    fis.add_input_variable("stok", u_stok, {
        "Sedikit": [0, 0, 50], "Sedang": [25, 50, 75], "Banyak": [50, 100, 100]})
    fis.set_output_variable("produksi", u_prod, {
        "Sedikit": [0, 0, 100], "Sedang": [50, 100, 150], "Banyak": [100, 200, 200]})
 
    tabel = [
        ("Rendah", "Sedikit", "Sedang"), ("Rendah", "Sedang", "Sedikit"), ("Rendah", "Banyak", "Sedikit"),
        ("Sedang", "Sedikit", "Banyak"), ("Sedang", "Sedang", "Sedang"), ("Sedang", "Banyak", "Sedikit"),
        ("Tinggi", "Sedikit", "Banyak"), ("Tinggi", "Sedang", "Banyak"), ("Tinggi", "Banyak", "Sedang"),
    ]
    for p, s, o in tabel:
        fis.add_rule(({"permintaan": p, "stok": s}, o))
    return fis
 
 
# ==========================================================
# 4. PENGUJIAN 3 KASUS
# ==========================================================
kasus = [
    ("Kasus 1", {"permintaan": 40,  "stok": 70}),
    ("Kasus 2", {"permintaan": 80,  "stok": 40}),
    ("Kasus 3", {"permintaan": 140, "stok": 30}),
]
 
if __name__ == "__main__":
    fis_min = bangun_fis("min")
    fis_prod = bangun_fis("prod")
 
    print("=" * 70)
    print("HASIL PENGUJIAN FIS - PRODUKSI ROTI")
    print("=" * 70)
    hasil = []
    for nama, inp in kasus:
        z_min = fis_min.compute(inp)
        snap = fis_min.last
        z_prod = fis_prod.compute(inp)
        hasil.append((nama, inp, snap, z_min, z_prod))
        print(f"\n{nama}: permintaan = {inp['permintaan']}, stok = {inp['stok']}")
        print("  Fuzzifikasi:", {v: {l: round(d, 2) for l, d in dd.items()} for v, dd in snap["deg"].items()})
        aktif = [(i + 1, round(a, 2)) for i, a in enumerate(snap["alphas"]) if a > 0]
        print("  Aturan aktif (R, alpha):", aktif)
        print(f"  Produksi (Min/Clipping)    = {z_min:.2f} roti")
        print(f"  Produksi (Product/Scaling) = {z_prod:.2f} roti")
 
    # Visualisasi: 3 kasus
    z = fis_min.output[1]
    out_mfs = fis_min.output[2]
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.6), sharey=True)
    for ax, (nama, inp, snap, z_min, _) in zip(axes, hasil):
        for lbl, col in zip(["Sedikit", "Sedang", "Banyak"], ["g", "b", "r"]):
            ax.plot(z, trimf(z, out_mfs[lbl]), col + "--", alpha=0.5, label=f"MF {lbl}")
        ax.fill_between(z, 0, snap["agregasi"], color="purple", alpha=0.35, label="Daerah Agregasi")
        ax.plot(z, snap["agregasi"], color="purple", linewidth=2)
        ax.axvline(z_min, color="black", linewidth=2, label=f"Centroid = {z_min:.1f}")
        ax.set_title(f"{nama}\nPermintaan={inp['permintaan']}, Stok={inp['stok']}", fontsize=10)
        ax.set_xlabel("Jumlah Produksi (roti)")
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(loc="upper center", fontsize=7)
    axes[0].set_ylabel("Derajat Keanggotaan μ(z)")
    plt.tight_layout()
    plt.savefig("grafik_agregasi_fis_roti.png", dpi=200)
 
    # Visualisasi: perbandingan Min vs Product (Kasus 2)
    inp = kasus[1][1]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, fis, ttl in zip(axes, [fis_min, fis_prod], ["Implikasi Clipping (Min)", "Implikasi Scaling (Product)"]):
        c = fis.compute(inp)
        s = fis.last
        ax.fill_between(z, 0, s["agregasi"], color="orange", alpha=0.4)
        ax.plot(z, s["agregasi"], color="darkorange", linewidth=2)
        ax.axvline(c, color="black", linewidth=2, label=f"Centroid = {c:.1f}")
        ax.set_title(f"{ttl} - Kasus 2", fontsize=10)
        ax.set_xlabel("Jumlah Produksi (roti)")
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(fontsize=8)
    axes[0].set_ylabel("μ(z)")
    plt.tight_layout()
    plt.savefig("grafik_min_vs_product.png", dpi=200)
 
    # Uji fallback
    f = bangun_fis("min")
    # input di luar domain -> semua alpha = 0 -> fallback
    print("\nUji fallback (input di luar domain, permintaan=500, stok=500):",
          f.compute({"permintaan": 500, "stok": 500}))
