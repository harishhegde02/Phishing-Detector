import pandas as pd
import sys
import os
from sklearn.model_selection import train_test_split

# Ensure we can import from utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.preprocessing import preprocess_dataframe
except ImportError:
    # Fallback if utils not found or running from wrong dir
    print("Warning: Could not import preprocess_dataframe. Using identity.")
    def preprocess_dataframe(df):
        # Basic cleanup if utils missing
        df['cleaned_text'] = df['text'].astype(str).str.lower()
        return df

def main():
    print("Starting data processing...")
    
    # Load raw data
    raw_dir = 'data/raw'
    dfs = []
    
    # Read all CSVs in raw_dir
    import glob
    csv_files = glob.glob(os.path.join(raw_dir, '*.csv'))
    
    for file in csv_files:
        try:
            print(f"Loading {file}")
            df_temp = pd.read_csv(file)
            if not df_temp.empty:
                dfs.append(df_temp)
        except Exception as e:
            print(f"Error loading {file}: {e}")
        
    if not dfs:
        print("No data found in data/raw/")
        return

    df = pd.concat(dfs, ignore_index=True)
    print(f"Total samples: {len(df)}")
    
    # Preprocess
    # Check if 'cleaned_text' already exists or needs creation
    if 'cleaned_text' not in df.columns:
        df = preprocess_dataframe(df)
    
    # Drops duplicates
    df = df.drop_duplicates(subset=['cleaned_text'])
    print(f"Samples after deduplication: {len(df)}")
    
    # Split
    train_df, tmp_df = train_test_split(df, test_size=0.3, random_state=42)
    val_df, test_df = train_test_split(tmp_df, test_size=0.5, random_state=42)
    
    print(f"Train size: {len(train_df)}")
    print(f"Val size: {len(val_df)}")
    print(f"Test size: {len(test_df)}")
    
    # Save
    processed_dir = 'data/processed'
    os.makedirs(processed_dir, exist_ok=True)
    
    train_df.to_csv(os.path.join(processed_dir, 'train.csv'), index=False)
    val_df.to_csv(os.path.join(processed_dir, 'val.csv'), index=False)
    test_df.to_csv(os.path.join(processed_dir, 'test.csv'), index=False)
    
    print(f"Saved processed splits to {processed_dir}")

if __name__ == "__main__":
    main()
