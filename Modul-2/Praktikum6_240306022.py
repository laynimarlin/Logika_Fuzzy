class FuzzyRule:
    def __init__(self, rule_id, antecedent, consequent, operator='AND'):
        self.rule_id = rule_id
        self.antecedent = antecedent
        self.consequent = consequent
        self.operator = operator.upper()
 
    def hitung_firing_strength(self, derajat):
        nilai = [derajat[var].get(lbl, 0.0)
                 for var, lbl in self.antecedent.items()]
        if not nilai:
            return 0.0
        if self.operator == 'AND':
            return min(nilai)
        elif self.operator == 'OR':
            return max(nilai)
        raise ValueError(f"Operator {self.operator} tidak dikenali.")
 
    def __str__(self):
        syarat = f" {self.operator} ".join(
            f"{v} is {l}" for v, l in self.antecedent.items())
        hasil = ", ".join(
            f"{v} is {l}" for v, l in self.consequent.items())
        return f"[{self.rule_id}] IF {syarat} THEN {hasil}"
 
 
# ===== BASIS ATURAN =====
def R(id_, perm, stok, prod):
    return FuzzyRule(id_, {"permintaan": perm, "stok": stok},
                     {"produksi": prod})
 
rule_base = [
    R("R1", "Rendah", "Sedikit", "Sedang"),
    R("R2", "Rendah", "Sedang",  "Sedikit"),
    R("R3", "Rendah", "Banyak",  "Sedikit"),
    R("R4", "Sedang", "Sedikit", "Banyak"),
    R("R5", "Sedang", "Sedang",  "Sedang"),
    R("R6", "Sedang", "Banyak",  "Sedikit"),
    R("R7", "Tinggi", "Sedikit", "Banyak"),
    R("R8", "Tinggi", "Sedang",  "Banyak"),
    R("R9", "Tinggi", "Banyak",  "Sedang"),
]
 
# ===== DATA UJI =====
derajat_input = {
    "permintaan": {"Rendah": 0.2, "Sedang": 0.8, "Tinggi": 0.0},
    "stok":       {"Sedikit": 0.0, "Sedang": 0.5, "Banyak": 0.5},
}
 
print("=" * 80)
print("HASIL EVALUASI BASIS ATURAN - PRODUKSI ROTI")
print("=" * 80)
 
aturan_aktif = []
for rule in rule_base:
    alpha = rule.hitung_firing_strength(derajat_input)
    lbl_out = rule.consequent["produksi"]
    status = f"AKTIF (alpha = {alpha:.2f})" if alpha > 0 else "NONAKTIF"
    print(f"{rule} --> {status}")
    if alpha > 0:
        aturan_aktif.append((rule.rule_id, lbl_out, alpha))
 
print("\n" + "=" * 80)
print("RINGKASAN ATURAN YANG TERPICU:")
print("=" * 80)
for r_id, konklusi, alpha in aturan_aktif:
    print(f" - {r_id:<4}: Produksi = {konklusi:<8} dengan alpha = {alpha:.2f}")
 
# Agregasi (max) per label output
agregat = {}
for _, lbl, a in aturan_aktif:
    agregat[lbl] = max(agregat.get(lbl, 0.0), a)
print("\nAGREGASI (MAX) PER LABEL OUTPUT:")
for lbl, a in agregat.items():
    print(f" - Produksi {lbl:<8}: {a:.2f}")
