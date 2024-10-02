import pandas as pd
import glob
import os

def process_file(file_path):
    try:
        # Read the file, using the first row as column names
        df = pd.read_csv(file_path, sep='\t', quoting=3, on_bad_lines='warn')
        
        # Check if the dataframe has 11 columns
        if len(df.columns) != 11:
            print(f"Warning: {file_path} has {len(df.columns)} columns instead of 11")
        
        # Filter rows where a.a.1 is 'L'
        df = df[df['a.a.1'] == 'Q']
        
        return df
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

# Set the path to the folder containing your TSV files
input_path = r"/Users/tanerkaragol/Desktop/AlphaMissense"
# Set the path where you want to save the output file
output_path = r"/Users/tanerkaragol/Desktop/"

all_files = glob.glob(os.path.join(input_path, "*.tsv"))

df_list = []
for file in all_files:
    df = process_file(file)
    if df is not None and not df.empty:
        df_list.append(df)

# Combine all dataframes
if df_list:
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Create the full output file path
    output_file = os.path.join(output_path, 'combined_data.csv')
    
    # Write to CSV
    combined_df.to_csv(output_file, index=False)
    print(f"Data written to {output_file}")
else:
    print("No data could be processed successfully or no rows with a.a.1 as 'L' were found.")
