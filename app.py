import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Cinematic Trends Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =========================
# Sample Dataset
# =========================
@st.cache_data
def load_data():
    data = {
        "Movie": [
            "Inception", "Parasite", "Titanic", "Avatar", "The Dark Knight",
            "La La Land", "Train to Busan", "Interstellar", "Spirited Away", "Get Out",
            "Dune", "Your Name", "The Wandering Earth", "Oldboy", "Everything Everywhere All at Once",
            "The Conjuring", "Mad Max: Fury Road", "The Notebook", "Coco", "Oppenheimer"
        ],
        "Genre": [
            "Sci-Fi", "Drama", "Romance", "Sci-Fi", "Action",
            "Romance", "Horror", "Sci-Fi", "Animation", "Horror",
            "Sci-Fi", "Animation", "Sci-Fi", "Drama", "Sci-Fi",
            "Horror", "Action", "Romance", "Animation", "Drama"
        ],
        "Rating": [8.8, 8.5, 7.9, 7.8, 9.0, 8.0, 7.6, 8.7, 8.6, 7.8, 8.0, 8.4, 6.0, 8.3, 7.8, 7.5, 8.1, 7.8, 8.4, 8.4],
        "Popularity": [95, 88, 90, 97, 96, 80, 82, 94, 85, 83, 91, 87, 75, 78, 89, 77, 86, 74, 88, 93],
        "BoxOffice": [836, 263, 2257, 2923, 1006, 472, 98, 733, 395, 255, 407, 382, 699, 15, 143, 320, 380, 118, 807, 952],
        "Year": [2010, 2019, 1997, 2009, 2008, 2016, 2016, 2014, 2001, 2017, 2021, 2016, 2019, 2003, 2022, 2013, 2015, 2004, 2017, 2023],
        "Country": [
            "USA", "South Korea", "USA", "USA", "USA",
            "USA", "South Korea", "USA", "Japan", "USA",
            "USA", "Japan", "China", "South Korea", "USA",
            "USA", "Australia", "USA", "Mexico", "USA"
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# =========================
# Advanced CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(229, 9, 20, 0.28), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(255, 184, 77, 0.15), transparent 25%),
        linear-gradient(135deg, #050505 0%, #111111 45%, #1b0708 100%);
    color: #f5f5f5;
}

[data-testid="stSidebar"] {
    background: rgba(8, 8, 8, 0.92);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.hero {
    padding: 58px 48px;
    border-radius: 30px;
    background:
        linear-gradient(120deg, rgba(0,0,0,0.95), rgba(30,0,0,0.78)),
        url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    box-shadow: 0 30px 80px rgba(0,0,0,0.55);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 28px;
}

.hero-label {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(229, 9, 20, 0.22);
    border: 1px solid rgba(229, 9, 20, 0.55);
    color: #ffb3b3;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 64px;
    line-height: 1.02;
    font-weight: 900;
    letter-spacing: -2px;
    margin-bottom: 18px;
    color: #ffffff;
}

.hero-title span {
    color: #e50914;
}

.hero-subtitle {
    max-width: 780px;
    font-size: 19px;
    line-height: 1.7;
    color: #d8d8d8;
}

.section-title {
    font-size: 27px;
    font-weight: 850;
    margin-top: 34px;
    margin-bottom: 16px;
    color: #ffffff;
    letter-spacing: -0.5px;
}

.section-title:before {
    content: "";
    display: inline-block;
    width: 8px;
    height: 24px;
    background: #e50914;
    border-radius: 20px;
    margin-right: 12px;
    vertical-align: -4px;
}

.insight-card {
    background: rgba(255,255,255,0.075);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 22px;
    border-radius: 24px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.35);
    backdrop-filter: blur(14px);
}

.movie-scroll {
    display: flex;
    gap: 18px;
    overflow-x: auto;
    padding: 10px 4px 24px 4px;
    scroll-snap-type: x mandatory;
}

.movie-scroll::-webkit-scrollbar {
    height: 8px;
}

.movie-scroll::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.05);
    border-radius: 999px;
}

.movie-scroll::-webkit-scrollbar-thumb {
    background: rgba(229, 9, 20, 0.75);
    border-radius: 999px;
}

.movie-card {
    flex: 0 0 210px;
    scroll-snap-align: start;
    background: linear-gradient(145deg, rgba(255,255,255,0.10), rgba(255,255,255,0.035));
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 12px;
    min-height: 390px;
    box-shadow: 0 16px 45px rgba(0,0,0,0.32);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 24px 60px rgba(229,9,20,0.18);
}

.movie-poster {
    width: 100%;
    height: 270px;
    object-fit: cover;
    border-radius: 16px;
    margin-bottom: 12px;
}

.movie-title {
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 10px;
}

.movie-meta {
    color: #bfbfbf;
    font-size: 14px;
    line-height: 1.7;
}

.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(229, 9, 20, 0.22);
    color: #ffb3b3;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 12px;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 18px;
    border-radius: 22px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.30);
}

