import csv
import math
from collections import defaultdict

def run_stats():
    # ESCENARIO 1
    with open('d:/ag/esc1.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        h = next(reader)
        data1 = defaultdict(list)
        for r in reader:
            if not r: continue
            vals = [float(x.replace(',', '.')) for x in r]
            T, vMed, vTeo, vrmsMed, vrmsTeo, chiFrac, Tmed = vals
            data1[T].append({
                'vMed': vMed, 'vTeo': vTeo, 'vrmsMed': vrmsMed, 'vrmsTeo': vrmsTeo,
                'chiFrac': chiFrac, 'Tmed': Tmed
            })
            
    print("=== ESTADÍSTICAS ESCENARIO 1 ===")
    all_chi1 = []
    # Check vMed vs vTeo, vrmsMed vs vrmsTeo, Tmed vs T
    # Also regression vMed vs sqrt(T) and vMed vs sqrt(Tmed)
    sum_sqrtT_vMed = 0.0
    sum_T = 0.0
    sum_sqrtTmed_vMed = 0.0
    sum_Tmed = 0.0
    
    for T in sorted(data1.keys()):
        rows = data1[T]
        n = len(rows)
        v_diffs = [r['vMed'] - r['vTeo'] for r in rows]
        vrms_diffs = [r['vrmsMed'] - r['vrmsTeo'] for r in rows]
        T_diffs = [r['Tmed'] - T for r in rows]
        chis = [r['chiFrac'] for r in rows]
        all_chi1.extend(chis)
        
        mv = sum(r['vMed'] for r in rows)/n
        mvteo = rows[0]['vTeo']
        mvrms = sum(r['vrmsMed'] for r in rows)/n
        mvrmsteo = rows[0]['vrmsTeo']
        mTmed = sum(r['Tmed'] for r in rows)/n
        mchi = sum(chis)/n
        
        # paired t-test for vMed vs vTeo (nominal)
        mean_diff = sum(v_diffs)/n
        var_diff = sum((x - mean_diff)**2 for x in v_diffs)/(n - 1)
        se_diff = math.sqrt(var_diff/n)
        t_v = mean_diff / se_diff if se_diff > 0 else 0
        
        # paired t-test for vrmsMed vs vrmsTeo (nominal)
        mean_vrms_diff = sum(vrms_diffs)/n
        var_vrms_diff = sum((x - mean_vrms_diff)**2 for x in vrms_diffs)/(n - 1)
        se_vrms_diff = math.sqrt(var_vrms_diff/n)
        t_vrms = mean_vrms_diff / se_vrms_diff if se_vrms_diff > 0 else 0

        # paired t-test for vrmsMed vs sqrt(2 * kB * Tmed) -> exactly sqrt(2*Tmed)
        vrms_eff_diffs = [r['vrmsMed'] - math.sqrt(2 * r['Tmed']) for r in rows]
        mean_eff_diff = sum(vrms_eff_diffs)/n
        var_eff_diff = sum((x - mean_eff_diff)**2 for x in vrms_eff_diffs)/(n - 1)
        se_eff_diff = math.sqrt(var_eff_diff/n)
        t_eff = mean_eff_diff / se_eff_diff if se_eff_diff > 0 else 0
        
        print(f"T={T}: vMed={mv:.3f} (teo {mvteo:.3f}, diff={mean_diff:+.3f}, t={t_v:+.2f}), "
              f"vrms={mvrms:.3f} (teo {mvrmsteo:.3f}, t={t_vrms:+.2f}), t_eff={t_eff:+.2f}, "
              f"Tmed={mTmed:.1f}, chiFrac={mchi:.3f}")
    
    print(f"Chi global Esc 1: {sum(all_chi1)/len(all_chi1):.4f}")

    # ESCENARIO 2
    with open('d:/ag/esc2.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        h = next(reader)
        data2 = defaultdict(list)
        for r in reader:
            if not r: continue
            vals = [float(x.replace(',', '.')) for x in r]
            m1, EkL, EkH, ratioEk, ratioTeo, vrmsRatio, vrmsRatioTeo, chiFrac = vals
            data2[m1].append({
                'EkL': EkL, 'EkH': EkH, 'ratioEk': ratioEk, 'ratioTeo': ratioTeo,
                'vrmsRatio': vrmsRatio, 'vrmsRatioTeo': vrmsRatioTeo, 'chiFrac': chiFrac
            })
            
    print("\n=== ESTADÍSTICAS ESCENARIO 2 ===")
    all_chi2 = []
    for m1 in sorted(data2.keys()):
        rows = data2[m1]
        n = len(rows)
        rEk = [r['ratioEk'] for r in rows]
        rvrms = [r['vrmsRatio'] for r in rows]
        rEk_diff = [r['ratioEk'] - 1.0 for r in rows]
        rvrms_diff = [r['vrmsRatio'] - r['vrmsRatioTeo'] for r in rows]
        chis = [r['chiFrac'] for r in rows]
        all_chi2.extend(chis)
        
        m_rEk = sum(rEk)/n
        m_rvrms = sum(rvrms)/n
        teo_vrms = rows[0]['vrmsRatioTeo']
        
        # t-test for ratioEk == 1.0
        m_dEk = sum(rEk_diff)/n
        var_dEk = sum((x - m_dEk)**2 for x in rEk_diff)/(n - 1)
        se_dEk = math.sqrt(var_dEk/n)
        t_dEk = m_dEk / se_dEk if se_dEk > 0 else 0
        
        # t-test for vrmsRatio == sqrt(m1)
        m_dvrms = sum(rvrms_diff)/n
        var_dvrms = sum((x - m_dvrms)**2 for x in rvrms_diff)/(n - 1)
        se_dvrms = math.sqrt(var_dvrms/n)
        t_dvrms = m_dvrms / se_dvrms if se_dvrms > 0 else 0
        
        print(f"m1={m1:.0f}: ratioEk={m_rEk:.4f} (diff={m_dEk:+.4f}, t={t_dEk:+.2f}), "
              f"vrmsRatio={m_rvrms:.4f} (teo {teo_vrms:.4f}, diff={m_dvrms:+.4f}, t={t_dvrms:+.2f}), "
              f"chiFrac={sum(chis)/n:.4f}")
    print(f"Chi global Esc 2: {sum(all_chi2)/len(all_chi2):.4f}")

    # ESCENARIO 3
    with open('d:/ag/esc3.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        h = next(reader)
        data3 = defaultdict(list)
        for r in reader:
            if not r: continue
            vals = [float(x.replace(',', '.')) for x in r]
            N, slope, R2, jumpL, jumpR, qL, qR, qSum, qSumTeo, Kn = vals
            data3[N].append({
                'slope': slope, 'R2': R2, 'jumpL': jumpL, 'jumpR': jumpR,
                'qL': qL, 'qR': qR, 'qSum': qSum, 'Kn': Kn
            })
            
    print("\n=== ESTADÍSTICAS ESCENARIO 3 ===")
    for N in sorted(data3.keys()):
        rows = data3[N]
        n = len(rows)
        m_slope = sum(r['slope'] for r in rows)/n
        m_R2 = sum(r['R2'] for r in rows)/n
        m_jumpL = sum(r['jumpL'] for r in rows)/n
        m_jumpR = sum(r['jumpR'] for r in rows)/n
        m_qL = sum(r['qL'] for r in rows)/n
        m_qR = sum(r['qR'] for r in rows)/n
        m_qSum = sum(r['qSum'] for r in rows)/n
        kn = rows[0]['Kn']
        
        # t-test for qSum == 0
        qSums = [r['qSum'] for r in rows]
        var_qSum = sum((x - m_qSum)**2 for x in qSums)/(n - 1)
        se_qSum = math.sqrt(var_qSum/n)
        t_qSum = m_qSum / se_qSum if se_qSum > 0 else 0
        
        # qSum relative to qL
        rel_imbalance = (m_qSum / m_qL) * 100
        
        print(f"N={N:.0f} (Kn={kn:.4f}): slope={m_slope:.3f}, R2={m_R2:.3f}, jumpL={m_jumpL:.1f}, jumpR={m_jumpR:.1f}, "
              f"qL={m_qL:.1f}, qR={m_qR:.1f}, qSum={m_qSum:.1f} (rel={rel_imbalance:+.2f}%, t={t_qSum:+.2f})")

    # ESCENARIO 4
    with open('d:/ag/esc4.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        h = next(reader)
        data4 = defaultdict(list)
        for r in reader:
            if not r: continue
            vals = [float(x.replace(',', '.')) for x in r]
            N, tHalf, tEq, fracFin, fracTeo, eDriftPpm = vals
            data4[N].append({
                'tHalf': tHalf, 'tEq': tEq, 'fracFin': fracFin, 'fracTeo': fracTeo,
                'eDriftPpm': eDriftPpm
            })
            
    print("\n=== ESTADÍSTICAS ESCENARIO 4 ===")
    for N in sorted(data4.keys()):
        rows = data4[N]
        n = len(rows)
        m_tHalf = sum(r['tHalf'] for r in rows)/n
        m_tEq = sum(r['tEq'] for r in rows)/n
        m_fracFin = sum(r['fracFin'] for r in rows)/n
        m_eDrift = sum(r['eDriftPpm'] for r in rows)/n
        
        frac_diffs = [r['fracFin'] - 0.5 for r in rows]
        m_fdiff = sum(frac_diffs)/n
        var_fdiff = sum((x - m_fdiff)**2 for x in frac_diffs)/(n - 1)
        se_fdiff = math.sqrt(var_fdiff/n)
        t_frac = m_fdiff / se_fdiff if se_fdiff > 0 else 0
        
        print(f"N={N:.0f}: tHalf={m_tHalf:.2f}s, tEq={m_tEq:.2f}s, fracFin={m_fracFin:.4f} (diff={m_fdiff:+.4f}, t={t_frac:+.2f}), eDriftPpm={m_eDrift:.2e}")

run_stats()
