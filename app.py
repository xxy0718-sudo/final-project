import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Movie Genre & Audience Trends Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =========================
# Dataset
# =========================
@st.cache_data
def load_data():
    data = {
        "Movie": [
            "Inception", "Parasite", "Titanic", "Avatar", "The Dark Knight",
            "La La Land", "Train to Busan", "Interstellar", "Spirited Away", "Get Out",
            "Dune", "Your Name", "The Wandering Earth", "Oldboy",
            "Everything Everywhere All at Once", "The Conjuring",
            "Mad Max: Fury Road", "The Notebook", "Coco", "Oppenheimer"
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
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(229, 9, 20, 0.25), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(255, 184, 77, 0.12), transparent 25%),
        linear-gradient(135deg, #050505 0%, #111111 45%, #1b0708 100%);
    color: white;
}

[data-testid="stSidebar"] {
    background: rgba(8, 8, 8, 0.95);
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
    margin-bottom: 28px;
}

.hero-label {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(229, 9, 20, 0.25);
    color: #ffb3b3;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 60px;
    line-height: 1.05;
    font-weight: 900;
    color: white;
    margin-bottom: 18px;
}

.hero-title span {
    color: #e50914;
}

.hero-subtitle {
    max-width: 780px;
    font-size: 18px;
    line-height: 1.7;
    color: #d8d8d8;
}

.section-title {
    font-size: 28px;
    font-weight: 850;
    margin-top: 36px;
    margin-bottom: 18px;
    color: white;
}

.section-title:before {
    content: "";
    display: inline-block;
    width: 8px;
    height: 25px;
    background: #e50914;
    border-radius: 20px;
    margin-right: 12px;
    vertical-align: -4px;
}

.insight-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.35);
    margin-top: 15px;
    margin-bottom: 25px;
    color: #f2f2f2;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 18px;
    border-radius: 20px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.30);
}
</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
st.sidebar.title("🎞️ Cinema Filters")
st.sidebar.caption("Explore movies by genre, country, rating, and year.")

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
# Hero
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-label">INTERACTIVE CINEMA DATA EXPERIENCE</div>
    <div class="hero-title">Movie Genre &<br><span>Audience Trends</span> Dashboard</div>
    <div class="hero-subtitle">
        Exploring global movie genres, audience ratings, popularity, box office performance,
        and regional cinema patterns through an interactive visual dashboard.
    </div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No movie data matches the selected filters. Please change the filter options.")
    st.stop()

# =========================
# Metrics
# =========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Movies", len(filtered_df))
col2.metric("Average Rating", round(filtered_df["Rating"].mean(), 2))
col3.metric("Average Popularity", round(filtered_df["Popularity"].mean(), 2))
col4.metric("Box Office", f"${filtered_df['BoxOffice'].sum():,.0f}M")

# =========================
# Dynamic Insight
# =========================
top_genre = filtered_df["Genre"].value_counts().idxmax()
top_country = filtered_df["Country"].value_counts().idxmax()
avg_rating_value = round(filtered_df["Rating"].mean(), 2)
avg_popularity_value = round(filtered_df["Popularity"].mean(), 2)

st.markdown(f"""
<div class="insight-card">
    <b>Current Insight</b><br>
    Based on the selected filters, <b>{top_genre}</b> is the most represented genre,
    and <b>{top_country}</b> appears most frequently in the filtered dataset.
    The average rating is <b>{avg_rating_value}</b>, while the average popularity score is <b>{avg_popularity_value}</b>.
    This shows that each filter changes not only the charts, but also the interpretation of audience trends.
</div>
""", unsafe_allow_html=True)

# =========================
# Movie Cards
# =========================
st.markdown('<div class="section-title">Top Audience Picks</div>', unsafe_allow_html=True)

poster_map = {
    "The Dark Knight": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "Interstellar": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "Parasite": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    "Oppenheimer": "https://image.tmdb.org/t/p/w500/ptpr0kGAckfQkJeJIt8st5dglvd.jpg",
    "Inception": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    "Spirited Away": "https://upload.wikimedia.org/wikipedia/en/d/db/Spirited_Away_Japanese_poster.png",
    "Coco": "https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg",
    "Your Name": "https://upload.wikimedia.org/wikipedia/en/0/0b/Your_Name_poster.png"
}

featured_movies = [
    "The Dark Knight",
    "Inception",
    "Interstellar",
    "Spirited Away",
    "Parasite",
    "Oppenheimer",
    "Coco",
    "Your Name"
]

featured = filtered_df[filtered_df["Movie"].isin(featured_movies)]

