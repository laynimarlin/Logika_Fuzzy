import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Kompatibilitas fungsi integrasi
if hasattr(np, 'trapezoid') and not hasattr(np, 'trapz'):
    np.trapz = np.trapezoid


class FuzzyDecisionSystem:
    """Sistem Inferensi Fuzzy Tipe Mamdani"""

    def __init__(self):
        self.input_vars = {}
        self.output_var = None
        self.rules = []

    def tambah_input(self, nama, semesta):
        self.input_vars[nama] = {'universe': semesta}

    def tetapkan_output(self, nama, semesta):
        self.output_var = {'name': nama, 'universe': semesta}

    def tambah_aturan(self, anteseden, konsekuen):
        self.rules.append((anteseden, konsekuen))

    # ============== FUNGSI KEANGGOTAAN ==============
    def _mu_permintaan(self, x, label):
        if label == 'Sedikit':
            if x <= 120: return 1.0
            elif 120 < x < 142: return (142 - x) / 22
            else: return 0.0
        elif label == 'Sedang':
            if x <= 120 or x >= 164: return 0.0
            elif 120 < x <= 142: return (x - 120) / 22
            elif 142 < x < 164: return (164 - x) / 22
        elif label == 'Banyak':
            if x <= 142: return 0.0
            elif 142 < x < 164: return (x - 142) / 22
            else: return 1.0
        return 0.0

    def _mu_persediaan(self, y, label):
        if label == 'Sedikit':
            if y <= 69: return 1.0
            elif 69 < y < 79: return (79 - y) / 10
            else: return 0.0
        elif label == 'Sedang':
            if y <= 69: return 0.0
            elif 69 < y <= 79: return (y - 69) / 10
            elif 79 < y < 88: return (88 - y) / 9
        elif label == 'Banyak':
            if y <= 79: return 0.0
            elif 79 < y < 88: return (y - 79) / 9
            else: return 1.0
        return 0.0

    def _mu_produksi(self, z, label):
        if label == 'Sedikit':
            if z <= 214: return 1.0
            elif 214 < z < 237: return (237 - z) / 23
            else: return 0.0
        elif label == 'Sedang':
            if z <= 214 or z >= 259: return 0.0
            elif 214 < z <= 237: return (z - 214) / 23
            elif 237 < z < 259: return (259 - z) / 22
        elif label == 'Banyak':
            if z <= 237: return 0.0
            elif 237 < z < 259: return (z - 237) / 22
            else: return 1.0
        return 0.0

    # ============== PROSES INFERENSI ==============
    def hitung(self, permintaan, persediaan):
        z_min, z_max = self.output_var['universe']
        z = np.linspace(z_min, z_max, 500)
        alpha_aturan = []

        # Fuzzifikasi & Firing Strength
        for antes, konsekuen in self.rules:
            mu_p = self._mu_permintaan(permintaan, antes['Permintaan'])
            mu_s = self._mu_persediaan(persediaan, antes['Persediaan'])
            alpha = min(mu_p, mu_s)
            alpha_aturan.append((alpha, konsekuen))

        # Implikasi (Clipping/Min) & Agregasi (Max)
        agregasi = np.zeros_like(z)
        for alpha, lbl in alpha_aturan:
            if alpha > 0:
                kurva = np.array([self._mu_produksi(zi, lbl) for zi in z])
                terpotong = np.minimum(alpha, kurva)
                agregasi = np.maximum(agregasi, terpotong)

        # Defuzzifikasi — Centroid + Fallback
        luas = np.trapz(agregasi, z)
        if luas < 1e-10:
            centroid = (z_min + z_max) / 2
        else:
            centroid = np.trapz(z * agregasi, z) / luas

        return centroid, alpha_aturan

    # ============== DECISION SURFACE 3D ==============
    def buat_permukaan_keputusan(self, nama_berkas='decision_surface.png'):
        p_min, p_max = self.input_vars['Permintaan']['universe']
        s_min, s_max = self.input_vars['Persediaan']['universe']

        kisi_p = np.linspace(p_min, p_max, 25)
        kisi_s = np.linspace(s_min, s_max, 25)
        P, S = np.meshgrid(kisi_p, kisi_s)
        Z = np.zeros_like(P)

        for i in range(P.shape[0]):
            for j in range(P.shape[1]):
                Z[i, j], _ = self.hitung(P[i, j], S[i, j])

        fig = plt.figure(figsize=(11, 7))
        ax = fig.add_subplot(111, projection='3d')
        permukaan = ax.plot_surface(P, S, Z, cmap='RdYlGn', edgecolor='none', alpha=0.9)
        ax.set_xlabel('Permintaan', fontsize=11, labelpad=8)
        ax.set_ylabel('Persediaan', fontsize=11, labelpad=8)
        ax.set_zlabel('Jumlah Produksi', fontsize=11, labelpad=8)
        ax.set_title('Permukaan Keputusan — Sistem Produksi Roti (Mamdani)',
                     fontweight='bold', fontsize=13, pad=20)
        fig.colorbar(permukaan, shrink=0.5, aspect=5, label='Jumlah Produksi')
        plt.tight_layout()
        plt.savefig(nama_berkas, dpi=300, bbox_inches='tight')
        print(f"Permukaan keputusan disimpan: {nama_berkas}")
        plt.show()


