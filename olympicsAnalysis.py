import pandas as pd

def preprocess(athletes,regions):
    athletes = athletes[athletes.Season == 'Summer']
    athletes = athletes.merge(regions, on='NOC', how='left')
    athletes.drop_duplicates(inplace=True)
    athletes = pd.concat([athletes, pd.get_dummies(athletes.Medal) * 1], axis=1)
    return athletes
