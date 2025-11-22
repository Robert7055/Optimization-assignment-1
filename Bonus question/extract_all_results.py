"""
Extract ALL numerical results from Part_2A_bonus.ipynb and populate the LaTeX report completely
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
            
            # Extract all possible values
            patterns = {
                # Basic solution values
                'total_cost': r'Objective value \(Total cost\): ([\d.]+) DKK',
                'import_cost': r'Import cost: ([\d.]+) DKK',
                'export_revenue': r'Export revenue: ([\d.]+) DKK',
                'net_energy_cost': r'Net energy cost: ([-\d.]+) DKK',
                'discomfort_cost': r'Discomfort cost: ([\d.]+) DKK',
                'total_pv': r'Total PV production:\s+([\d.]+) kWh',
                'total_curtailment': r'Total PV curtailment:\s+([\d.]+) kWh',
                'total_import': r'Total grid import:\s+([\d.]+) kWh',
                'total_export': r'Total grid export:\s+([\d.]+) kWh',
                'total_load': r'Total load:\s+([\d.]+) kWh',
                'reference_load': r'Reference load:\s+([\d.]+) kWh',
                'load_deviation': r'Load deviation:\s+([-\d.]+) kWh',
                # Shadow price statistics
                'mu_mean': r'Mean shadow price.*?:\s+([\d.]+)',
                'mu_min': r'Min shadow price.*?:\s+([\d.]+)',
                'mu_max': r'Max shadow price.*?:\s+([\d.]+)',
                'mu_std': r'Std dev shadow price.*?:\s+([\d.]+)',
                # Curtailment analysis
                'curtailment_hours': r'Hours with curtailment:\s+(\d+)',
                'mean_curtail_dual': r'Mean \(when curtailing\):\s+([\d.]+)',
                # Discomfort analysis
                'hours_above_ref': r'Hours above reference:\s+(\d+)',
                'hours_below_ref': r'Hours below reference:\s+(\d+)',
                'hours_at_ref': r'Hours at reference:\s+(\d+)',
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, text, re.DOTALL)
                if match:
                    values[key] = match.group(1)
            
            # Extract hour-specific data from threshold analysis
            hour_patterns = [
                (6, 'Morning \(6am\) \(Hour 6\)'),
                (12, 'Midday \(12pm\) \(Hour 12\)'),
                (18, 'Evening \(6pm\) \(Hour 18\)')
            ]
            
            for hour_num, hour_label in hour_patterns:
                hour_section = re.search(
                    f'{hour_label}:(.*?)(?=(?:Morning|Midday|Evening|$))', 
                    text, 
                    re.DOTALL
                )
                if hour_section:
                    section = hour_section.group(1)
                    h_patterns = {
                        f'h{hour_num}_base_price': r'Base price:\s+([\d.]+)',
                        f'h{hour_num}_mu': r'Base μ_t:\s+([\d.]+)',
                        f'h{hour_num}_wtp': r'Maximum willingness to pay:\s+([-\d.]+)',
                        f'h{hour_num}_wtp_theory': r'Theoretical WTP[^:]*:\s+([\d.]+)',
                        f'h{hour_num}_moc': r'Minimum opportunity cost:\s+([\d.]+)',
                        f'h{hour_num}_moc_theory': r'Theoretical MOC[^:]*:\s+([\d.]+)',
                        f'h{hour_num}_action': r'Base case action:\s+([A-Z]+)',
                    }
                    for key, pattern in h_patterns.items():
                        match = re.search(pattern, section)
                        if match:
                            values[key] = match.group(1)
    
    return values

# Extract values from notebook cells
print("Extracting all values from notebook...")
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        extracted = extract_from_output(cell)
        results.update(extracted)

print(f"Extracted {len(results)} values\n")

# Now we need to get PV, load, import/export for each hour from the notebook variables
# These are stored in the kernel variables, so we'll add placeholders and note what's needed
print("Additional values needed from notebook execution:")
print("  - Hour 6/12/18: PV production, reference load, optimal load, grid import/export")
print("  These need to be extracted from the notebook's solution variables\n")

# Read the LaTeX template
with open('Question_2A_Report.tex', 'r', encoding='utf-8') as f:
    latex_content = f.read()

# First, replace the simple values that we have
def safe_replace(old, new):
    """Replace if old string exists in content"""
    global latex_content
    if old in latex_content:
        latex_content = latex_content.replace(old, new)
        return True
    return False

# Table 1: Solution summary - these all work
safe_replace('29.25', results.get('total_cost', '29.25'))
safe_replace('24.94', results.get('import_cost', '24.94'))  
safe_replace('0.00', results.get('export_revenue', '0.00'))
safe_replace('24.94', results.get('net_energy_cost', '24.94'))
safe_replace('4.31', results.get('discomfort_cost', '4.31'))

# Table 1: Energy totals
replacements = [
    ('Total PV Production & [Run notebook] & kWh', 
     f'Total PV Production & {results.get("total_pv", "N/A")} & kWh'),
    ('Total PV Curtailment & [Run notebook] & kWh',
     f'Total PV Curtailment & {results.get("total_curtailment", "N/A")} & kWh'),
    ('Total Grid Import & [Run notebook] & kWh',
     f'Total Grid Import & {results.get("total_import", "N/A")} & kWh'),
    ('Total Grid Export & [Run notebook] & kWh',
     f'Total Grid Export & {results.get("total_export", "N/A")} & kWh'),
    ('Total Load & [Run notebook] & kWh',
     f'Total Load & {results.get("total_load", "N/A")} & kWh'),
    ('Reference Load & [Run notebook] & kWh',
     f'Reference Load & {results.get("reference_load", "N/A")} & kWh'),
    ('Load Deviation & [Run notebook] & kWh',
     f'Load Deviation & {results.get("load_deviation", "N/A")} & kWh'),
    
    # Table 2: Shadow prices
    ('Mean & 1.7629', f'Mean & {results.get("mu_mean", "1.7629")}'),
    ('Minimum & 1.3500', f'Minimum & {results.get("mu_min", "1.3500")}'),
    ('Maximum & 2.7000', f'Maximum & {results.get("mu_max", "2.7000")}'),
    ('Standard Deviation & 0.3703', f'Standard Deviation & {results.get("mu_std", "0.3703")}'),
    
    # Curtailment analysis
    ('Hours with curtailment: 0 out of 24',
     f'Hours with curtailment: {results.get("curtailment_hours", "0")} out of 24'),
    ('Mean dual (when curtailing): [Run notebook] DKK/kWh',
     f'Mean dual (when curtailing): {results.get("mean_curtail_dual", "N/A")} DKK/kWh'),
    
    # Discomfort analysis
    ('Hours with load $>$ reference: 16',
     f'Hours with load $>$ reference: {results.get("hours_above_ref", "16")}'),
    ('Hours with load $<$ reference: 9',
     f'Hours with load $<$ reference: {results.get("hours_below_ref", "9")}'),
    ('Hours at reference: [Run notebook]',
     f'Hours at reference: {results.get("hours_at_ref", "N/A")}'),
]

for old, new in replacements:
    safe_replace(old, new)

# Representative hour characteristics table - these need actual notebook data
# For now, mark them clearly as needing data extraction from solution vectors
hour_table_replacements = [
    # Hour 6
    ('[Notebook] & [Notebook] & [Notebook]', 
     f'{results.get("h6_base_price", "N/A")} & {results.get("h12_base_price", "N/A")} & {results.get("h18_base_price", "N/A")}'),
]

# Price threshold table
threshold_replacements = []
for h, h_label in [(6, 'h6'), (12, 'h12'), (18, 'h18')]:
    threshold_replacements.extend([
        (f'[Notebook] & [Notebook] & [Notebook]',
         f'{results.get(f"{h_label}_base_price", "N/A")} & {results.get(f"{h_label}_mu", "N/A")} & {results.get(f"{h_label}_action", "N/A")}')
    ])

# Remove all remaining [Run notebook] and [Notebook] placeholders with clear notes
latex_content = latex_content.replace('[Run notebook]', 'TBD')
latex_content = latex_content.replace('[Notebook]', 'TBD')

# Write the updated LaTeX file
output_file = 'Question_2A_Report_filled.tex'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(latex_content)

print(f"✓ Created {output_file}")
print("\nExtracted values:")
for key, value in sorted(results.items()):
    print(f"  {key}: {value}")

print("\n" + "="*70)
print("Status:")
print(f"  - Extracted {len(results)} values from notebook outputs")
print("  - Populated basic solution statistics")
print("  - Some hour-specific details marked as 'TBD' (need solution vectors)")
print("\nRemaining 'TBD' values need extraction from notebook solution variables")
print("="*70)
