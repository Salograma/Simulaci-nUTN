import csv
import math
from collections import defaultdict

def stdev(vals):
    n = len(vals)
    if n <= 1: return 0.0
    mean = sum(vals) / n
    var = sum((x - mean)**2 for x in vals) / (n - 1)
    return math.sqrt(var)

base_path = "Boltzmann/Resultados Nuevos"

# ESCENARIO 1
print("=== CUADRO 9: ESCENARIO 1 ===")
data1 = defaultdict(list)
with open(f'{base_path}/esc1.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f, delimiter=';')
    next(r)
    for row in r:
        if not row: continue
        vals = [float(x.replace(',', '.')) for x in row]
        data1[vals[0]].append(vals)

all_vMed = []
all_sqrtT = []
all_chis1 = []
for T in sorted(data1.keys()):
    rows = data1[T]
    n = len(rows)
    vMed_list = [x[1] for x in rows]
    vTeo = rows[0][2]
    chi_list = [x[5] for x in rows]
    all_chis1.extend(chi_list)
    Tmed_list = [x[6] for x in rows]
    
    mean_vMed = sum(vMed_list) / n
    sd_vMed = stdev(vMed_list)
    err_pct = ((mean_vMed - vTeo) / vTeo) * 100
    
    diffs = [x - vTeo for x in vMed_list]
    mean_diff = sum(diffs) / n
    sd_diff = stdev(diffs)
    t_val = mean_diff / (sd_diff / math.sqrt(n))
    
    mean_Tmed = sum(Tmed_list) / n
    mean_chi = (sum(chi_list) / n) * 100
    
    print(f"{int(T)} & {mean_vMed:.2f} $\\pm$ {sd_vMed:.2f} & {vTeo:.2f} & {err_pct:+.2f} \\% & {t_val:.2f} & {mean_Tmed:.1f} & {mean_chi:.1f} \\% \\\\")
    
    for v in vMed_list:
        all_vMed.append(v)
        all_sqrtT.append(math.sqrt(T))

# Regression vMed = a * sqrt(T)
# sum(vMed * sqrtT) / sum(sqrtT^2)
sum_num = sum(v * s for v, s in zip(all_vMed, all_sqrtT))
sum_den = sum(s * s for s in all_sqrtT)
a_fit = sum_num / sum_den
# residual variance
res = [v - a_fit * s for v, s in zip(all_vMed, all_sqrtT)]
var_res = sum(r**2 for r in res) / (len(all_vMed) - 1)
se_a = math.sqrt(var_res / sum_den)
t_a = (a_fit - 1.2533) / se_a
print(f"Fit a = {a_fit:.4f} +- {se_a:.4f}, t_a = {t_a:.2f}, global_chi = {sum(all_chis1)/len(all_chis1)*100:.1f}%")

# ESCENARIO 2
print("\n=== CUADRO 10: ESCENARIO 2 ===")
data2 = defaultdict(list)
with open(f'{base_path}/esc2.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f, delimiter=';')
    next(r)
    for row in r:
        if not row: continue
        vals = [float(x.replace(',', '.')) for x in row]
        data2[vals[0]].append(vals)

all_chis2 = []
for m1 in sorted(data2.keys()):
    rows = data2[m1]
    n = len(rows)
    ratioEk_list = [x[3] for x in rows]
    vrmsRatio_list = [x[5] for x in rows]
    vrmsTeo = rows[0][6]
    chi_list = [x[7] for x in rows]
    all_chis2.extend(chi_list)
    
    mean_rEk = sum(ratioEk_list) / n
    sd_rEk = stdev(ratioEk_list)
    diffs_Ek = [x - 1.0 for x in ratioEk_list]
    t_Ek = (sum(diffs_Ek)/n) / (stdev(diffs_Ek) / math.sqrt(n)) if stdev(diffs_Ek) > 0 else 0
    
    mean_rvrms = sum(vrmsRatio_list) / n
    err_vrms = ((mean_rvrms - vrmsTeo) / vrmsTeo) * 100
    diffs_vrms = [x - vrmsTeo for x in vrmsRatio_list]
    t_vrms = (sum(diffs_vrms)/n) / (stdev(diffs_vrms) / math.sqrt(n)) if stdev(diffs_vrms) > 0 else 0
    
    mean_chi = (sum(chi_list) / n) * 100
    if m1 == 1:
        print(f"1 (control) & 1 & - & 1 & 1 & - & - & {mean_chi:.1f} \\% \\\\")
    else:
        print(f"{int(m1)} & {mean_rEk:.3f} $\\pm$ {sd_rEk:.3f} & {t_Ek:.2f} & {mean_rvrms:.3f} & {vrmsTeo:.3f} & {err_vrms:+.2f} \\% & {t_vrms:.2f} & {mean_chi:.1f} \\% \\\\")

print(f"Global Chi Esc 2: {sum(all_chis2)/len(all_chis2)*100:.1f}%")

# ESCENARIO 3
print("\n=== CUADRO 11 & 12: ESCENARIO 3 ===")
data3 = defaultdict(list)
with open(f'{base_path}/esc3.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f, delimiter=';')
    next(r)
    for row in r:
        if not row: continue
        vals = [float(x.replace(',', '.')) for x in row]
        data3[vals[0]].append(vals)

for N in sorted(data3.keys()):
    rows = data3[N]
    n = len(rows)
    kn = rows[0][9]
    slope_list = [x[1] for x in rows]
    R2_list = [x[2] for x in rows]
    jumpL_list = [x[3] for x in rows]
    jumpR_list = [x[4] for x in rows]
    qL_list = [x[5] for x in rows]
    qR_list = [x[6] for x in rows]
    qSum_list = [x[7] for x in rows]
    
    mean_slope = sum(slope_list) / n
    mean_R2 = sum(R2_list) / n
    mean_qL = sum(qL_list) / n
    mean_qR = sum(qR_list) / n
    mean_qSum = sum(qSum_list) / n
    sd_qSum = stdev(qSum_list)
    t_qSum = (mean_qSum) / (sd_qSum / math.sqrt(n))
    rel_q = (mean_qSum / mean_qL) * 100
    
    mean_jL = sum(jumpL_list) / n
    sd_jL = stdev(jumpL_list)
    mean_jR = sum(jumpR_list) / n
    sd_jR = stdev(jumpR_list)
    
    print(f"Cuadro 11: {int(N)} & {kn:.3f} & {mean_slope:.2f} & {mean_R2:.2f} & {mean_qL:.0f} & {mean_qR:.0f} & {mean_qSum:+.0f} $\\pm$ {sd_qSum:.0f} & {t_qSum:.2f} & {rel_q:+.1f} \\% \\\\")
    print(f"Cuadro 12: {int(N)} & {mean_jL:+.0f} $\\pm$ {sd_jL:.0f} & {mean_jR:+.0f} $\\pm$ {sd_jR:.0f} \\\\")

# ESCENARIO 4
print("\n=== CUADRO 13: ESCENARIO 4 ===")
data4 = defaultdict(list)
with open(f'{base_path}/esc4.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f, delimiter=';')
    next(r)
    for row in r:
        if not row: continue
        vals = [float(x.replace(',', '.')) for x in row]
        data4[vals[0]].append(vals)

for N in sorted(data4.keys()):
    rows = data4[N]
    n = len(rows)
    tHalf_list = [x[1] for x in rows]
    tEq_list = [x[2] for x in rows]
    frac_list = [x[3] for x in rows]
    drift_list = [abs(x[5]) for x in rows]
    
    mean_tHalf = sum(tHalf_list) / n
    sd_tHalf = stdev(tHalf_list)
    mean_tEq = sum(tEq_list) / n
    sd_tEq = stdev(tEq_list)
    mean_frac = sum(frac_list) / n
    sd_frac = stdev(frac_list)
    
    diffs_frac = [x - 0.5 for x in frac_list]
    t_frac = (sum(diffs_frac)/n) / (stdev(diffs_frac) / math.sqrt(n))
    max_drift = max(drift_list)
    
    print(f"{int(N)} & {mean_tHalf:.1f} $\\pm$ {sd_tHalf:.1f} & {mean_tEq:.1f} $\\pm$ {sd_tEq:.1f} & {mean_frac:.4f} $\\pm$ {sd_frac:.4f} & {t_frac:.2f} & {max_drift:.1e} \\\\")
