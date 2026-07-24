import pandas as pd

try:
    from datasets import load_dataset
    print("Downloading fake news dataset from HuggingFace...")
    ds = load_dataset("GonzaloA/fake_news")
    df = ds['train'].to_pandas()
    
    # The GonzaloA dataset has 'text' and 'label' columns
    df.to_csv('train.csv', index=False)
    print(f"Successfully saved train.csv! Shape: {df.shape}")
except ImportError:
    print("Error: 'datasets' library is not installed. Please run 'pip install datasets'.")
except Exception as e:
    print(f"Error downloading dataset: {e}")
