import numpy as np

class FuzzyRule:
    def __init__(self, antecedent_labels, consequent_label):
        self.antecedent_labels = antecedent_labels  # list: [permintaan_label, persediaan_label]
        self.consequent_label = consequent_label
        self.firing_strength = 0.0

# ----- Fungsi keanggotaan -----
def mu_permintaan(x, label):
    if label == "sedikit":
        if x <= 120:
            return 1.0
        elif 120 < x < 142:
            return (142 - x) / (142 - 120)
        else:
            return 0.0
    elif label == "sedang":
        if x <= 120 or x >= 164:
            return 0.0
        elif 120 < x <= 142:
            return (x - 120) / (142 - 120)
        else:
            return (164 - x) / (164 - 142)
    elif label == "banyak":
        if x <= 142:
            return 0.0
        elif 142 < x < 164:
            return (x - 142) / (164 - 142)
        else:
            return 1.0
    return 0.0

def mu_persediaan(y, label):
    if label == "sedikit":
        if y <= 69:
            return 1.0
        elif 69 < y < 79:
            return (79 - y) / (79 - 69)
        else:
            return 0.0
    elif label == "sedang":
        if y <= 69 or y >= 88:
            return 0.0
        elif 69 < y <= 79:
            return (y - 69) / (79 - 69)
        else:
            return (88 - y) / (88 - 79)
    elif label == "banyak":
        if y <= 79:
            return 0.0
        elif 79 < y < 88:
            return (y - 79) / (88 - 79)
        else:
            return 1.0
    return 0.0

def hitung_firing_strength(rule, x, y):
    m1 = mu_permintaan(x, rule.antecedent_labels[0])
    m2 = mu_persediaan(y, rule.antecedent_labels[1])
    return min(m1, m2)   # operator AND = min (Mamdani)

# ----- Bangun Knowledge Base (9 aturan) -----
rule_list = [
    FuzzyRule(["sedikit", "sedikit"], "sedikit"),
    FuzzyRule(["sedikit", "sedang"],  "sedikit"),
    FuzzyRule(["sedikit", "banyak"],  "sedikit"),
    FuzzyRule(["sedang",  "sedikit"], "banyak"),
    FuzzyRule(["sedang",  "sedang"],  "sedang"),
    FuzzyRule(["sedang",  "banyak"],  "sedang"),
    FuzzyRule(["banyak",  "sedikit"], "banyak"),
    FuzzyRule(["banyak",  "sedang"],  "banyak"),
    FuzzyRule(["banyak",  "banyak"],  "banyak"),
]

# ----- Uji sampel dari jurnal: Permintaan=141, Persediaan=71 -----
if __name__ == "__main__":
    x_test = 141
    y_test = 71
    print(f"Sampel input: Permintaan = {x_test}, Persediaan = {y_test}\n")
    for i, r in enumerate(rule_list, start=1):
        fs = hitung_firing_strength(r, x_test, y_test)
        r.firing_strength = fs
        print(f"R{i}: IF permintaan {r.antecedent_labels[0]} AND persediaan {r.antecedent_labels[1]} "
              f"THEN produksi {r.consequent_label} | alpha = {fs:.4f}")
