import numpy as np
np.trapz = np.trapezoid
import matplotlib.pyplot as plt

# --------------------------------------------------------------
# Kelas Modular: FuzzyInferenceSystem
# --------------------------------------------------------------
class FuzzyInferenceSystem:
    def __init__(self):
        self.input_vars = {}    # {nama: (semesta, dict_fungsi_keanggotaan)}
        self.output_var = None # (nama, semesta, dict_fungsi_keanggotaan)
        self.rules = []        # daftar aturan: (antecedent_dict, konsekuen_label)

    # Tambah variabel input
    def add_input_variable(self, name, universe, mf_dict):
        self.input_vars[name] = {
            'universe': universe,
            'mfs': mf_dict
        }

    # Tetapkan variabel output
    def set_output_variable(self, name, universe, mf_dict):
        self.output_var = {
            'name': name,
            'universe': universe,
            'mfs': mf_dict
        }

    # Tambah aturan: ({var_input: label}, konsekuen_output_label)
    def add_rule(self, rule_tuple):
        self.rules.append(rule_tuple)

    # === Fungsi Keanggotaan: Segitiga & Trapesium ===
    def _trimf(self, x, a, b, c):
        """Fungsi keanggotaan segitiga"""
        return np.maximum(0, np.minimum((x - a)/(b - a) if b != a else 1,
                                         (c - x)/(c - b) if c != b else 1))

    def _trapmf(self, x, a, b, c, d):
        """Fungsi keanggotaan trapesium"""
        return np.maximum(0, np.minimum(np.minimum((x-a)/(b-a) if b!=a else 1, 1),
                                        (d-x)/(d-c) if d!=c else 1))

    # Hitung derajat keanggotaan pada nilai tertentu
    def _get_membership(self, var_name, crisp_value, label):
        var_data = (self.input_vars.get(var_name) or
                    {'mfs': self.output_var['mfs']})
        mf = var_data['mfs'][label]
        x = np.array([crisp_value])
        if mf['type'] == 'trimf':
            return float(self._trimf(x, *mf['params'])[0])
        elif mf['type'] == 'trapmf':
            return float(self._trapmf(x, *mf['params'])[0])
        return 0.0

    # === Hitung FIS Lengkap ===
    def compute(self, input_values_dict):
        # ---- Langkah 1: Fuzzifikasi ----
        alpha_rules = []
        for antecedents, cons_label in self.rules:
            mu_values = []
            for var_name, lbl in antecedents.items():
                mu = self._get_membership(var_name, input_values_dict[var_name], lbl)
                mu_values.append(mu)
            alpha = min(mu_values)  # AND = min
            alpha_rules.append((alpha, cons_label))

        # ---- Langkah 2: Agregasi Output ----
        z_univ = self.output_var['universe']
        z_vals = np.linspace(z_univ[0], z_univ[1], 500)
        agg_mf = np.zeros_like(z_vals)

        for alpha, lbl in alpha_rules:
            if alpha > 0:
                mf = self.output_var['mfs'][lbl]
                if mf['type'] == 'trimf':
                    curve = self._trimf(z_vals, *mf['params'])
                else:
                    curve = self._trapmf(z_vals, *mf['params'])
                clipped = np.minimum(alpha, curve)
                agg_mf = np.maximum(agg_mf, clipped)

        # ---- Langkah 3: Defuzzifikasi — Centroid ----
        area = np.trapz(agg_mf, z_vals)
        if area < 1e-10:
            z_centroid = np.mean(z_univ)  # Fallback jika semua α = 0
        else:
            z_centroid = np.trapz(z_vals * agg_mf, z_vals) / area

        return {
            'z_values': z_vals,
            'aggregated_mf': agg_mf,
            'centroid': z_centroid,
            'alpha_rules': alpha_rules
        }

    # === Visualisasi Lengkap & Simpan Gambar ===
    def plot_system(self, input_dict, save_as='hasil_fis.png'):
        res = self.compute(input_dict)
        z_vals = res['z_values']
        agg_mf = res['aggregated_mf']
        cent = res['centroid']

        fig, axes = plt.subplots(2, 2, figsize=(14, 9))
        fig.suptitle('FIS Mamdani — Penentuan Jumlah Produksi Roti', fontsize=16)

        # Subplot 1: Permintaan
        ax = axes[0,0]
        ax.set_title('Variabel Input: Permintaan')
        x = np.linspace(99, 164, 200)
        for lbl, mf in self.input_vars['Permintaan']['mfs'].items():
            if mf['type'] == 'trimf':
                y = self._trimf(x, *mf['params'])
            else:
                y = self._trapmf(x, *mf['params'])
            ax.plot(x, y, label=lbl)
        ax.axvline(input_dict['Permintaan'], color='red', linestyle='--', label=f'Nilai: {input_dict["Permintaan"]}')
        ax.legend(); ax.grid(True); ax.set_ylim(0,1.05)

        # Subplot 2: Persediaan
        ax = axes[0,1]
        ax.set_title('Variabel Input: Persediaan')
        x = np.linspace(60, 88, 200)
        for lbl, mf in self.input_vars['Persediaan']['mfs'].items():
            if mf['type'] == 'trimf':
                y = self._trimf(x, *mf['params'])
            else:
                y = self._trapmf(x, *mf['params'])
            ax.plot(x, y, label=lbl)
        ax.axvline(input_dict['Persediaan'], color='red', linestyle='--', label=f'Nilai: {input_dict["Persediaan"]}')
        ax.legend(); ax.grid(True); ax.set_ylim(0,1.05)

        # Subplot 3: Output & Agregasi
        ax = axes[1,0]
        ax.set_title('Variabel Output: Produksi & Daerah Agregasi')
        for lbl, mf in self.output_var['mfs'].items():
            if mf['type'] == 'trimf':
                y = self._trimf(z_vals, *mf['params'])
            else:
                y = self._trapmf(z_vals, *mf['params'])
            ax.plot(z_vals, y, ':', label=lbl)
        ax.fill_between(z_vals, agg_mf, alpha=0.4, color='green', label='Agregasi')
        ax.axvline(cent, color='crimson', linewidth=2, label=f'Centroid = {cent:.2f}')
        ax.legend(); ax.grid(True); ax.set_ylim(0,1.05)

        # Subplot 4: Ringkasan Aturan Aktif
        ax = axes[1,1]
        ax.set_title('Nilai Firing Strength (α) Tiap Aturan')
        rule_nums = list(range(1, len(res['alpha_rules'])+1))
        alphas = [a for a, _ in res['alpha_rules']]
        colors = ['#2ecc71' if a>0 else '#bdc3c7' for a in alphas]
        bars = ax.bar(rule_nums, alphas, color=colors)
        ax.bar_label(bars, fmt='%.4f', fontsize=8)
        ax.set_xlabel('Nomor Aturan')
        ax.set_ylabel('α (Firing Strength)')
        ax.set_xticks(rule_nums)
        ax.grid(True, axis='y'); ax.set_ylim(0, 1.1)

        plt.tight_layout(rect=[0,0,1,0.96])
        plt.savefig(save_as, dpi=150, bbox_inches='tight')
        print(f"Gambar hasil disimpan sebagai: {save_as}")
        plt.show()
        return res


