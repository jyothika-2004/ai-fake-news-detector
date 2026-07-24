import pandas as pd

print("Loading Kaggle datasets...")
fake_df = pd.read_csv(r"dataset\News _dataset\Fake.csv")
true_df = pd.read_csv(r"dataset\News _dataset\True.csv")

# Add labels
fake_df['label'] = 'Fake News'
true_df['label'] = 'Real News'

# Combine and shuffle
combined_df = pd.concat([fake_df, true_df], ignore_index=True)
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# The dataset has columns: title, text, subject, date.
# We will combine title and text for better accuracy.
combined_df['text'] = combined_df['title'] + " " + combined_df['text']

# Keep only necessary columns to reduce file size just in case
final_df = combined_df[['text', 'label']]

print(f"Combined dataset shape: {final_df.shape}")
final_df.to_csv("train.csv", index=False)
print("Saved to train.csv!")
