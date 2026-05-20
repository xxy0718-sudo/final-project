```python
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Movie Genre & Audience Trends Dashboard",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #0b0f19;
    color: white;
    font-family: Arial, sans-serif;
}

/* Hide Streamlit Style */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Hero Banner */

.hero {
    position: relative;

    background-image:
    linear-gradient(
        rgba(0,0,0,0.7),
        rgba(0,0,0,0.8)
    ),
    url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1974&auto=format&fit=crop");

    background-size: cover;
    background-position: center;

    padding: 140px 60px;
    border-radius: 25px;

    margin-bottom: 50px;
}

.hero h1 {
    font-size: 75px;
    line-height: 1.1;
    margin-bottom: 20px;
}

.hero span {
    color: #ef4444;
}

.hero p {
    font-size: 24px;
    max-width: 850px;
    line-height: 1.8;
    color: #d1d5db;
}

/* Section Titles */

.section-title {
    font-size: 42px;
    margin-top: 60px;
    margin-bottom: 35px;
    color: white;
}

/* Metric Cards */

.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 35px;
    text-align: center;
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: #ef4444;
    box-shadow: 0 0 20px rgba(239,68,68,0.3);
}

.metric-number {
    font-size: 48px;
    color: #ef4444;
    font-weight: bold;
}

.metric-text {
    margin-top: 12px;
    color: #d1d5db;
    font-size: 18px;
}

/* Genre Cards */

.genre-container {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    margin-bottom: 30px;
}

.genre-card {
    background: #111827;
    padding: 16px 28px;
    border-radius: 40px;
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 18px;
    transition: 0.3s;
}

.genre-card:hover {
    background: #ef4444;
    transform: scale(1.05);
}

/* Movie Cards */

.movie-card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.4s;
}

.movie-card:hover {
    transform: translateY(-10px);
    border-color: #ef4444;
    box-shadow: 0 0 25px rgba(239,68,68,0.25);
}

.movie-card img {
    width: 100%;
}

.movie-content {
    padding: 20px;
}

.movie-title {
    font-size: 24px;
    margin-bottom: 12px;
}

.movie-info {
    color: #d1d5db;
    line-height: 1.9;
}

/* Search Box */

.stTextInput input {
    background-color: #111827;
    color: white;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown("""
<div class="hero">

<h1>
Exploring <span>Cinema</span><br>
Through Data
</h1>

<p>
An interactive movie discovery platform inspired by Netflix and IMDb.
Explore movie genres, audience ratings, popularity trends, and global cinema insights through cinematic data visualization.
</p>

</div>
""", unsafe_allow_html=True)

# -----------------------------------
# DATASET
# -----------------------------------

data = {
    "Movie": [
        "Inception",
        "Parasite",
        "Interstellar",
        "Avengers Endgame",
        "Joker",
        "Titanic",
        "Frozen",
        "The Conjuring"
    ],

    "Genre": [
        "Sci-Fi",
        "Drama",
        "Sci-Fi",
        "Action",
        "Drama",
        "Romance",
        "Animation",
        "Horror"
    ],

    "Rating": [
        8.8,
        8.5,
        8.7,
        8.4,
        8.3,
        7.9,
        7.5,
        7.5
    ],

    "Popularity": [
        98,
        92,
        95,
        99,
        94,
        90,
        85,
        80
    ],

    "BoxOffice": [
        829,
        258,
        701,
        2797,
        1074,
        2201,
        1280,
        320
    ],

    "Year": [
        2010,
        2019,
        2014,
        2019,
        2019,
        1997,
        2013,
        2013
    ]
}

df = pd.DataFrame(data)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🎬 Movie Filters")

genre_filter = st.sidebar.multiselect(
    "Select Genre",
    options=df["Genre"].unique(),
    default=df["Genre"].unique()
)

rating_filter = st.sidebar.slider(
    "Minimum Rating",
    0.0,
    10.0,
    7.0
)

filtered_df = df[
    (df["Genre"].isin(genre_filter)) &
    (df["Rating"] >= rating_filter)
]

# -----------------------------------
# SEARCH SECTION
# -----------------------------------

st.markdown(
    '<div class="section-title">🔍 Search Movies</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search your favorite movie"
)

if search:

    search_df = filtered_df[
        filtered_df["Movie"].str.contains(search, case=False)
    ]

else:

    search_df = filtered_df

# -----------------------------------
# METRICS
# -----------------------------------

st.markdown(
    '<div class="section-title">📊 Dashboard Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{len(search_df)}</div>
        <div class="metric-text">Movies</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{round(search_df['Rating'].mean(),1)}</div>
        <div class="metric-text">Average Rating</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{search_df['Popularity'].max()}</div>
        <div class="metric-text">Popularity Score</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">${search_df['BoxOffice'].sum()}M</div>
        <div class="metric-text">Box Office</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# GENRE SECTION
# -----------------------------------

st.markdown(
    '<div class="section-title">🎭 Movie Genres</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="genre-container">

<div class="genre-card">🎬 Action</div>
<div class="genre-card">👻 Horror</div>
<div class="genre-card">🚀 Sci-Fi</div>
<div class="genre-card">💕 Romance</div>
<div class="genre-card">🎭 Drama</div>
<div class="genre-card">✨ Animation</div>

</div>
""", unsafe_allow_html=True)

# -----------------------------------
# MOVIE CARDS
# -----------------------------------

st.markdown(
    '<div class="section-title">🎞 Top Movies</div>',
    unsafe_allow_html=True
)

movies = [
    {
        "title":"Inception",
        "image":"https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "rating":"8.8",
        "genre":"Sci-Fi"
    },

    {
        "title":"Parasite",
        "image":"https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
        "rating":"8.5",
        "genre":"Drama"
    },

    {
        "title":"Interstellar",
        "image":"https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "rating":"8.7",
        "genre":"Sci-Fi"
    }
]

col1, col2, col3 = st.columns(3)

columns = [col1, col2, col3]

for col, movie in zip(columns, movies):

    with col:

        st.markdown(f"""
        <div class="movie-card">

            <img src="{movie['image']}">

            <div class="movie-content">

                <div class="movie-title">
                    {movie['title']}
                </div>

                <div class="movie-info">
                    ⭐ Rating : {movie['rating']} <br>
                    🎬 Genre : {movie['genre']}
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)

# -----------------------------------
# CHARTS
# -----------------------------------

st.markdown(
    '<div class="section-title">📈 Audience Trends</div>',
    unsafe_allow_html=True
)

fig1 = px.bar(
    search_df,
    x="Movie",
    y="Rating",
    color="Genre",
    title="Movie Ratings"
)

fig1.update_layout(
    paper_bgcolor="#0b0f19",
    plot_bgcolor="#111827",
    font_color="white"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------

fig2 = px.line(
    search_df,
    x="Year",
    y="Popularity",
    color="Movie",
    markers=True,
    title="Popularity Trends"
)

fig2.update_layout(
    paper_bgcolor="#0b0f19",
    plot_bgcolor="#111827",
    font_color="white"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------

fig3 = px.pie(
    search_df,
    names="Genre",
    title="Genre Distribution"
)

fig3.update_layout(
    paper_bgcolor="#0b0f19",
    font_color="white"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("""
<br><br><br>

<center>

<h3>🎬 Movie Genre & Audience Trends Dashboard</h3>

<p>
Created by 허형월
</p>

</center>
""", unsafe_allow_html=True)
```
