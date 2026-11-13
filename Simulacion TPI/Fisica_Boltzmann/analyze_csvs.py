import csv
from collections import defaultdict

for i in range(1, 5):
    path = f"d:/ag/esc{i}.csv"
    print(f"\n==================== ESCENARIO {i} ({path}) ====================")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            header = next(reader)
            print("Columns:", header)
            
            rows = []
            for row in reader:
                if not row: continue
                # replace commas with dots
                parsed = []
                for val in row:
                    try:
                        parsed.append(float(val.replace(',', '.')))
                    except ValueError:
                        parsed.append(val)
                rows.append(parsed)
            
            print(f"Total rows: {len(rows)}")
            if rows:
                print("First row:", rows[0])
                print("Last row:", rows[-1])
            
            # Group by first column
            groups = defaultdict(list)
            for r in rows:
                groups[r[0]].append(r[1:])
            
            print(f"Grouped by {header[0]} (unique: {list(groups.keys())}):")
            for k, group_rows in sorted(groups.items()):
                print(f"  {header[0]} = {k} (n = {len(group_rows)}):")
                # compute mean for each numeric column
                means = []
                for col_idx in range(len(header) - 1):
                    col_vals = [gr[col_idx] for gr in group_rows if isinstance(gr[col_idx], (int, float))]
                    if col_vals:
                        m = sum(col_vals) / len(col_vals)
                        means.append(f"{header[col_idx+1]}={m:.4f}")
                print("    " + ", ".join(means))
    except Exception as e:
        print(f"Error: {e}")
