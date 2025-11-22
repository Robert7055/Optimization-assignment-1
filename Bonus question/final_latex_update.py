"""
Final update to LaTeX report - populate ALL remaining TBD values
"""

import json

# Load the hourly data
with open('hourly_data.json', 'r') as f:
    hourly_data = json.load(f)

# Read the current LaTeX file
with open('Question_2A_Report_filled.tex', 'r', encoding='utf-8') as f:
    latex = f.read()

# Extract data for each hour
h6 = hourly_data['6']
h12 = hourly_data['12']
h18 = hourly_data['18']

# We already have extracted values from earlier run - load them
import re
with open('Question_2A_Report_filled.tex', 'r', encoding='utf-8') as f:
    temp_latex = f.read()

# Extract the already-extracted threshold values
threshold_values = {}
for h_num, h_label in [(6, 'h6'), (12, 'h12'), (18, 'h18')]:
    # These were extracted by extract_all_results.py
    pass

# Hardcode the extracted threshold values (from previous extraction)
thresholds = {
    '6': {'wtp': 1.90, 'wtp_theory': 1.05, 'moc': 2.80, 'moc_theory': 1.95, 'action': 'SELF'},
    '12': {'wtp': 0.80, 'wtp_theory': 0.85, 'moc': 1.80, 'moc_theory': 1.75, 'action': 'SELF'},
    '18': {'wtp': 1.80, 'wtp_theory': 1.85, 'moc': 2.80, 'moc_theory': 2.75, 'action': 'SELF'},
}

# Replace the hourly characteristics table rows
replacements = {
    'Base price (DKK/kWh) & TBD & TBD & TBD \\\\':
        f'Base price (DKK/kWh) & {h6["base_price"]} & {h12["base_price"]} & {h18["base_price"]} \\\\',
    
    'PV production (kW) & TBD & TBD & TBD \\\\':
        f'PV production (kW) & {h6["pv"]} & {h12["pv"]} & {h18["pv"]} \\\\',
    
    'Reference load (kW) & TBD & TBD & TBD \\\\':
        f'Reference load (kW) & {h6["ref_load"]} & {h12["ref_load"]} & {h18["ref_load"]} \\\\',
    
    'Optimal load (kW) & TBD & TBD & TBD \\\\':
        f'Optimal load (kW) & {h6["opt_load"]} & {h12["opt_load"]} & {h18["opt_load"]} \\\\',
    
    'Grid import (kW) & TBD & TBD & TBD \\\\':
        f'Grid import (kW) & {h6["import"]} & {h12["import"]} & {h18["import"]} \\\\',
    
    'Grid export (kW) & TBD & TBD & TBD \\\\':
        f'Grid export (kW) & {h6["export"]} & {h12["export"]} & {h18["export"]} \\\\',
    
    'Shadow price (DKK/kWh) & TBD & TBD & TBD \\\\':
        f'Shadow price (DKK/kWh) & {h6["mu"]} & {h12["mu"]} & {h18["mu"]} \\\\',
    
    # Price threshold table
    'Max WTP (DKK/kWh) & TBD & TBD & TBD \\\\':
        f'Max WTP (DKK/kWh) & {thresholds["6"]["wtp"]} & {thresholds["12"]["wtp"]} & {thresholds["18"]["wtp"]} \\\\',
    
    'Theoretical WTP & TBD & TBD & TBD \\\\':
        f'Theoretical WTP & {thresholds["6"]["wtp_theory"]} & {thresholds["12"]["wtp_theory"]} & {thresholds["18"]["wtp_theory"]} \\\\',
    
    'Min MOC (DKK/kWh) & TBD & TBD & TBD \\\\':
        f'Min MOC (DKK/kWh) & {thresholds["6"]["moc"]} & {thresholds["12"]["moc"]} & {thresholds["18"]["moc"]} \\\\',
    
    'Theoretical MOC & TBD & TBD & TBD \\\\':
        f'Theoretical MOC & {thresholds["6"]["moc_theory"]} & {thresholds["12"]["moc_theory"]} & {thresholds["18"]["moc_theory"]} \\\\',
    
    'Base case action & TBD & TBD & TBD \\\\':
        f'Base case action & {thresholds["6"]["action"]} & {thresholds["12"]["action"]} & {thresholds["18"]["action"]} \\\\',
}

# Apply all replacements
for old, new in replacements.items():
    latex = latex.replace(old, new)

# Check for any remaining TBD values
remaining_tbd = latex.count('TBD')

# Write the final LaTeX file
output_file = 'Question_2A_Report_complete.tex'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(latex)

print(f"✓ Created {output_file}")
print(f"\nApplied {len(replacements)} replacements")
print(f"Remaining TBD placeholders: {remaining_tbd}")

if remaining_tbd == 0:
    print("\n🎉 SUCCESS! All values populated - LaTeX report is complete!")
else:
    print(f"\n⚠️  Still {remaining_tbd} TBD values remaining")

print("\n" + "="*70)
print("LaTeX compilation:")
print("  pdflatex Question_2A_Report_complete.tex")
print("  (or upload to Overleaf with the PNG plots)")
print("="*70)
