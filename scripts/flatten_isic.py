import pandas as pd

def flatten_isic_excel(input_path: str, output_path: str = None):
    """
    Flatten ISIC Excel structure to columns: section_name, division_name, group_name, class_name, includes, excludes
    """
    # Read Excel file
    df = pd.read_excel(input_path)
    
    flattened_rows = []
    current_section = ""
    current_division = ""
    current_group = ""
    
    for _, row in df.iterrows():
        # Skip empty rows
        if pd.isna(row.iloc[0]):
            continue
            
        # Determine hierarchy level based on content patterns
        first_col = str(row.iloc[0]).strip()
        
        # Section level (single letter like A, B, C)
        if len(first_col) == 1 and first_col.isalpha():
            current_section = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            current_division = ""
            current_group = ""
            
        # Division level (2 digits like 01, 02)
        elif len(first_col) == 2 and first_col.isdigit():
            current_division = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            current_group = ""
            
        # Group level (3 digits like 011, 012)
        elif len(first_col) == 3 and first_col.isdigit():
            current_group = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            
        # Class level (4 digits like 0111, 0112)
        elif len(first_col) == 4 and first_col.isdigit():
            class_name = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            includes = row.iloc[2] if len(row) > 2 and pd.notna(row.iloc[2]) else ""
            excludes = row.iloc[3] if len(row) > 3 and pd.notna(row.iloc[3]) else ""
            
            flattened_rows.append({
                'section_name': current_section,
                'division_name': current_division,
                'group_name': current_group,
                'class_name': class_name,
                'includes': includes,
                'excludes': excludes
            })
    
    # Create DataFrame
    result_df = pd.DataFrame(flattened_rows)
    
    # Save to CSV
    if output_path is None:
        output_path = input_path.replace('.xlsx', '_flattened.csv')
    
    result_df.to_csv(output_path, index=False)
    print(f"Flattened data saved to: {output_path}")
    print(f"Total records: {len(result_df)}")
    
    return result_df

if __name__ == "__main__":
    input_file = r"C:\alkashef\GitHub\brands_dataset\data\ISIC5_Exp_Notes_11Mar2024.xlsx"
    flatten_isic_excel(input_file)