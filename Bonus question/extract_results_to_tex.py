"""
Extract numerical results from Part_2A_bonus.ipynb and fill in the LaTeX report tables
"""

import json
import re

# Load the notebook
with open('Part_2A_bonus.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Dictionary to store extracted values
results = {}

# Function to extract values from cell outputs
def extract_from_output(cell):
    if 'outputs' not in cell:
        return {}
    
    values = {}
    for output in cell['outputs']:
        if 'text' in output:
            text = ''.join(output['text']) if isinstance(output['text'], list) else output['text']
            
            # Extract various values using regex
            patterns = {
                'total_cost': r'Objective value \(Total cost\): ([\d.]+) DKK',
                'import_cost': r'Import cost: ([\d.]+) DKK',
                'export_revenue': r'Export revenue: ([\d.]+) DKK',
                'net_energy_cost': r'Net energy cost: ([\d.]+) DKK',
                'discomfort_cost': r'Discomfort cost: ([\d.]+) DKK',
                'total_pv': r'Total PV production:\s+([\d.]+) kWh',
                'total_curtailment': r'Total PV curtailment:\s+([\d.]+) kWh',
                'total_import': r'Total grid import:\s+([\d.]+) kWh',
                'total_export': r'Total grid export:\s+([\d.]+) kWh',
                'total_load': r'Total load:\s+([\d.]+) kWh',
                'reference_load': r'Reference load:\s+([\d.]+) kWh',
                'load_deviation': r'Load deviation:\s+([-\d.]+) kWh',
                'mu_mean': r'Mean:\s+([\d.]+) DKK/kWh',
                'mu_min': r'Min:\s+([\d.]+) DKK/kWh',
                'mu_max': r'Max:\s+([\d.]+) DKK/kWh',
                'mu_std': r'Std Dev:\s+([\d.]+) DKK/kWh',
                'curtailment_hours': r'Hours with curtailment: (\d+) out of',
                'mean_curtail_dual': r'Mean \(when curtailing\):\s+([\d.]+) DKK/kWh',
                'hours_above_ref': r'Hours above reference: (\d+)',
                'hours_below_ref': r'Hours below reference: (\d+)',
                'hours_at_ref': r'Hours at reference: (\d+)',
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, text)
                if match:
                    values[key] = match.group(1)
    
    return values

# Extract values from notebook cells
print("Extracting values from notebook...")
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        extracted = extract_from_output(cell)
        results.update(extracted)

print(f"Extracted {len(results)} values")

# Read the LaTeX template
with open('Question_2A_Report.tex', 'r', encoding='utf-8') as f:
    latex_content = f.read()

# Replace placeholders with actual values
replacements = {
    # Table 1: Optimal Solution Summary
    'Total Cost & [From notebook] & DKK': f'Total Cost & {results.get("total_cost", "[Run notebook]")} & DKK',
    'Import Cost & [From notebook] & DKK': f'Import Cost & {results.get("import_cost", "[Run notebook]")} & DKK',
    'Export Revenue & [From notebook] & DKK': f'Export Revenue & {results.get("export_revenue", "[Run notebook]")} & DKK',
    'Net Energy Cost & [From notebook] & DKK': f'Net Energy Cost & {results.get("net_energy_cost", "[Run notebook]")} & DKK',
    'Discomfort Cost & [From notebook] & DKK': f'Discomfort Cost & {results.get("discomfort_cost", "[Run notebook]")} & DKK',
    'Total PV Production & [From notebook] & kWh': f'Total PV Production & {results.get("total_pv", "[Run notebook]")} & kWh',
    'Total PV Curtailment & [From notebook] & kWh': f'Total PV Curtailment & {results.get("total_curtailment", "[Run notebook]")} & kWh',
    'Total Grid Import & [From notebook] & kWh': f'Total Grid Import & {results.get("total_import", "[Run notebook]")} & kWh',
    'Total Grid Export & [From notebook] & kWh': f'Total Grid Export & {results.get("total_export", "[Run notebook]")} & kWh',
    'Total Load & [From notebook] & kWh': f'Total Load & {results.get("total_load", "[Run notebook]")} & kWh',
    'Reference Load & [From notebook] & kWh': f'Reference Load & {results.get("reference_load", "[Run notebook]")} & kWh',
    'Load Deviation & [From notebook] & kWh': f'Load Deviation & {results.get("load_deviation", "[Run notebook]")} & kWh',
    
    # Table 2: Shadow Price Statistics
    'Mean & [From notebook]': f'Mean & {results.get("mu_mean", "[Run notebook]")}',
    'Minimum & [From notebook]': f'Minimum & {results.get("mu_min", "[Run notebook]")}',
    'Maximum & [From notebook]': f'Maximum & {results.get("mu_max", "[Run notebook]")}',
    'Standard Deviation & [From notebook]': f'Standard Deviation & {results.get("mu_std", "[Run notebook]")}',
    
    # PV Curtailment Analysis
    'Hours with curtailment: [From notebook] out of 24': 
        f'Hours with curtailment: {results.get("curtailment_hours", "[Run notebook]")} out of 24',
    'Mean dual (when curtailing): [From notebook] DKK/kWh':
        f'Mean dual (when curtailing): {results.get("mean_curtail_dual", "[Run notebook]")} DKK/kWh',
    
    # Discomfort Analysis
    'Hours with load $>$ reference: [From notebook]':
        f'Hours with load $>$ reference: {results.get("hours_above_ref", "[Run notebook]")}',
    'Hours with load $<$ reference: [From notebook]':
        f'Hours with load $<$ reference: {results.get("hours_below_ref", "[Run notebook]")}',
    'Hours at reference: [From notebook]':
        f'Hours at reference: {results.get("hours_at_ref", "[Run notebook]")}',
}

# Apply replacements
for old, new in replacements.items():
    latex_content = latex_content.replace(old, new)

# Write the updated LaTeX file
output_file = 'Question_2A_Report_filled.tex'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(latex_content)

print(f"\n✓ Created {output_file}")
print("\nExtracted values:")
for key, value in sorted(results.items()):
    print(f"  {key}: {value}")

print("\n" + "="*70)
print("Next steps:")
print("1. Run the notebook Part_2A_bonus.ipynb to generate all outputs")
print("2. Run this script again: python extract_results_to_tex.py")
print("3. Compile: pdflatex Question_2A_Report_filled.tex")
print("="*70)
