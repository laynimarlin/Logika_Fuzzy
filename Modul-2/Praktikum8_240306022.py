import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# 1. Definisi semesta output produksi roti [190 - 260]
z = np.linspace(190, 260, 1000)

# 2. Fungsi keanggotaan variabel produksi (sesuai jurnal Sahulata et al., 2020)
mf_sedikit = fuzz.trapmf(z, [190, 190, 214, 237])
mf_sedang = fuzz.trimf(z, [214, 237, 259])
mf_banyak = fuzz.trapmf(z, [237, 259, 260, 260])

# 3. Nilai alpha-predikat hasil inferensi (sampel tanggal 02-06-18)
alpha_sedikit = 0.0455
alpha_sedang = 0.2000
alpha_banyak = 0.8000

# 4. Implikasi MIN dan agregasi MAX
imp_sedikit = np.fmin(alpha_sedikit, mf_sedikit)
imp_sedang = np.fmin(alpha_sedang, mf_sedang)
imp_banyak = np.fmin(alpha_banyak, mf_banyak)

agregasi = np.fmax(imp_sedikit, np.fmax(imp_sedang, imp_banyak))

# 5. Perhitungan 5 metode defuzzifikasi
metode = ["centroid", "bisector", "mom", "som", "lom"]
hasil = {}
for m in metode:
    hasil[m.upper()] = fuzz.defuzz(z, agregasi, m)

# 6. Menampilkan hasil di terminal
print("\nHASIL DEFUZZIFIKASI PRODUKSI ROTI (02-06-18)")
print("-" * 42)
print(f"{'Metode':<12} | {'Jumlah Produksi (Pcs)':>22}")
print("-" * 42)
for nama, nilai in hasil.items():
    print(f"{nama:<12} | {nilai:>22.2f}")
print("-" * 42)

# 7. Visualisasi Kurva Agregasi dan Titik Defuzzifikasi
plt.figure(figsize=(12, 6.5))
plt.plot(z, agregasi, 'b', linewidth=2.5, label='Kurva Agregasi Fuzzy')
plt.fill_between(z, 0, agregasi, color='skyblue', alpha=0.4)

warna = {
    "CENTROID": "red",
    "BISECTOR": "purple",
    "MOM": "black",
    "SOM": "green",
    "LOM": "orange"
}

for nama, nilai in hasil.items():
    plt.axvline(x=nilai, color=warna[nama], linestyle='--', linewidth=2,
                label=f'{nama} ({nilai:.2f})')
    tinggi = np.interp(nilai, z, agregasi)
    plt.scatter([nilai], [tinggi], color=warna[nama], s=60, zorder=6)

plt.title('Perbandingan 5 Metode Defuzzifikasi Penentuan Produksi Roti', fontsize=13, fontweight='bold')
plt.xlabel('Jumlah Produksi Roti (Pcs)', fontsize=11)
plt.ylabel('Derajat Keanggotaan μ(z)', fontsize=11)
plt.xlim(190, 260)
plt.ylim(-0.05, 1.05)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()
plt.savefig('produksi_roti_defuzzifikasi.png', dpi=300)
plt.show()