# ==============================================================
# BANGUN SISTEM
# ==============================================================
def bangun_sistem():
    fis = FuzzyDecisionSystem()
    fis.tambah_input('Permintaan', [99, 164])
    fis.tambah_input('Persediaan', [60, 88])
    fis.tetapkan_output('Produksi', [192, 259])

    # 9 Aturan Penuh
    fis.tambah_aturan({'Permintaan':'Sedikit', 'Persediaan':'Sedikit'}, 'Sedikit')
    fis.tambah_aturan({'Permintaan':'Sedikit', 'Persediaan':'Sedang'},  'Sedikit')
    fis.tambah_aturan({'Permintaan':'Sedikit', 'Persediaan':'Banyak'},  'Sedikit')
    fis.tambah_aturan({'Permintaan':'Sedang',  'Persediaan':'Sedikit'}, 'Banyak')
    fis.tambah_aturan({'Permintaan':'Sedang',  'Persediaan':'Sedang'},  'Sedang')
    fis.tambah_aturan({'Permintaan':'Sedang',  'Persediaan':'Banyak'},  'Sedang')
    fis.tambah_aturan({'Permintaan':'Banyak',  'Persediaan':'Sedikit'}, 'Banyak')
    fis.tambah_aturan({'Permintaan':'Banyak',  'Persediaan':'Sedang'},  'Banyak')
    fis.tambah_aturan({'Permintaan':'Banyak',  'Persediaan':'Banyak'},  'Banyak')

    return fis


# ==============================================================
# EKSEKUSI & PENGUJIAN
# ==============================================================
if __name__ == "__main__":
    fis = bangun_sistem()

    print("="*70)
    print("ASESMEN MODUL 2 — PRAKTIKUM 10")
    print("Sistem Penentuan Jumlah Produksi Roti — Mamdani")
    print("="*70)

    # 5 Skenario Pengujian
    skenario = [
        ("1 — Data Utama (02-06-18)", 141, 71, 234),
        ("2 — Permintaan Rendah",     122, 66, 214),
        ("3 — Permintaan Tinggi",     161, 61, 248),
        ("4 — Persediaan Melimpah",   130, 85, 225),
        ("5 — Kondisi Rata-rata",     135, 74, 230),
    ]

    hasil = []
    for nama, p, s, aktual in skenario:
        prod, aturan = fis.hitung(p, s)
        galat = abs(aktual - prod) / aktual * 100 if aktual != 0 else 0
        hasil.append([nama, p, s, aktual, round(prod, 2), round(galat, 4)])

        print(f"\n{nama}")
        print(f"  Permintaan = {p} | Persediaan = {s}")
        print(f"  Produksi Aktual = {aktual} | FIS Mamdani = {prod:.2f}")
        print(f"  Galat = {galat:.4f}%")
        print("  Firing Strength tiap aturan:")
        for i, (a, lbl) in enumerate(aturan, 1):
            if a > 0:
                print(f"    R{i}: α = {a:.4f} → Produksi {lbl}")

    # Tabel Ringkasan
    print("\nTABEL RINGKASAN HASIL PENGUJIAN")
    print(f"{'Skenario':<30} {'Permintaan':>10} {'Persediaan':>10} {'Aktual':>8} {'FIS':>10} {'Galat(%)':>10}")
    print("-"*70)
    for b in hasil:
        print(f"{b[0]:<30} {b[1]:>10} {b[2]:>10} {b[3]:>8} {b[4]:>10} {b[5]:>10}")

    # Visualisasi Permukaan Keputusan
    print("\nMembuat grafik permukaan keputusan...")
    fis.buat_permukaan_keputusan()