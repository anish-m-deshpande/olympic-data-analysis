import numpy as np
import streamlit as st
import pandas as pd
import olympicsAnalysis
import fetch
import plotly.express as px
import matplotlib.pyplot as pt
import seaborn as sns
import plotly.figure_factory as pf

athletes = pd.read_csv('athlete_events.csv.zip')
regions = pd.read_csv('noc_regions.csv')
df = olympicsAnalysis.preprocess(athletes, regions)
st.set_page_config(layout="wide")
st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Wise Analysis')
)
if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = fetch.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title('Overall Tally')
    elif selected_year == 'Overall':
        st.title(selected_country + ' Overall Tally')
    elif selected_country == 'Overall':
        st.title(str(selected_year) + ' Medal Tally')
    else:
        st.title(str(selected_year) + " " + selected_country + ' Medal Tally')
    medal_tally = fetch.medal_tally(df, selected_year, selected_country)
    st.table(medal_tally)
if user_menu == 'Overall Analysis':
    st.title('Olympic Statistics:')
    st.sidebar.header('Overall Analysis')
    editions = df['Year'].unique().shape[0] - 1
    cities = df.City.unique().shape[0]
    sports = df.Sport.unique().shape[0]
    events = df.Event.unique().shape[0]
    no_athletes = df.Name.unique().shape[0]
    nations = df.region.unique().shape[0]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions:')
        st.title(editions)
    with col2:
        st.header('Hosts:')
        st.title(cities)
    with col3:
        st.header('Sports:')
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events:')
        st.title(events)
    with col2:
        st.header('Nations:')
        st.title(nations)
    with col3:
        st.header('Athletes:')
        st.title(no_athletes)
    nations_over_time = fetch.participating_nations_overtime(df)

    figure = px.line(nations_over_time, x='Edition', y='No of countries')
    st.title('Participating Nations Over Time:')
    st.plotly_chart(figure, use_container_width=True)
    events_over_time = fetch.events_over_time(df)
    st.title('Events Conducted Over Time:')
    figure2 = px.line(events_over_time, x='Edition', y='Events')
    st.plotly_chart(figure2, use_container_width=True)
    st.title('Athletes Over Time:')
    athletes_over_time = fetch.athletes_over_time(df)
    figure3 = px.line(athletes_over_time, x='Edition', y='Athletes')
    st.plotly_chart(figure3, use_container_width=True)
    st.title('Events Conducted per Sport Over Time:')
    graph = df.drop_duplicates(['Year', 'Event', 'Sport'])
    fig, ax = pt.subplots(figsize=(20, 20))
    ax = sns.heatmap(graph.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0),
                     annot=True)
    st.pyplot(fig)
    st.title('Most Successful Athletes:')
    x = fetch.get_sports_list(df)
    selected_sport = st.selectbox('Select Sport', x)
    table = fetch.most_successful(df, selected_sport)
    st.table(table)
if user_menu == 'Country Wise Analysis':
    x = df.dropna(subset=['Medal'])
    x = x.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    country_list = df.dropna(subset=['Medal', 'region'])['region'].unique().tolist()
    country_list = np.sort(country_list).tolist()
    selected_country1 = st.sidebar.selectbox('Select Country', country_list)
    st.title(selected_country1 + ' Medals won Over the Years:')
    c = fetch.medals_over_years(x, selected_country1)
    fig = px.line(c, x='Year', y='Medal')
    st.plotly_chart(fig, use_container_width=True)
    st.title(selected_country1 + "'s Sport Wise Heatmap:")
    graph = df[df['region'] == selected_country1]
    graph = graph.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    graph.dropna(subset=['Medal'], inplace=True)
    fig, ax = pt.subplots(figsize=(20, 20))
    ax = sns.heatmap(graph.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0),
                     annot=True)
    st.pyplot(fig)
    st.title(selected_country1 + "'s Most Successful Athletes:")
    msa = fetch.most_successful_athlete(df, selected_country1)
    st.table(msa)
if user_menu == 'Athlete Wise Analysis':
    st.title('Age Distribution:')
    x = df.drop_duplicates(subset=['Name', 'region'])
    x1 = x['Age'].dropna()
    x2 = x[x['Medal'] == 'Gold']['Age'].dropna()
    x3 = x[x['Medal'] == 'Silver']['Age'].dropna()
    x4 = x[x['Medal'] == 'Bronze']['Age'].dropna()
    fig = pf.create_distplot([x1, x2, x3, x4],
                             ['Participants', 'Gold Medalist', 'Silver Medalists', 'Bronze Medalists'], show_hist=False,
                             show_rug=False)
    fig.update_layout(autosize=False, height=600)
    st.plotly_chart(fig, use_container_width=True)
    l1, l2 = fetch.sport_wise_graph(df)
    st.title("Sport Wise Winners Age Distribution:")
    fig1 = pf.create_distplot(l1, l2, show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False, height=800)
    st.plotly_chart(fig1, use_container_width=True)
    st.title('Height vs Weight:')
    temp_df = df.dropna(subset=['Height', 'Weight'])
    temp_df.drop_duplicates(subset=['Name'], inplace=True)
    temp_df['Medal'].fillna('No Medal', inplace=True)
    sports_list=df['Sport'].dropna().unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sport', sports_list)
    fig2, ax = pt.subplots(figsize=(15, 15))
    if selected_sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == selected_sport]
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], s=50, style=temp_df['Sex'],
                         palette=["blue", "gold", "black", "brown"])
    st.pyplot(fig2, use_container_width=False)
    st.title('Male vs Female Participation Over the Years:')
    male_vs_female=fetch.male_vs_female(df)
    fig=px.line(male_vs_female,x='Year',y=['Male','Female'])
    st.plotly_chart(fig,use_container_width=True)