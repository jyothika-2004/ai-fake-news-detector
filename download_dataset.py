import pandas as pd

url = "https://raw.githubusercontent.com/GeorgeMcIntire/fake_real_news_dataset/master/fake_or_real_news.csv"
try:
    print(f"Downloading dataset from {url}...")
    df = pd.read_csv(url)
    df.to_csv('train.csv', index=False)
    print(f"Dataset downloaded successfully! Shape: {df.shape}")
except Exception as e:
    print(f"Failed to download: {e}")
