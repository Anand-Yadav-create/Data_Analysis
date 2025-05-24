import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sms


import matplotlib.pyplot as pt
import plotly.figure_factory as ff
import plotly.graph_objs as go

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


import numpy as np
import scipy as sp
df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympic Analysis")
st.sidebar.image('https://cdn.britannica.com/01/23901-050-33507FA4/flag-Olympic-Games.jpg')

user_res = st.sidebar.radio(

    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete wise Analysis')
)



if user_res=='Medal Tally':
    st.sidebar.header("Medal Tally")
    country,years=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tall=helper.fetch_medal_tally(df,year=selected_year,country=selected_country)

    if selected_country=='Overall' and selected_year=='Overall':
        st.title("Overall Medal Tally")
    if selected_country!='Overall' and selected_year=='Overall':
        st.title(selected_country+" Performance")
    if selected_country=='Overall' and selected_year!='Overall':
        st.title("Overall Country Performance in "+str(selected_year))
    if selected_country!='Overall' and selected_year!='Overall':
        st.title(selected_country+" Performance in "+str(selected_year))
    st.table(medal_tall)


if user_res=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nation")
        st.title(nations)


    nation_over_time=helper.participating_nation_over_time(df,'region')
    fig=px.line(nation_over_time,x='Year',y='count',labels={
                     "Year": "Edition",
                     "count": "No of Countries",

                 })
    st.title("Participating nation over year")

    st.plotly_chart(fig)

    event_over_time=helper.participating_nation_over_time(df,'Event')
    fig=px.line(event_over_time,x='Year',y='count',labels={
                     "Year": "Edition",
                     "count": "Events",

                 })

    st.title("Events over year")

    st.plotly_chart(fig)

    athletes_over_time = helper.participating_nation_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Year', y='count', labels={
        "Year": "Edition",
        "count": "No of  Athletes",

    })

    st.title("Atheletes over year")

    st.plotly_chart(fig)

    st.title("No of Events over time (Every Sport)")
    fig,ax=pt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sms.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),annot = True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox("Select a Sport",sport_list)

    x=helper.most_successful(df,selected_sport)
    st.table(x)


if user_res=='Country-wise Analysis':
    st.sidebar.title("Country-Wise Analysis")
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0,'India')
    select_country=st.sidebar.selectbox('Select a Country',country_list)
    country_df=helper.year_wise_tally(df,select_country)

    fig = px.line(country_df, x='Year', y='Medal', labels={
        "Year": "Edition",


    })
    st.title(select_country+" Medal tally Over Year")

    st.plotly_chart(fig)

    st.title(select_country + " excels Over the Year")

    fx=helper.country_event_heatmap(df,select_country)
    fig, ax = pt.subplots(figsize=(20, 20))
    ax=sms.heatmap(fx,annot=True)
    st.pyplot(fig)

    st.title('Top 10 Athletes in '+select_country)
    x=helper.most_successful_countrywise(df,select_country)

    st.table(x)

if user_res== 'Athelete wise Analysis':
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    ti = athlete_df[['Age', 'Gold', 'Silver', 'Bronze']]
    x1=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    ti['Total'] = ti['Gold'] + ti['Silver'] + ti['Bronze']
    ti = ti.groupby('Age').sum()[['Total']].sort_values('Age', ascending=False).reset_index()
    fig = px.line(ti, x='Age', y='Total', labels={
        "Total": "Medal",

    })
    st.title( "Distribution of Age and Medal Over The Year")

    st.plotly_chart(fig)

    st.title("Distribution of Age and Medal in a particular Sport Over The Year")
    sport_list1 = df['Sport'].unique().tolist()
    sport_list1.sort()
    sport_list1.insert(0, 'Athletics')
    selected_sport1 = st.selectbox("Select a Sport", sport_list1)
    fr=helper.select_country_data(df,selected_sport1)

    fig = px.line(fr, x='Age', y='Total', labels={
        "Total": "Medal",

    })
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()

    sport_list.insert(0,'Overall')
    st.title('Height Vs weight')
    selected_sport=st.selectbox("Select a Sport",sport_list)

    athlete_df=helper.weight_V_height(df,selected_sport)
    fig,ax=pt.subplots()
    ax=sms.scatterplot(x=athlete_df['Weight'],y=athlete_df['Height'],hue=athlete_df['Medal'],style=athlete_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Year")
    final=helper.men_vs_women(df)
    fig=px.line(final,x='Year',y=["Male","Female"])

    st.plotly_chart(fig)








