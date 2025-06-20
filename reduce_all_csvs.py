import os
import pandas as pd

# Set your root directory and target size in bytes (10MB)
root_dir = "D:/relocationasonedrive/LEARNCODE/Git_Finejas/pricing-insights-portfolio/data"
target_size = 10 * 1024 * 1024  # 10MB

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.lower().endswith('.csv') and '_reduced' not in filename:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            if file_size <= target_size:
                print(f"Skipping {file_path} (already <= 10MB)")
                continue

            print(f"Processing {file_path} ({file_size/1024/1024:.2f} MB)")

            # Read the CSV
            df = pd.read_csv(file_path)
            # Estimate fraction to keep
            frac = target_size / file_size
            frac = min(frac, 1.0)
            if frac <= 0 or len(df) == 0:
                print(f"Skipping {file_path} (cannot reduce further)")
                continue

            df_sampled = df.sample(frac=frac, random_state=42)
            new_filename = filename.replace('.csv', '_reduced.csv')
            output_path = os.path.join(dirpath, new_filename)
            df_sampled.to_csv(output_path, index=False)
            new_size = os.path.getsize(output_path)
            print(
                f"Saved reduced file to {output_path} ({new_size/1024/1024:.2f} MB)")
