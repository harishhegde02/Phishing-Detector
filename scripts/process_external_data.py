
import pandas as pd
import os
import glob
from sklearn.model_selection import train_test_split

def load_and_process_external_data(ext_data_dir, output_dir):
    """
    Loads external datasets, consolidates them, cleans the URL column,
    and splits into train/val/test sets.
    """
    print("Loading external datasets...")
    
    # Load ALL CSV files from ext_data/
    ext_files = glob.glob(os.path.join(ext_data_dir, '*.csv'))
    
    # Add all CSVs from data/raw/
    raw_files = []
    raw_dir = os.path.join(os.path.dirname(ext_data_dir), 'data', 'raw')
    if os.path.exists(raw_dir):
        raw_files = glob.glob(os.path.join(raw_dir, '*.csv'))
    
    dfs = []
    # Load Main External Data
    print(f"Found {len(ext_files)} files in ext_data/")
    for f in ext_files:
        print(f"Reading {f}...")
        try:
            df = pd.read_csv(f, on_bad_lines='skip', low_memory=False)
            df.columns = [c.lower().strip() for c in df.columns]
            
            # Handle both 'url' and 'text' columns
            if 'text' in df.columns and 'url' not in df.columns:
                df.rename(columns={'text': 'url'}, inplace=True)
            
            required_cols = ['url', 'urgency', 'authority', 'fear', 'impersonation']
            if all(c in df.columns for c in required_cols):
                dfs.append(df[required_cols])
                print(f"  Added {len(df)} samples from {os.path.basename(f)}")
            else:
                print(f"  Skipping {f}: Missing columns. Has: {df.columns.tolist()}")
        except Exception as e:
            print(f"  Error reading {f}: {e}")

    # Load and OVERSAMPLE Raw Benign Data
    if raw_files:
        print(f"Loading and Oversampling Raw Benign Data: {raw_files}")
        for f in raw_files:
            try:
                df = pd.read_csv(f)
                df.columns = [c.lower().strip() for c in df.columns] # normalize
                
                # Rename 'text' to 'url' if needed for consistency before rename later
                if 'text' in df.columns and 'url' not in df.columns:
                    df.rename(columns={'text': 'url'}, inplace=True)

                if 'url' in df.columns:
                     # OVERSAMPLE FACTOR: 500x to give it weight against 1M records
                     # This makes ~100 rows into ~50,000 rows
                    df_oversampled = pd.concat([df] * 500, ignore_index=True)
                    dfs.append(df_oversampled)
                    print(f"Added {len(df_oversampled)} samples from {os.path.basename(f)} (Oversampled 500x)")
            except Exception as e:
                print(f"Error reading raw file {f}: {e}")

    if not dfs:
        print("No valid external data found.")
        return

    # Consolidate
    full_df = pd.concat(dfs, ignore_index=True)
    print(f"Total raw samples: {len(full_df)}")
    
    # Deduplicate based on URL
    full_df.drop_duplicates(subset=['url'], inplace=True)
    print(f"Unique samples: {len(full_df)}")
    
    # Rename 'url' to 'text' for compatibility with existing training scripts
    full_df.rename(columns={'url': 'text'}, inplace=True)
    
    # Basic cleaning: Ensure text is string and fill NaNs
    full_df['text'] = full_df['text'].astype(str).fillna('')
    
    # Fill NaN labels with 0 and convert to numeric (handling any non-numeric values)
    label_cols = ['urgency', 'authority', 'fear', 'impersonation']
    for col in label_cols:
        # Convert to numeric, coercing errors to NaN, then fill with 0
        full_df[col] = pd.to_numeric(full_df[col], errors='coerce').fillna(0).astype(int)


    # Filtering: Remove extremely short URLs/texts (likely noise)
    full_df = full_df[full_df['text'].str.len() > 3]
    
    print(f"Samples after cleaning: {len(full_df)}")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Split Data (Train: 80%, Val: 10%, Test: 10%)
    # Using a stratified split sample if possible, but for multi-label suitable approximation
    train_df, temp_df = train_test_split(full_df, test_size=0.2, random_state=42)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)
    
    print(f"Train size: {len(train_df)}")
    print(f"Val size: {len(val_df)}")
    print(f"Test size: {len(test_df)}")
    
    # Save
    train_df.to_csv(os.path.join(output_dir, 'train_ext.csv'), index=False)
    val_df.to_csv(os.path.join(output_dir, 'val_ext.csv'), index=False)
    test_df.to_csv(os.path.join(output_dir, 'test_ext.csv'), index=False)
    
    print("Processed external data saved to data/processed/")

if __name__ == "__main__":
    EXT_DATA_DIR = os.path.join("d:\\coding_files\\DTLshit\\ext_data") # Use absolute path or relative to script execution
    OUTPUT_DIR = "d:\\coding_files\\DTLshit\\data\\processed"
    
    # Ensure paths are correct relative to where script is likely run (root)
    if not os.path.exists(EXT_DATA_DIR):
        # Fallback to relative path
        EXT_DATA_DIR = "ext_data"
        OUTPUT_DIR = "data/processed"

    load_and_process_external_data(EXT_DATA_DIR, OUTPUT_DIR)
