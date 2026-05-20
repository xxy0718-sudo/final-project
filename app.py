import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# Page Config
# --------------------------------

st.set_page_config(
    page_title="Movie Trends Dashboard",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------
# Custom CSS
# --------------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #0b0f19;
    color: white;
    font-family: Arial, sans-serif;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

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

    margin-bottom: 40px;
}

.hero h1 {
    font-size: 70px;
    margin-bottom: 20px;
    color: white;
}

.hero span {
    color: #ef4444;
}

.hero p {
    font-size: 24px;
    color: #d1d5db;
    max-width: 800px;
    line-height: 1.8;
}

.section-title {
    font-size: 40px;
    margin-top: 50px;
    margin-bottom: 30px;
    color: white;
}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

.metric-number {
    font-size: 48px;
    color: #ef4444;
    font-weight: bold;
}

.metric-text {
    margin-top: 10px;
    font-size: 18px;
    color: #d1d5db;
}

.genre-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 40px;
}

.genre-card {
    background: #111827;
    padding: 18px 28px;
    border-radius: 40px;
    border: 1px solid rgba(255,255,255,0.1);
    font-size: 18px;
}

.movie-card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

.movie-card img {
    width: 100%;
}

.movie-content {
    padding: 20px;
}

.movie-title {
    font-size: 22px;
    margin-bottom: 10px;
    color: white;
}

.movie-info {
    color: #d1d5db;
    line-height: 1.8;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# Hero
# --------------------------------

st.markdown("""
<div class="hero">

<h1>
Exploring <span>Cinema</span><br>
Through Data
</h1>

<p>
An interactive cinematic dashboard analyzing movie genres,
audience ratings, popularity trends, and global cinema insights.
</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------
# Dataset
# --------------------------------

data = {
    "Movie": [
        "Inception",
        "Parasite",
        "Avengers Endgame",
        "Interstellar",
        "Joker",
        "Titanic",
        "Frozen",
        "The Conjuring"
    ],

    "Genre": [
        "Sci-Fi",
        "Drama",
        "Action",
        "Sci-Fi",
        "Drama",
        "Romance",
        "Animation",
        "Horror"
    ],

    "Rating": [
        8.8,
        8.5,
        8.4,
        8.7,
        8.3,
        7.9,
        7.5,
        7.5
    ],

    "Popularity": [
        98,
        92,
        99,
        95,
        94,
        90,
        85,
        80
    ],

    "BoxOffice": [
        829,
        258,
        2797,
        701,
        1074,
        2201,
        1280,
        320
    ],

    "Year": [
        2010,
        2019,
        2019,
        2014,
        2019,
        1997,
        2013,
        2013
    ]
}

df = pd.DataFrame(data)

# --------------------------------
# Sidebar
# --------------------------------

st.sidebar.title("🎬 Filter Movies")

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

# --------------------------------
# Metrics
# --------------------------------

st.markdown(
    '<div class="section-title">Dashboard Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{len(filtered_df)}</div>
        <div class="metric-text">Movies</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{round(filtered_df['Rating'].mean(),1)}</div>
        <div class="metric-text">Average Rating</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{filtered_df['Popularity'].max()}</div>
        <div class="metric-text">Popularity Score</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">${filtered_df['BoxOffice'].sum()}M</div>
        <div class="metric-text">Box Office</div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------
# Charts
# --------------------------------

st.markdown(
    '<div class="section-title">Audience Trends</div>',
    unsafe_allow_html=True
)

fig1 = px.bar(
    filtered_df,
    x="Movie",
    y="Rating",
    color="Genre"
)

fig1.update_layout(
    paper_bgcolor="#0b0f19",
    plot_bgcolor="#111827",
    font_color="white"
)

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    filtered_df,
    x="Year",
    y="Popularity",
    color="Movie",
    markers=True
)

fig2.update_layout(
    paper_bgcolor="#0b0f19",
    plot_bgcolor="#111827",
    font_color="white"
)

st.plotly_chart(fig2, use_container_width=True)

fig3 = px.pie(
    filtered_df,
    names="Genre"
)

fig3.update_layout(
    paper_bgcolor="#0b0f19",
    font_color="white"
)

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------
# Footer
# --------------------------------

st.markdown("""
<br><br>

<center>

<h3>🎬 Movie Genre & Audience Trends Dashboard</h3>

<p>Created by 허형월</p>

</center>
""", unsafe_allow_html=True)