movie_cards = ""
for _, row in featured.iterrows():
    movie_cards += f"""
    <div class="movie-card">
        <img class="movie-poster" src="{poster_map.get(row['Movie'], '')}">
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
            font-family: Arial, sans-serif;
        }}

        .movie-scroll {{
            display: flex;
            gap: 18px;
            overflow-x: auto;
            padding: 10px 20px 28px 20px;
        }}

        .movie-scroll::-webkit-scrollbar {{
            height: 8px;
        }}

        .movie-scroll::-webkit-scrollbar-track {{
            background: rgba(255,255,255,0.08);
            border-radius: 999px;
        }}

        .movie-scroll::-webkit-scrollbar-thumb {{
            background: rgba(229, 9, 20, 0.8);
            border-radius: 999px;
        }}

        .movie-card {{
            flex: 0 0 220px;
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
# Chart Style
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
# Interactive Analysis Mode
# =========================
st.markdown('<div class="section-title">Interactive Analysis Mode</div>', unsafe_allow_html=True)

analysis_mode = st.radio(
    "Choose an analysis mode",
    ["Genre View", "Rating View", "Country View", "Mood View"],
    horizontal=True
)

if analysis_mode == "Genre View":
    st.subheader("Genre View")
    genre_count = filtered_df["Genre"].value_counts().reset_index()
    genre_count.columns = ["Genre", "Count"]

    fig = px.bar(
        genre_count,
        x="Genre",
        y="Count",
        text="Count",
        title="Movie Count by Genre"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.info("This view helps users compare which movie genres appear most frequently.")

elif analysis_mode == "Rating View":
    st.subheader("Rating View")
    avg_rating = filtered_df.groupby("Genre")["Rating"].mean().reset_index()

    fig = px.bar(
        avg_rating,
        x="Genre",
        y="Rating",
        text=avg_rating["Rating"].round(2),
        title="Average Rating by Genre"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.info("This view shows which genres receive higher audience ratings.")

elif analysis_mode == "Country View":
    st.subheader("Country View")
    country_count = filtered_df["Country"].value_counts().reset_index()
    country_count.columns = ["Country", "Count"]

    fig = px.bar(
        country_count,
        x="Country",
        y="Count",
        text="Count",
        title="Movie Distribution by Country"
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.info("This view compares movie distribution across countries.")

elif analysis_mode == "Mood View":
    st.subheader("Mood View")

    mood = st.radio(
        "Select a Mood",
        ["Exciting", "Emotional", "Tense", "Imaginative", "Warm"],
        horizontal=True
    )

    mood_map = {
        "Exciting": ["Action", "Sci-Fi"],
        "Emotional": ["Drama", "Romance"],
        "Tense": ["Horror", "Drama"],
        "Imaginative": ["Sci-Fi", "Animation"],
        "Warm": ["Romance", "Animation"]
    }

    recommended = filtered_df[
        filtered_df["Genre"].isin(mood_map[mood])
    ].sort_values(["Rating", "Popularity"], ascending=False)

    st.markdown(f"""
    <div class="insight-card">
        <b>Selected Mood:</b> {mood}<br>
        Recommended genres: <b>{", ".join(mood_map[mood])}</b>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        recommended[["Movie", "Genre", "Country", "Year", "Rating", "Popularity"]],
        use_container_width=True,
        hide_index=True
    )

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

correlation = filtered_df["Rating"].corr(filtered_df["Popularity"])

if correlation > 0.5:
    relation_text = "a strong positive relationship"
elif correlation > 0.2:
    relation_text = "a moderate positive relationship"
elif correlation > -0.2:
    relation_text = "a weak relationship"
else:
    relation_text = "a negative relationship"

st.markdown(f"""
<div class="insight-card">
    <b>Rating vs Popularity Insight</b><br>
    The correlation between audience rating and popularity is <b>{correlation:.2f}</b>,
    which indicates <b>{relation_text}</b>.
    This helps users understand whether highly rated movies are also highly popular.
</div>
""", unsafe_allow_html=True)

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
# Movie Mood Explorer
# =========================

st.markdown(
    '<div class="section-title">Movie Mood Explorer</div>',
    unsafe_allow_html=True
)

mood = st.radio(
    "Select a Mood",
    ["Exciting", "Emotional", "Tense", "Imaginative", "Warm"],
    horizontal=True
)

mood_map = {
    "Exciting": ["Action", "Sci-Fi"],
    "Emotional": ["Drama", "Romance"],
    "Tense": ["Horror", "Drama"],
    "Imaginative": ["Sci-Fi", "Animation"],
    "Warm": ["Romance", "Animation"]
}

mood_description = {
    "Exciting": "High-energy movies with action, adventure, and excitement.",
    "Emotional": "Character-driven stories that focus on relationships and feelings.",
    "Tense": "Suspenseful and thrilling movies that create tension.",
    "Imaginative": "Creative worlds filled with fantasy, science fiction, and imagination.",
    "Warm": "Comforting and uplifting stories that create a positive feeling."
}

st.markdown(f"""
<div class="insight-card">
<b>{mood}</b><br><br>
{mood_description[mood]}
</div>
""", unsafe_allow_html=True)

recommended = filtered_df[
    filtered_df["Genre"].isin(mood_map[mood])
].sort_values(
    ["Rating", "Popularity"],
    ascending=False
)

st.markdown("### Recommended Movies")

st.dataframe(
    recommended[
        ["Movie", "Genre", "Country", "Year", "Rating", "Popularity"]
    ],
    use_container_width=True,
    hide_index=True
)

# =========================
# Key Takeaways
# =========================
st.markdown('<div class="section-title">Key Takeaways</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-card">
    This dashboard connects movie data with audience interpretation.
    Through filters, charts, poster browsing, and mood-based discovery,
    users can explore how genre, rating, popularity, country, and emotion shape the movie-viewing experience.
</div>
""", unsafe_allow_html=True)

st.caption("Final Project | Streamlit Dashboard | Movie Genre & Audience Trends Dashboard")
