import pandas as pd

df = pd.read_csv('nba_data_processed.csv')

df.fillna(0, inplace=True)

numeric_cols = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
df[numeric_cols] = df[numeric_cols].astype(float)

df['Player'] = df['Player'].str.upper()

df['Player'] = df['Player'].astype(object)

df.to_csv('nba_novo.csv', index=False)