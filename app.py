import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

st.sidebar.image("olympic_img.png")
st.sidebar.header("OLYMPIC ANALYSIS")

df = preprocessor.preprocess(df, region_df)
user_menu = st.sidebar.radio(
    'Select an option',
    ('Introduction','Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athletic-wise Analysis')
)

if user_menu == 'Introduction':
    st.title("All About Olympics")
    st.caption("The modern Olympic Games or Olympics are leading international sporting events featuring summer and winter sports competitions in which thousands of athletes from around the world participate in a variety of competitions. The Olympic Games are considered the world's foremost sports competition with more than 200 nations participating.The Olympic Games are normally held every four years, alternating between the Summer and Winter Olympics every two years in the four-year period.")
    video_file = open('Olympic_intro.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.title("Olympics history")
    st.caption("The Olympic Games, which originated in ancient Greece as many as 3,000 years ago, were revived in the late 19th century and have become the world’s preeminent sporting competition. From the 8th century B.C. to the 4th century A.D., the Games were held every four years in Olympia, located in the western Peloponnese peninsula, in honor of the god Zeus. The first modern Olympics took place in 1896 in Athens, and featured 280 participants from 12 nations, competing in 43 events. Since 1994, the Summer and Winter Olympic Games have been held separately and have alternated every two years. The 2020 Summer Olympics, delayed one year because of the COVID-19 pandemic, it held from July 23 to August 8, 2021 in Tokyo, Japan.")
    videos = open('history.mp4', 'rb')
    video_byt = videos.read()
    st.video(video_byt)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.header("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.header("Year Wise Tally")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.header("Country Wise Tally")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.header("Year Country Wise Tally")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("Editions")
        st.title(editions)
    with col5:
        st.subheader("Hosts")
        st.title(cities)
    with col6:
        st.subheader("Sports")
        st.title(sports)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("Events")
        st.title(events)
    with col5:
        st.subheader("Athletes")
        st.title(athletes)
    with col6:
        st.subheader("Nations")
        st.title(nations)

    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.area(nations_over_time, x='Editions', y='No of Countries')
    st.header("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.occuring_event_over_time(df)
    fig2 = px.area(events_over_time, x='Editions', y='No of events')
    st.header("All Occurring Events over the years")
    st.plotly_chart(fig2)

    athletes_over_time = helper.participating_athletes_over_time(df)
    fig3 = px.area(athletes_over_time, x='Editions', y='No of Athletes')
    st.header("All occurring Participants over the years")
    st.plotly_chart(fig3)

    st.header("No of Events over time (every sport)")
    fig4, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Event', 'Sport', 'Year'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
        annot=True)
    st.pyplot(fig4)

    st.header("Most Successfull Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox("Select any Sport", sport_list)
    st.table(helper.most_successfull(df, selected_sport))

if user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country Wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select a Country", country_list)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.area(country_df, x='Year', y='Medal')
    st.title(selected_country + " medal tally over the years")
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df, selected_country)
    st.title("Events strength of " + selected_country + " in every sport")
    fig4, ax2 = plt.subplots(figsize=(20, 20))
    ax2 = sns.heatmap(pt, annot=True)
    st.pyplot(fig4)

    st.header("Most Successfull Athletes in " + selected_country)
    final_df = helper.country_successful_athlete(df, selected_country)
    st.table(final_df)

if user_menu == 'Athletic-wise Analysis':
    lst = helper.Agewise_Medal_list(df)
    fig = ff.create_distplot(lst, ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    st.header("Distribution of Age")
    fig.update_layout(autosize=False, width=850, height=550)
    st.plotly_chart(fig)

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    g, s = [], []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        g.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        s.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    figG = ff.create_distplot(g, name, show_hist=False, show_rug=False)
    figG.update_layout(autosize=False, width=850, height=550)
    st.header("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(figG)

    figS = ff.create_distplot(s, name, show_hist=False, show_rug=False)
    figS.update_layout(autosize=False, width=850, height=550)
    st.header("Distribution of Age wrt Sports(Silver Medalist)")
    st.plotly_chart(figS)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.header("Height vs Weight")
    selected_sport = st.selectbox("Select any Sport", sport_list)
    sport_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(sport_df['Weight'],athlete_df['Height'],hue=sport_df['Medal'],style=sport_df['Sex'],s=30)
    st.pyplot(fig)

    st.header("Men vs Women participation over the years")
    final = helper.men_vs_women(athlete_df)
    fig2 = px.area(final, x='Year', y=['Male', 'Female'])
    fig2.update_layout(autosize=False, width=850, height=550)
    st.plotly_chart(fig2)