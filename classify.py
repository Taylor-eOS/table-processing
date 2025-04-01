import pandas as pd
from llm import is_tech_industry

df = pd.read_csv('industries.csv')
df['needs_tech'] = None

for index, row in df.iterrows():
    industry = str(row['industry'])
    result = is_tech_industry(industry)
    df.at[index, 'needs_tech'] = result
    print(f"Processed: {industry} → {result}")

df.to_csv('industries_classified.csv', index=False)
print("\nFinal results:")
print(df.head())
