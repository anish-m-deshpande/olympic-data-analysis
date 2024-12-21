import numpy as np


def medal_tally(df, year, country):
    flag = 0
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    if year != 'Overall' and country == 'Overall':
        medal_tally = medal_tally[medal_tally['Year'] == year]
    if year == 'Overall' and country != 'Overall':
        flag = 1
        medal_tally = medal_tally[medal_tally['region'] == country]
    if year != 'Overall' and country != 'Overall':
        medal_tally = medal_tally[(medal_tally['Year'] == year) & (medal_tally['region'] == country)]
    if flag == 1:
        medal_tally.Year = medal_tally.Year.astype(str)
        medal_tally = medal_tally.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year')
        medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Bronze'] + medal_tally['Silver']
    else:
        medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']]
        medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Bronze'] + medal_tally['Silver']
        medal_tally = medal_tally.sort_values('Total', ascending=False).reset_index()
    return medal_tally


def country_year_list(df):
    country = np.unique(df['region'].dropna().values).tolist()
    years = np.unique(df['Year'].dropna().values).tolist()
    years.sort()
    country.sort()
    years.insert(0, 'Overall')
    country.insert(0, 'Overall')
    return years, country


def participating_nations_overtime(df):
    nations = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
    nations.rename(columns={'Year': 'Edition', 'count': 'No of countries'}, inplace=True)
    return nations.sort_values('Edition')


def events_over_time(df):
    events = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index()
    events.rename(columns={'Year': 'Edition', 'count': 'Events'}, inplace=True)
    return events.sort_values('Edition')


def athletes_over_time(df):
    athletes = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index()
    athletes.rename(columns={'Year': 'Edition', 'count': 'Athletes'}, inplace=True)
    return athletes.sort_values('Edition')

def get_sports_list(df):
    x= np.unique(df['Sport']).tolist()
    x.insert(0,'Overall')
    return x

def most_successful(df, sport):
    df.dropna(subset=['Medal'], inplace=True)
    if (sport != 'Overall'):
        df = df[df['Sport'] == sport]
    return df['Name'].value_counts().reset_index().head(15).merge(df, on='Name', how='left').drop_duplicates(['Name'])[
        ['Name', 'count', 'region', 'Sport']].rename(columns={'count': 'Medals'}).reset_index().drop(columns=['index'])
def medals_over_years(x,country):
    x=x[x['region']==country]
    return x.groupby('Year').count()['Medal'].reset_index()
def sport_heatmap(df,country):
    sport = df[df['region'] == country]
    sport.dropna(subset=['Medal'], inplace=True)
    sport.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    return sport.groupby('Sport').count()['Medal'].reset_index()
def most_successful_athlete(df,country):
    topa = df.dropna(subset=['Medal'])
    topa = topa[topa['region'] == country]
    topa = topa.groupby('Name').count()['Medal'].reset_index()
    topa=topa.sort_values(by='Medal',ascending=False).reset_index()[['Name','Medal']].head(15)
    topa=topa.rename(columns={'Medal':'Medals'})
    tempdf = df.drop_duplicates(subset=['Name'])
    tempdf = tempdf[tempdf['region'] == country]
    return topa.merge(tempdf, on='Name')[['Name',  'Sport','Medals']]
def sport_wise_graph(df):
    sports=df.dropna(subset=['Medal'])
    sports=sports['Sport'].value_counts().reset_index()
    sports=sports[sports['count'] >50]
    sports=sports['Sport'].values.tolist()
    age_dist=[]
    for i in sports:
        age_dist.append(df[df['Sport']==i]['Age'].dropna())
    return age_dist,sports
def male_vs_female(df):
    male = df[df['Sex'] == 'M']
    female = df[df['Sex'] == 'F']
    male = male.groupby('Year').count().reset_index()
    female = female.groupby('Year').count().reset_index()
    male.rename(columns={'ID': 'Male'}, inplace=True)
    female.rename(columns={'ID': 'Female'}, inplace=True)
    female = female[['Year', 'Female']]
    male = male[['Year', 'Male']]
    return male.merge(female, on='Year')
