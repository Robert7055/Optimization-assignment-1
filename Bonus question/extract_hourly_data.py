"""
Extract hourly data from notebook solution variables and complete the LaTeX report
Run this in the notebook's Python environment after executing all cells
"""

# This will be run in the notebook context where variables are available
import json

# Hours to analyze
hours = [6, 12, 18]  # Morning, Midday, Evening (1-indexed in problem, 0-indexed in arrays)

# Extract data for each hour (note: hour indices are 0-based in Python)
hourly_data = {}
for h in hours:
    idx = h - 1  # Convert to 0-based index
    hourly_data[h] = {
        'pv': round(pv_prod_hourly[idx], 2),
        'ref_load': round(D_ref[idx], 2),
        'opt_load': round(D_t[h].X, 2),
        'import': round(P_imp_t[h].X, 2),
        'export': round(P_exp_t[h].X, 2),
        'mu': round(abs(mu_t[idx]), 2),
        'base_price': round(electricity_prices[idx], 2)
    }

# Print the data
print("\nHourly Characteristics:")
print("="*70)
for h in hours:
    d = hourly_data[h]
    hour_label = {6: 'Morning (6am)', 12: 'Midday (12pm)', 18: 'Evening (6pm)'}[h]
    print(f"\n{hour_label} - Hour {h}:")
    print(f"  Base price: {d['base_price']} DKK/kWh")
    print(f"  PV production: {d['pv']} kW")
    print(f"  Reference load: {d['ref_load']} kW")
    print(f"  Optimal load: {d['opt_load']} kW")
    print(f"  Grid import: {d['import']} kW")
    print(f"  Grid export: {d['export']} kW")
    print(f"  Shadow price: {d['mu']} DKK/kWh")

# Save to JSON for easy extraction
with open('hourly_data.json', 'w') as f:
    json.dump(hourly_data, f, indent=2)

print("\n" + "="*70)
print("✓ Saved hourly data to hourly_data.json")
