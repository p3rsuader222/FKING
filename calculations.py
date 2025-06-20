import os
import pandas as pd

# === CONFIG ===
BASE_DIR = r'D:\relocationasonedrive\LEARNCODE\FKING\data\raw'
SAVE_PATH = r'D:\relocationasonedrive\LEARNCODE\FKING\data\eda_summary.txt'

# === LOAD ALL CSV FILES ===
dataframes = {}
print("🔍 Loading files...")
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            try:
                df = pd.read_csv(file_path)
                key = os.path.splitext(file)[0].lower().replace(" ", "_")
                dataframes[key] = df
                print(
                    f"✅ Loaded: {key} ({df.shape[0]} rows, {df.shape[1]} cols)")
            except Exception as e:
                print(f"❌ Failed to load {file_path}: {e}")

# === PROFILE DATASETS ===
print("\n📊 Profiling datasets...")
with open(SAVE_PATH, 'w', encoding='utf-8') as f:
    for name, df in dataframes.items():
        f.write(f"\n===== {name.upper()} =====\n")
        f.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} cols\n\n")
        f.write("🔸 Column Info:\n")
        f.write(str(df.dtypes))
        f.write("\n\n🔸 Missing Values:\n")
        f.write(str(df.isnull().sum()))
        f.write("\n\n🔸 Sample Rows:\n")
        f.write(str(df.head(3)))
        f.write("\n\n")

        # Check for likely join keys
        likely_keys = [col for col in df.columns if 'id' in col.lower(
        ) or 'date' in col.lower() or 'store' in col.lower()]
        if likely_keys:
            f.write("🔗 Possible Join Keys: " + ", ".join(likely_keys) + "\n")
        f.write("\n\n")

print(f"\n📁 Summary saved to: {SAVE_PATH}")
