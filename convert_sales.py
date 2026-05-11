import csv
import glob
import os

input_dir = 'data'
files = sorted(glob.glob(os.path.join(input_dir, 'daily_sales_data_*.csv')))
output = 'formatted_sales.csv'
rows = []

for fn in files:
    with open(fn, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r['product'].strip().lower() == 'pink morsel':
                price = r['price'].strip().replace('$', '')
                sales = float(price) * float(r['quantity'])
                rows.append({
                    'Sales': int(sales) if sales.is_integer() else sales,
                    'Date': r['date'],
                    'Region': r['region'],
                })

with open(output, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Sales', 'Date', 'Region'])
    writer.writeheader()
    writer.writerows(rows)

print(f'Created {output} with {len(rows)} rows')
