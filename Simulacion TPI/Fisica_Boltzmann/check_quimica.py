import csv
import math
from collections import defaultdict

def stdev(vals):
    n = len(vals)
    if n <= 1: return 0.0
    mean = sum(vals) / n
    var = sum((x - mean)**2 for x in vals) / (n - 1)
    return math.sqrt(var)

base = 'D:/ag/GitHub/Simulaci-nUTN/Simulacion TPI/Quimica_Cinetica/QuimicaCinetica/Resultados Nuevos'

# EXP 2
print("\n=== QUIMICA EXP 2 ===")
with open(f'{base}/Experimento2.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]
rows2 = []
for l in lines[1:]:
    if l.startswith('N') or l.startswith('C'): continue
    try:
        parts = [float(x.replace(',','.')) for x in l.split(',')]
        rows2.append(parts)
    except:
        pass

C_vals = [x[1] for x in rows2]
C_teo = rows2[0][2]
A_vals = [x[3] for x in rows2]
B_vals = [x[4] for x in rows2]
n2 = len(rows2)
print(f"n = {n2}")
print(f"C_medio: {sum(C_vals)/n2:.2f} +- {stdev(C_vals):.2f} (Teo: {C_teo:.2f}, Error: {(sum(C_vals)/n2 - C_teo)/C_teo*100:+.2f}%)")
print(f"A_medio: {sum(A_vals)/n2:.2f} +- {stdev(A_vals):.2f} (Teo: {200 - C_teo:.2f}, Error: {(sum(A_vals)/n2 - (200-C_teo))/(200-C_teo)*100:+.2f}%)")
print(f"B_medio: {sum(B_vals)/n2:.2f} +- {stdev(B_vals):.2f} (Teo: {50 - C_teo:.2f}, Error: {(sum(B_vals)/n2 - (50-C_teo))/(50-C_teo)*100:+.2f}%)")

# EXP 3
print("\n=== QUIMICA EXP 3 ===")
with open(f'{base}/Experimento3.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]
rows3 = []
for l in lines[1:]:
    if l.startswith('e') or l.startswith('C'): continue
    try:
        parts = [float(x.replace(',','.')) for x in l.split(',')]
        rows3.append(parts)
    except:
        pass

sin_cat = [x[1] for x in rows3 if x[0] == 0.0]
con_cat = [x[1] for x in rows3 if x[0] == 1.0]
c_eq_teo = rows3[0][2]
print(f"Sin cat (n={len(sin_cat)}): {sum(sin_cat)/len(sin_cat):.2f} +- {stdev(sin_cat):.2f}, Avance: {sum(sin_cat)/len(sin_cat)/c_eq_teo*100:.1f}%")
print(f"Con cat (n={len(con_cat)}): {sum(con_cat)/len(con_cat):.2f} +- {stdev(con_cat):.2f}, Avance: {sum(con_cat)/len(con_cat)/c_eq_teo*100:.1f}%")

m_sin = sum(sin_cat)/len(sin_cat)
sd_sin = stdev(sin_cat)
m_con = sum(con_cat)/len(con_cat)
sd_con = stdev(con_cat)
se_diff = math.sqrt((sd_sin**2)/len(sin_cat) + (sd_con**2)/len(con_cat))
t_welch = (m_con - m_sin) / se_diff
num = ((sd_sin**2)/len(sin_cat) + (sd_con**2)/len(con_cat))**2
den = ((sd_sin**2/len(sin_cat))**2)/(len(sin_cat) - 1) + ((sd_con**2/len(con_cat))**2)/(len(con_cat) - 1)
df_welch = num / den
print(f"Welch t: {t_welch:.2f}, df: {df_welch:.1f}")

# EXP 4
print("\n=== QUIMICA EXP 4 ===")
with open(f'{base}/Experimento4.csv', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]
rows4 = []
for l in lines[1:]:
    if l.startswith('T') or l.startswith('K'): continue
    try:
        parts = [float(x.replace(',','.')) for x in l.split(';')]
        rows4.append(parts)
    except:
        pass

print(f"Exp 4 total rows: {len(rows4)}")
if rows4:
    # T;KeqExacta;KeqTeo;C_medio;C_eq_teo
    keq_vals = [x[1] for x in rows4]
    keq_teo = rows4[0][2]
    c_vals = [x[3] for x in rows4]
    c_teo = rows4[0][4]
    n4 = len(rows4)
    m_k = sum(keq_vals)/n4
    sd_k = stdev(keq_vals)
    m_c = sum(c_vals)/n4
    sd_c = stdev(c_vals)
    err_k = (m_k - keq_teo)/keq_teo * 100
    err_c = (m_c - c_teo)/c_teo * 100
    diff_k = [x - keq_teo for x in keq_vals]
    t_k = (sum(diff_k)/n4)/(sd_k/math.sqrt(n4))
    diff_c = [x - c_teo for x in c_vals]
    t_c = (sum(diff_c)/n4)/(sd_c/math.sqrt(n4))
    print(f"Keq: {m_k:.5f} +- {sd_k:.5f} (Teo: {keq_teo:.5f}, diff={m_k-keq_teo:+.5f}, err={err_k:+.2f}%, t={t_k:.2f})")
    print(f"C: {m_c:.2f} +- {sd_c:.2f} (Teo: {c_teo:.2f}, diff={m_c-c_teo:+.2f}, err={err_c:+.2f}%, t={t_c:.2f})")
