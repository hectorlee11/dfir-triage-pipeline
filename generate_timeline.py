import csv
import glob
import os

csv.field_size_limit(10000000)

triage_dir = r"C:\DFIR_Triage\Output"
master_rows = []

# 1. Parse Prefetch Output
prefetch_files = glob.glob(os.path.join(triage_dir, "Prefetch", "*_PECmd_Output.csv"))
if prefetch_files:
    with open(prefetch_files[0], mode='r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamp = row.get('LastRun', '')
            if timestamp:
                master_rows.append({
                    'Timestamp': timestamp,
                    'EventType': 'Program Execution (Prefetch)',
                    'Item': row.get('ExecutableName', 'N/A'),
                    'Details': f"Run Count: {row.get('RunCount', 'N/A')}",
                    'Source': os.path.basename(row.get('SourceFilename', 'Prefetch'))
                })

# 2. Parse JumpLists Output (Automatic/Custom Destinations)
jumplist_files = glob.glob(os.path.join(triage_dir, "JumpLists", "*.csv"))
for jf in jumplist_files:
    with open(jf, mode='r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Flexible fallbacks for JLECmd column names across different versions
            timestamp = row.get('Last Modified', '') or row.get('Last Accessed', '') or row.get('Timestamp', '')
            target = row.get('Target Path', '') or row.get('Path', '') or row.get('Application', 'N/A')
            if timestamp:
                master_rows.append({
                    'Timestamp': timestamp,
                    'EventType': 'File Access (JumpList)',
                    'Item': target,
                    'Details': f"AppID: {row.get('AppId Short', 'N/A')}",
                    'Source': os.path.basename(jf)
                })

# Sort all events chronologically (newest first)
master_rows.sort(key=lambda x: x['Timestamp'], reverse=True)

# Export to Master Markdown Timeline
markdown_output = r"C:\DFIR_Triage\TIMELINE.md"
with open(markdown_output, "w", encoding='utf-8') as f:
    f.write("# Local Endpoint Master Incident Response Timeline\n\n")
    f.write("| Timestamp (UTC) | Event Type | Target / Executable | Details | Source Artifact |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- |\n")
    for row in master_rows[:35]:
        f.write(f"| {row['Timestamp']} | {row['EventType']} | `{row['Item']}` | {row['Details']} | `{row['Source']}` |\n")

print(f"Master timeline successfully generated at {markdown_output}")
