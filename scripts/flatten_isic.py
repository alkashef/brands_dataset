import pandas as pd
import sys

def clean_text(text):
    """Clean text for safe console output"""
    if pd.isna(text):
        return ""
    
    # Convert to string and make lowercase
    cleaned = str(text).lower()
    
    # Remove unwanted patterns using regex for better matching
    import re
    cleaned = re.sub(r'this\s+class\s+(includes?|excludes?)\s*:?\s*', '', cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace("_x000d_", " ").replace("_x000D_", " ")
    cleaned = cleaned.replace("_x000d_", " ").replace("_x000D_", " ")
    
    # Remove "see" patterns more comprehensively
    import re
    # Remove "see NUMBER", "see group NUMBER", "see groups NUMBER and NUMBER", etc.
    cleaned = re.sub(r'\bsee\s+(group\s*|groups\s*)?[\d.,\s]+(and\s+[\d.,\s]+)*\b', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bsee\s+\d+[\d.]*\b', '', cleaned, flags=re.IGNORECASE)
    
    # Replace dashes with commas
    cleaned = cleaned.replace('-', ',').replace('–', ',').replace('—', ',')
    
    # Remove empty lines and extra whitespace
    cleaned = ' '.join(cleaned.split())
    
    # Clean up double commas with spaces
    cleaned = cleaned.replace(', ,', ',')
    
    # Remove punctuation at beginning and end
    import string
    cleaned = cleaned.strip(string.punctuation + ' ')
    
    return cleaned.encode('ascii', 'ignore').decode('ascii').strip()

def flatten_isic_excel(input_path: str, output_path: str = None):
    """
    Flatten ISIC Excel structure to columns: section_name, division_name, group_name, class_name, includes, excludes
    """
    # Read all sheets and find the one with data
    excel_file = pd.ExcelFile(input_path)
    print(f"Worksheets: {excel_file.sheet_names}")
    
    for sheet_name in excel_file.sheet_names:
        print(f"\nTrying sheet: {sheet_name}")
        df = pd.read_excel(input_path, sheet_name=sheet_name)
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        if df.empty:
            continue
        
        # Show first 15 rows to understand structure
        print("\nFirst 15 rows with their first values:")
        for idx in range(min(15, len(df))):
            row = df.iloc[idx]
            first_value = None
            for cell in row.values:
                if pd.notna(cell) and str(cell).strip():
                    first_value = str(cell).strip()
                    break
            if first_value:
                first_clean = first_value.replace('.', '').strip()
                print(f"Row {idx}: '{first_value}' -> cleaned: '{first_clean}' (len={len(first_clean)}, isdigit={first_clean.isdigit()})")
            
        flattened_rows = []
        current_section = ""
        current_division = ""
        current_group = ""
        
        for idx, row in df.iterrows():
            # Skip completely empty rows
            if row.isna().all():
                continue
            
            # Get first non-empty cell value
            first_value = None
            for cell in row.values:
                if pd.notna(cell) and str(cell).strip():
                    first_value = str(cell).strip()
                    break
            
            if not first_value:
                continue
            
            # Clean the first value for pattern matching
            first_clean = first_value.replace('.', '').strip()
            
            # Section level (single letter like T, A, B, etc)
            if len(first_clean) == 1 and first_clean.isalpha():
                current_section = clean_text(row.iloc[2]) if len(row) > 2 else ""  # Column C
                current_division = ""
                current_group = ""
                print(f"Section: {first_clean} - {current_section}")
                
            # Division level (letter + 2 digits like T94, A01, etc)
            elif len(first_clean) == 3 and first_clean[0].isalpha() and first_clean[1:].isdigit():
                current_division = clean_text(row.iloc[2]) if len(row) > 2 else ""  # Column C
                current_group = ""
                print(f"Division: {first_clean} - {current_division}")
                
            # Group level (letter + 3 digits like T941, A011, etc)  
            elif len(first_clean) == 4 and first_clean[0].isalpha() and first_clean[1:].isdigit():
                current_group = clean_text(row.iloc[2]) if len(row) > 2 else ""  # Column C
                print(f"Group: {first_clean} - {current_group}")
                
            # Class level (letter + 4 digits like T9411, A0111, etc)
            elif len(first_clean) == 5 and first_clean[0].isalpha() and first_clean[1:].isdigit():
                class_name = clean_text(row.iloc[2]) if len(row) > 2 else ""  # Column C
                includes_e = clean_text(row.iloc[4]) if len(row) > 4 else ""  # Column E
                includes_f = clean_text(row.iloc[5]) if len(row) > 5 else ""  # Column F
                excludes = clean_text(row.iloc[6]) if len(row) > 6 else ""    # Column G
                
                # Combine includes from columns E and F
                includes_parts = [includes_e, includes_f]
                includes = "; ".join([part for part in includes_parts if part]).strip()
                
                flattened_rows.append({
                    'section_name': current_section,
                    'division_name': current_division,
                    'group_name': current_group,
                    'class_name': class_name,
                    'includes': includes,
                    'excludes': excludes
                })
                
                print(f"Class: {first_clean} - {class_name}")
        
        print(f"\nTotal classes found: {len(flattened_rows)}")
        
        if flattened_rows:
            # Create DataFrame
            result_df = pd.DataFrame(flattened_rows)
            
            # Save to CSV in same directory as input file
            if output_path is None:
                output_path = input_path.replace('.xlsx', '_flattened.csv')
            
            result_df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"Flattened data saved to: {output_path}")
            print(f"Total records: {len(result_df)}")
            
            return result_df
    
    print("No data found in any sheet")
    return pd.DataFrame()

if __name__ == "__main__":
    # relative path to the input file
    input_file = r"data\isic\ISIC5_Exp_Notes_11Mar2024.xlsx"
    #input_file = r"C:\alkashef\GitHub\brands_dataset\data\isic\ISIC5_Exp_Notes_11Mar2024.xlsx"
    flatten_isic_excel(input_file)