import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Cinematic Trends Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =========================
# Custom CSS
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1b1b1b 50%, #2b0f0f 100%);
        color: #f5f5f5;
    }
    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 20px;
        color: #cccccc;
        text-align: center;
        margin-bottom: 35px;
    }
    .section-title {
        font-size: 28px;
        font-weight: 700;
        color: #ffcc66;
        margin-top: 35px;
        margin-bottom: 15px;
    }
    .metric-card {
        background-color: rgba(255,255,255,0.08);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Sample Movie Dataset
# You can replace this part with your own CSV file later.
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
# Sidebar Filters
# =========================
st.sidebar.title("🎞️ Filter Options")

selected_genres = st.sidebar.multiselect(
    "Select Genre",
    options=sorted(df["Genre"].unique()),
    default=sorted(df["Genre"].unique())
)

selected_countries = st.sidebar.multiselect(
    "Select Country",
    options=sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

rating_range = st.sidebar.slider(
    "Rating Range",
    min_value=float(df["Rating"].min()),
    max_value=float(df["Rating"].max()),
    value=(float(df["Rating"].min()), float(df["Rating"].max()))
)

year_range = st.sidebar.slider(
    "Release Year Range",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(int(df["Year"].min()), int(df["Year"].max()))
)

filtered_df = df[
    (df["Genre"].isin(selected_genres)) &
    (df["Country"].isin(selected_countries)) &
    (df["Rating"].between(rating_range[0], rating_range[1])) &
    (df["Year"].between(year_range[0], year_range[1]))
]

# =========================
# Header
# =========================
st.markdown('<div class="main-title">🎬 Cinematic Trends Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Exploring Global Movie Genres, Audience Ratings, and Popularity Trends</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    This interactive dashboard explores how movie genres, audience ratings, popularity, box office performance,
    and global cinema trends are connected. Users can filter movies by genre, rating, country, and release year
    to discover different patterns in audience preferences.
    """
)

# =========================
# Overview Metrics
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Movies", len(filtered_df))
with col2:
    st.metric("Average Rating", round(filtered_df["Rating"].mean(), 2) if not filtered_df.empty else 0)
with col3:
    st.metric("Average Popularity", round(filtered_df["Popularity"].mean(), 2) if not filtered_df.empty else 0)
with col4:
    st.metric("Total Box Office", f"${filtered_df['BoxOffice'].sum():,.0f}M" if not filtered_df.empty else "$0M")

if filtered_df.empty:
    st.warning("No movie data matches the selected filters. Please change the filter options.")
    st.stop()

# =========================
# Movie Genre Analysis
# =========================
st.markdown('<div class="section-title">1. Movie Genre Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

genre_count = filtered_df["Genre"].value_counts().reset_index()
genre_count.columns = ["Genre", "Count"]

with col1:
    fig_bar = px.bar(
        genre_count,
        x="Genre",
        y="Count",
        title="Genre Popularity by Movie Count",
        text="Count"
    )
    fig_bar.update_layout(template="plotly_dark")
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_pie = px.pie(
        genre_count,
        names="Genre",
        values="Count",
        title="Genre Distribution"
    )
    fig_pie.update_layout(template="plotly_dark")
    st.plotly_chart(fig_pie, use_container_width=True)

# Genre trend by year
trend_df = filtered_df.groupby(["Year", "Genre"]).size().reset_index(name="Count")
fig_trend = px.line(
    trend_df,
    x="Year",
    y="Count",
    color="Genre",
    markers=True,
    title="Genre Trend Over Time"
)
fig_trend.update_layout(template="plotly_dark")
st.plotly_chart(fig_trend, use_container_width=True)

# =========================
# Audience Rating & Popularity Analysis
# =========================
st.markdown('<div class="section-title">2. Audience Rating & Popularity Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

avg_rating = filtered_df.groupby("Genre")["Rating"].mean().reset_index().sort_values("Rating", ascending=False)

with col1:
    fig_rating = px.bar(
        avg_rating,
        x="Genre",
        y="Rating",
        title="Average Rating by Genre",
        text=avg_rating["Rating"].round(2)
    )
    fig_rating.update_layout(template="plotly_dark")
    st.plotly_chart(fig_rating, use_container_width=True)

with col2:
    fig_scatter = px.scatter(
        filtered_df,
        x="Rating",
        y="Popularity",
        size="BoxOffice",
        color="Genre",
        hover_name="Movie",
        title="Rating vs Popularity"
    )
    fig_scatter.update_layout(template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("🏆 Top Rated Movies")
top_movies = filtered_df.sort_values("Rating", ascending=False)[["Movie", "Genre", "Country", "Year", "Rating", "Popularity", "BoxOffice"]]
st.dataframe(top_movies, use_container_width=True)

# =========================
# Popularity Trend Analysis
# =========================
st.markdown('<div class="section-title">3. Popularity Trend Analysis</div>', unsafe_allow_html=True)

popularity_year = filtered_df.groupby("Year")["Popularity"].mean().reset_index()

fig_popularity = px.line(
    popularity_year,
    x="Year",
    y="Popularity",
    markers=True,
    title="Average Movie Popularity by Release Year"
)
fig_popularity.update_layout(template="plotly_dark")
st.plotly_chart(fig_popularity, use_container_width=True)

# =========================
# Global Cinema Analysis
# =========================
st.markdown('<div class="section-title">4. Global Cinema Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

country_count = filtered_df["Country"].value_counts().reset_index()
country_count.columns = ["Country", "Count"]

with col1:
    fig_country = px.bar(
        country_count,
        x="Country",
        y="Count",
        title="Movie Distribution by Country",
        text="Count"
    )
    fig_country.update_layout(template="plotly_dark")
    st.plotly_chart(fig_country, use_container_width=True)

with col2:
    country_rating = filtered_df.groupby("Country")["Rating"].mean().reset_index().sort_values("Rating", ascending=False)
    fig_country_rating = px.bar(
        country_rating,
        x="Country",
        y="Rating",
        title="Average Rating by Country",
        text=country_rating["Rating"].round(2)
    )
    fig_country_rating.update_layout(template="plotly_dark")
    st.plotly_chart(fig_country_rating, use_container_width=True)

# =========================
# Movie Mood Explorer
# Creativity Feature
# =========================
st.markdown('<div class="section-title">5. Movie Mood Explorer</div>', unsafe_allow_html=True)

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

st.write(f"Based on the selected mood **{mood}**, the dashboard recommends these movies:")
st.dataframe(recommended[["Movie", "Genre", "Country", "Year", "Rating", "Popularity"]], use_container_width=True)

# =========================
# Conclusion
# =========================
st.markdown('<div class="section-title">Conclusion</div>', unsafe_allow_html=True)

st.markdown(
    """
    This dashboard shows that movie popularity is shaped by genre, audience rating, release period, and country.
    By combining cinematic visual design with interactive data visualization, this project provides a more engaging
    way to understand global cinema trends and audience preferences.
    """
)

st.caption("Final Project | Streamlit Dashboard | Movie Genre & Audience Trends")
