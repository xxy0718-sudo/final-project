import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Cinema Analytics Platform",
    page_icon="🎬",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');

html, body, [class*="css"]{
    font-family: 'Poppins', sans-serif;
}

/* BACKGROUND */

.stApp{

    background:
    linear-gradient(
        rgba(0,0,0,0.88),
        rgba(0,0,0,0.95)
    ),

    url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070&auto=format&fit=crop");

    background-size:cover;
    background-position:center;
    background-attachment:fixed;

    color:white;
}

/* REMOVE STREAMLIT STYLE */

header{
    visibility:hidden;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* HERO */

.hero-title{

    text-align:center;

    font-size:90px;

    font-weight:900;

    letter-spacing:8px;

    margin-top:50px;

    color:white;

    text-shadow:
    0 0 20px rgba(255,255,255,0.3),
    0 0 40px rgba(229,9,20,0.4);
}

.hero-subtitle{

    text-align:center;

    font-size:24px;

    color:#d1d5db;

    margin-bottom:60px;
}

/* SECTION TITLE */

.section-title{

    font-size:42px;

    font-weight:700;

    margin-top:40px;
    margin-bottom:25px;

    color:white;

    border-left:6px solid #E50914;

    padding-left:15px;
}

/* MOVIE CARD */

.movie-card{

    background:rgba(20,20,20,0.72);

    backdrop-filter:blur(14px);

    border:1px solid rgba(255,255,255,0.08);

    border-radius:22px;

    overflow:hidden;

    transition:0.4s;

    margin-bottom:30px;
}

.movie-card:hover{

    transform:
    translateY(-10px)
    scale(1.02);

    box-shadow:
    0 0 35px rgba(229,9,20,0.35);
}

.movie-title{

    font-size:28px;

    font-weight:700;

    margin-top:15px;
}

.movie-info{

    color:#d1d5db;

    margin-bottom:10px;
}

/* SEARCH */

.stTextInput input{

    background:rgba(255,255,255,0.08);

    color:white;

    border-radius:12px;

    border:1px solid rgba(255,255,255,0.15);

    padding:12px;
}

/* BUTTON */

.stButton button{

    background:#E50914;

    color:white;

    border:none;

    border-radius:12px;

    padding:12px 25px;

    font-size:16px;

    font-weight:600;

    transition:0.3s;
}

.stButton button:hover{

    background:#ff1f2f;

    transform:scale(1.03);
}

/* METRIC */

[data-testid="metric-container"]{

    background:rgba(20,20,20,0.72);

    border:1px solid rgba(255,255,255,0.08);

    padding:20px;

    border-radius:18px;

    backdrop-filter:blur(10px);
}

/* DATAFRAME */

[data-testid="stDataFrame"]{

    background:rgba(20,20,20,0.72);

    border-radius:18px;
}

</style>

""", unsafe_allow_html=True)

# ------------------------------------------------
# HERO SECTION
# ------------------------------------------------

st.markdown(
    '<div class="hero-title">CINEMA ANALYTICS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">Movie Trends • Audience Insights • Interactive Cinema Experience</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------
# DATA
# ------------------------------------------------

data = {

    "Movie":[
        "Inception",
        "Interstellar",
        "Parasite",
        "Joker",
        "Avengers Endgame",
        "The Batman",
        "La La Land",
        "Dune"
    ],

    "Genre":[
        "Sci-Fi",
        "Sci-Fi",
        "Drama",
        "Drama",
        "Action",
        "Action",
        "Romance",
        "Sci-Fi"
    ],

    "Rating":[
        8.8,
        8.7,
        8.5,
        8.4,
        8.3,
        8.1,
        8.0,
        8.2
    ],

    "Popularity":[
        95,
        92,
        90,
        89,
        98,
        86,
        80,
        91
    ]
}

df = pd.DataFrame(data)

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("🎬 Filter Movies")

genre = st.sidebar.multiselect(
    "Select Genre",
    df["Genre"].unique(),
    default=df["Genre"].unique()
)

filtered_df = df[df["Genre"].isin(genre)]

# ------------------------------------------------
# METRICS
# ------------------------------------------------

st.markdown(
    '<div class="section-title">Now Showing</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Movies", len(filtered_df))

with col2:
    st.metric(
        "Average Rating",
        round(filtered_df["Rating"].mean(),1)
    )

with col3:
    st.metric(
        "Average Popularity",
        round(filtered_df["Popularity"].mean(),1)
    )

# ------------------------------------------------
# SEARCH
# ------------------------------------------------

st.markdown(
    '<div class="section-title">Search Movies</div>',
    unsafe_allow_html=True
)

search = st.text_input("🔍 Search Movie")

search_button = st.button("Search")

if search_button and search:

    search_df = filtered_df[
        filtered_df["Movie"].str.contains(search, case=False)
    ]

else:

    search_df = filtered_df

# ------------------------------------------------
# MOVIE POSTERS
# ------------------------------------------------

st.markdown(
    '<div class="section-title">Trending Cinema</div>',
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
        "title":"Interstellar",
        "image":"https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "rating":"8.7",
        "genre":"Sci-Fi"
    },

    {
        "title":"Parasite",
        "image":"https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
        "rating":"8.5",
        "genre":"Drama"
    },

    {
        "title":"Joker",
        "image":"https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
        "rating":"8.4",
        "genre":"Drama"
    }
]

filtered_movies = []

if search_button and search:

    for movie in movies:

        if search.lower() in movie["title"].lower():

            filtered_movies.append(movie)

else:

    filtered_movies = movies

cols = st.columns(4)

for index, movie in enumerate(filtered_movies):

    with cols[index % 4]:

        st.markdown('<div class="movie-card">', unsafe_allow_html=True)

        st.image(movie["image"])

        st.markdown(
            f'<div class="movie-title">{movie["title"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="movie-info">⭐ Rating: {movie["rating"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="movie-info">🎬 Genre: {movie["genre"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------
# CHARTS
# ------------------------------------------------

st.markdown(
    '<div class="section-title">Audience Analytics</div>',
    unsafe_allow_html=True
)

chart1, chart2 = st.columns(2)

with chart1:

    fig = px.bar(
        filtered_df,
        x="Movie",
        y="Rating",
        color="Genre",
        title="Movie Ratings"
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

with chart2:

    fig2 = px.pie(
        filtered_df,
        names="Genre",
        title="Genre Distribution"
    )

    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------
# DATA TABLE
# ------------------------------------------------

st.markdown(
    '<div class="section-title">Movie Database</div>',
    unsafe_allow_html=True
)

st.dataframe(search_df)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align:center;color:gray;padding-bottom:30px;'>
    © 2026 Cinema Analytics Platform
    </div>
    """,
    unsafe_allow_html=True
)
