import pandas as pd
import re

def transform_name(name):
    """Transform name from 'Last, First' to '[[First Last]]'"""
    if pd.isna(name) or name == '':
        return ''
    # Split the name and reverse it
    parts = name.split(', ')
    if len(parts) == 2:
        return f"[[{parts[1]} {parts[0]}]]"
    return f"[[{name}]]"  # If name isn't in expected format, just wrap it

def convert_to_markdown(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Transform the Name and Reports To columns
    df['Name'] = df['Name'].apply(transform_name)
    df['Reports To'] = df['Reports To'].apply(transform_name)
    
    # Convert to markdown
    markdown = "| Name | Reports To | Job Title | Number of Direct Reports | Department | Location |\n"
    markdown += "|------|------------|------------|-------------------------|------------|----------|\n"
    
    # Add each row to the markdown string
    for _, row in df.iterrows():
        markdown += f"| {row['Name']} | {row['Reports To']} | {row['Job Title']} | {row['Number of Direct Reports']} | {row['Department']} | {row['Location']} |\n"
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

# Example usage
try:
    convert_to_markdown('prospermkt-2024-12-13.xlsx', 'output_markdown.md')
    print("Conversion completed successfully!")
except Exception as e:
    print(f"An error occurred: {str(e)}")