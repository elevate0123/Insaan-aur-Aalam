# Re-exporting divine_names_master.csv

Run this any time `Master_Divine_Names_Dataset_v2_1.xlsx` changes (new JJK
decision, F1_Include_in_Network flag updated after consultant review, Tier 3
list grows, etc.). The pipeline reads the CSV, not the xlsx — a stale CSV
means stale results with no error message, so make this a habit after every
workbook edit.

```python
import openpyxl, csv

wb = openpyxl.load_workbook('Master_Divine_Names_Dataset_v2_1.xlsx', data_only=True)
ws = wb['Master Name List']
hdr_row = 5  # header row is row 5 in this workbook (group header is row 4)
headers = [ws.cell(row=hdr_row, column=c).value for c in range(1, ws.max_column + 1)]
idx = {h: i for i, h in enumerate(headers)}

keep_cols = [
    'A1_Serial_Number', 'A2_Arabic_Name', 'A3_Transliteration_ALA_LC',
    'A4_English_Meaning', 'A5_Arabic_Root', 'A7_Tier',
    'D1_Jalal_Jamal_Kamal', 'H1_JJK_5Class_v2_1',
    'C4_Homonym_Flag', 'F1_Include_in_Network',
]

rows_out = []
for r in range(hdr_row + 1, ws.max_row + 1):
    vals = [ws.cell(row=r, column=c + 1).value for c in range(len(headers))]
    if vals[0] is None:
        continue
    rows_out.append([vals[idx[k]] for k in keep_cols])

with open('divine_names_master.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(keep_cols)
    writer.writerows(rows_out)

print(f"Exported {len(rows_out)} names.")
```

If you add NEW columns to the workbook that the pipeline should use (e.g.
once the Islamic Studies consultant finalizes the Disputed-node network
decision, or Tier 3 grows), add them to `keep_cols` here AND to the
`DivineName` dataclass in `src/names_loader.py` — the two must stay in sync.
