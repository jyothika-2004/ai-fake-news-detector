import pandas as pd
import requests
import zipfile
import io

url = "https://github.com/GeorgeMcIntire/fake_real_news_dataset/raw/master/fake_or_real_news.csv.zip"
print(f"Downloading dataset from {url}...")

response = requests.get(url)
if response.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as f:
            df = pd.read_csv(f)
            df.to_csv('train.csv', index=False)
            print(f"Dataset downloaded and extracted successfully! Shape: {df.shape}")
else:
    print(f"Failed to download: HTTP {response.status_code}")