# ==============================================================
# 2. DEFINISI SISTEM — Studi Kasus Produksi Roti
# ==============================================================
def buat_sistem_produksi_roti():
    fis = FuzzyInferenceSystem()

    # ---- Variabel Input 1: Permintaan ----
    fis.add_input_variable('Permintaan', [99, 164], {
        'Sedikit':  {'type': 'trapmf', 'params': [0, 99, 120, 142]},
        'Sedang':   {'type': 'trimf',  'params': [120, 142, 164]},
        'Banyak':   {'type': 'trapmf', 'params': [142, 164, 200, 200]}
    })

    # ---- Variabel Input 2: Persediaan ----
    fis.add_input_variable('Persediaan', [60, 88], {
        'Sedikit':  {'type': 'trapmf', 'params': [0, 60, 69, 79]},
        'Sedang':   {'type': 'trimf',  'params': [69, 79, 88]},
        'Banyak':   {'type': 'trapmf', 'params': [79, 88, 100, 100]}
    })

    # ---- Variabel Output: Produksi ----
    fis.set_output_variable('Produksi', [192, 259], {
        'Sedikit':  {'type': 'trapmf', 'params': [0, 192, 214, 237]},
        'Sedang':   {'type': 'trimf',  'params': [214, 237, 259]},
        'Banyak':   {'type': 'trapmf', 'params': [237, 259, 300, 300]}
    })

    # ---- Basis Aturan (9 Aturan) ----
    fis.add_rule(({'Permintaan':'Sedikit', 'Persediaan':'Sedikit'}, 'Sedikit'))
    fis.add_rule(({'Permintaan':'Sedikit', 'Persediaan':'Sedang'},  'Sedikit'))
    fis.add_rule(({'Permintaan':'Sedikit', 'Persediaan':'Banyak'},  'Sedikit'))
    fis.add_rule(({'Permintaan':'Sedang',  'Persediaan':'Sedikit'}, 'Banyak'))
    fis.add_rule(({'Permintaan':'Sedang',  'Persediaan':'Sedang'},  'Sedang'))
    fis.add_rule(({'Permintaan':'Sedang',  'Persediaan':'Banyak'},  'Sedang'))
    fis.add_rule(({'Permintaan':'Banyak',  'Persediaan':'Sedikit'}, 'Banyak'))
    fis.add_rule(({'Permintaan':'Banyak',  'Persediaan':'Sedang'},  'Banyak'))
    fis.add_rule(({'Permintaan':'Banyak',  'Persediaan':'Banyak'},  'Banyak'))

    return fis


# ==============================================================
# 3. PENGUJIAN — 3 Skenario Input Berbeda
# ==============================================================
if __name__ == "__main__":
    fis = buat_sistem_produksi_roti()

    print("="*60)
    print("PENGUJIAN SISTEM FUZZY — Penentuan Jumlah Produksi Roti")
    print("="*60)

    skenario = [
        ("Skenario 1 — Data Utama Jurnal",    {'Permintaan':141, 'Persediaan':71}, 'hasil_skenario1.png'),
        ("Skenario 2 — Permintaan Rendah",     {'Permintaan':122, 'Persediaan':66}, 'hasil_skenario2.png'),
        ("Skenario 3 — Permintaan Tinggi",     {'Permintaan':161, 'Persediaan':61}, 'hasil_skenario3.png'),
    ]

    for nama, input_val, fname in skenario:
        print(f"\n▶ {nama}")
        print(f"   Input → Permintaan = {input_val['Permintaan']}, Persediaan = {input_val['Persediaan']}")
        hasil = fis.plot_system(input_val, save_as=fname)
        print(f"   Jumlah Produksi yang disarankan: {hasil['centroid']:.2f}")
        print("   Nilai α tiap aturan:")
        for i, (a, lbl) in enumerate(hasil['alpha_rules'], 1):
            print(f"      R{i}: α = {a:.4f} → Produksi {lbl}")
        print("-"*60)