import pandas as pd
import random

# Generate a small dummy dataset
data = []
for i in range(200):
    if i % 2 == 0:
        text = "This is a real news article about the economy and government policies. The stock market is rising today."
        label = 0 # 0 for real
    else:
        text = "SHOCKING TRUTH! Aliens have invaded the earth and are controlling our minds through 5G towers! Click here to learn more."
        label = 1 # 1 for fake
    # add some randomness to text
    text += f" Random id {random.randint(1,1000)}."
    data.append({"text": text, "label": label})

df = pd.DataFrame(data)
df.to_csv("train.csv", index=False)
print("Dummy dataset created at train.csv")