[data-testid="stMetricLabel"] {
    color: #bdbdbd;
}

[data-testid="stMetricValue"] {
    color: #ffffff;
    font-weight: 900;
}

hr {
    border-color: rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar Filters
# =========================
st.sidebar.title("🎞️ Cinema Filters")
st.sidebar.caption("Explore the dataset by genre, country, rating, and release year.")

selected_genres = st.sidebar.multiselect(
    "Genre",
    sorted(df["Genre"].unique()),
    default=sorted(df["Genre"].unique())
)

selected_countries = st.sidebar.multiselect(
    "Country",
    sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

rating_range = st.sidebar.slider(
    "Audience Rating",
    float(df["Rating"].min()),
    float(df["Rating"].max()),
    (float(df["Rating"].min()), float(df["Rating"].max()))
)

year_range = st.sidebar.slider(
    "Release Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

filtered_df = df[
    (df["Genre"].isin(selected_genres)) &
    (df["Country"].isin(selected_countries)) &
    (df["Rating"].between(rating_range[0], rating_range[1])) &
    (df["Year"].between(year_range[0], year_range[1]))
]

# =========================
# Hero Section
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-label">INTERACTIVE CINEMA DATA EXPERIENCE</div>
    <div class="hero-title">Cinematic <span>Trends</span><br>Dashboard</div>
    <div class="hero-subtitle">
        Explore global movie genres, audience ratings, popularity, box office performance,
        and regional cinema patterns through an interactive visual dashboard.
    </div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No movie data matches the selected filters. Please change the filter options.")
    st.stop()

# =========================
# Overview Metrics
# =========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Movies", len(filtered_df))
col2.metric("Average Rating", round(filtered_df["Rating"].mean(), 2))
col3.metric("Average Popularity", round(filtered_df["Popularity"].mean(), 2))
col4.metric("Box Office", f"${filtered_df['BoxOffice'].sum():,.0f}M")

# =========================
# Featured Movie Cards
# =========================
st.markdown('<div class="section-title">Top Audience Picks</div>', unsafe_allow_html=True)

# Poster images for a more cinematic UI
poster_map = {
    "Inception": "https://image.tmdb.org/t/p/w500/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg",
    "Interstellar": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "The Dark Knight": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "Parasite": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    "Dune": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
    "Oppenheimer": "https://image.tmdb.org/t/p/w500/ptpr0kGAckfQkJeJIt8st5dglvd.jpg",
    "Avatar": "https://image.tmdb.org/t/p/w500/kyeqWdyUXW608qlYkRqosgbbJyK.jpg",
    "La La Land": "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg"
}

featured = filtered_df.sort_values(["Rating", "Popularity"], ascending=False).head(8)

movie_cards = ""
for _, row in featured.iterrows():
    movie_cards += f"""
    <div class="movie-card">
        <img class="movie-poster" src="{poster_map.get(row['Movie'], 'https://via.placeholder.com/300x450?text=Movie')}">
        <div class="badge">{row['Genre']}</div>
        <div class="movie-title">{row['Movie']}</div>
        <div class="movie-meta">
            {row['Country']} · {row['Year']}<br>
            ⭐ {row['Rating']} / 10 · Popularity {row['Popularity']}
        </div>
    </div>
    """

components.html(
    f"""
    <style>
        body {{
            background: transparent;
            margin: 0;
            font-family: Inter, Arial, sans-serif;
        }}
        .movie-scroll {{
            display: flex;
            gap: 18px;
            overflow-x: auto;
            padding: 10px 4px 24px 4px;
            scroll-snap-type: x mandatory;
        }}
        .movie-scroll::-webkit-scrollbar {{
            height: 8px;
        }}
        .movie-scroll::-webkit-scrollbar-track {{
            background: rgba(255,255,255,0.08);
            border-radius: 999px;
        }}
        .movie-scroll::-webkit-scrollbar-thumb {{
            background: rgba(229, 9, 20, 0.75);
            border-radius: 999px;
        }}
        .movie-card {{
            flex: 0 0 210px;
            scroll-snap-align: start;
            background: linear-gradient(145deg, rgba(255,255,255,0.14), rgba(255,255,255,0.04));
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 22px;
            padding: 12px;
            min-height: 390px;
            box-shadow: 0 16px 45px rgba(0,0,0,0.35);
            color: white;
        }}
        .movie-card:hover {{
            transform: translateY(-6px);
            transition: 0.25s ease;
            box-shadow: 0 24px 60px rgba(229,9,20,0.20);
        }}
        .movie-poster {{
            width: 100%;
            height: 270px;
            object-fit: cover;
            border-radius: 16px;
            margin-bottom: 12px;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(229, 9, 20, 0.28);
            color: #ffb3b3;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .movie-title {{
            font-size: 17px;
            font-weight: 800;
            margin-bottom: 8px;
        }}
        .movie-meta {{
            font-size: 13px;
            color: #cfcfcf;
            line-height: 1.6;
        }}
    </style>
    <div class="movie-scroll">
        {movie_cards}
    </div>
    """,
    height=480,
    scrolling=False
)

# =========================
# Chart Theme Helper
# =========================
def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f5f5f5"),
        title=dict(font=dict(size=20, color="#ffffff")),
        margin=dict(l=20, r=20, t=55, b=20),
    )
    return fig

# =========================
# Genre Analysis
# =========================
st.markdown('<div class="section-title">Movie Genre Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
genre_count = filtered_df["Genre"].value_counts().reset_index()
genre_count.columns = ["Genre", "Count"]

with col1:
    fig = px.bar(
        genre_count,
        x="Genre",
        y="Count",
        text="Count",
        title="Genre Popularity"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

with col2:
    fig = px.pie(
        genre_count,
        names="Genre",
        values="Count",
        hole=0.52,
        title="Genre Distribution"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

trend_df = filtered_df.groupby(["Year", "Genre"]).size().reset_index(name="Count")
fig = px.line(
    trend_df,
    x="Year",
    y="Count",
    color="Genre",
    markers=True,
    title="Genre Trend Over Time"
)
st.plotly_chart(style_chart(fig), use_container_width=True)

# =========================
# Audience Rating & Popularity
# =========================
st.markdown('<div class="section-title">Audience Rating & Popularity Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

avg_rating = filtered_df.groupby("Genre")["Rating"].mean().reset_index().sort_values("Rating", ascending=False)

with col1:
    fig = px.bar(
        avg_rating,
        x="Genre",
        y="Rating",
        text=avg_rating["Rating"].round(2),
        title="Average Rating by Genre"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

with col2:
    fig = px.scatter(
        filtered_df,
        x="Rating",
        y="Popularity",
        size="BoxOffice",
        color="Genre",
        hover_name="Movie",
        title="Rating vs Popularity"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

st.markdown('<div class="section-title">Top Rated Movies</div>', unsafe_allow_html=True)
st.dataframe(
    filtered_df.sort_values("Rating", ascending=False)[
        ["Movie", "Genre", "Country", "Year", "Rating", "Popularity", "BoxOffice"]
    ],
    use_container_width=True,
    hide_index=True
)

# =========================
# Popularity Trend
# =========================
st.markdown('<div class="section-title">Popularity Trend Analysis</div>', unsafe_allow_html=True)

popularity_year = filtered_df.groupby("Year")["Popularity"].mean().reset_index()
fig = px.area(
    popularity_year,
    x="Year",
    y="Popularity",
    markers=True,
    title="Average Movie Popularity by Release Year"
)
st.plotly_chart(style_chart(fig), use_container_width=True)

# =========================
# Global Cinema Analysis
# =========================
st.markdown('<div class="section-title">Global Cinema Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
country_count = filtered_df["Country"].value_counts().reset_index()
country_count.columns = ["Country", "Count"]

with col1:
    fig = px.bar(
        country_count,
        x="Country",
        y="Count",
        text="Count",
        title="Movie Distribution by Country"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

with col2:
    country_rating = filtered_df.groupby("Country")["Rating"].mean().reset_index().sort_values("Rating", ascending=False)
    fig = px.bar(
        country_rating,
        x="Country",
        y="Rating",
        text=country_rating["Rating"].round(2),
        title="Average Rating by Country"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

# =========================
# Mood Explorer
# =========================
st.markdown('<div class="section-title">Movie Mood Explorer</div>', unsafe_allow_html=True)

mood = st.selectbox(
    "Choose a movie mood",
    ["Exciting", "Emotional", "Tense", "Imaginative", "Warm"]
)

mood_map = {
    "Exciting": ["Action", "Sci-Fi"],
    "Emotional": ["Drama", "Romance"],
    "Tense": ["Horror", "Drama"],
    "Imaginative": ["Sci-Fi", "Animation"],
    "Warm": ["Romance", "Animation"]
}

recommended = filtered_df[filtered_df["Genre"].isin(mood_map[mood])].sort_values(
    ["Rating", "Popularity"], ascending=False
)

st.markdown(f"""
<div class="insight-card">
    <b>Selected Mood:</b> {mood}<br>
    This feature connects emotional viewing preferences with movie genres, making the dashboard feel more like
    an interactive cinema discovery experience rather than only a statistics page.
</div>
""", unsafe_allow_html=True)

st.dataframe(
    recommended[["Movie", "Genre", "Country", "Year", "Rating", "Popularity"]],
    use_container_width=True,
    hide_index=True
)

# =========================
# Conclusion
# =========================
st.markdown('<div class="section-title">Conclusion</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-card">
This dashboard demonstrates how movie data can be transformed into a cinematic and interactive visual experience.
By connecting genres, ratings, popularity, box office performance, and country-based comparisons, the project helps
users understand global cinema trends and audience preferences in a more engaging way.
</div>
""", unsafe_allow_html=True)

st.caption("Final Project | Streamlit Dashboard | Cinematic Trends Dashboard")
