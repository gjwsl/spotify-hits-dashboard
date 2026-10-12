from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Spotify Hits Dashboard",
    page_icon="🎵",
    layout="wide",
)

DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def load_data():
    metadata = pd.read_csv(DATA_DIR / "track_metadata.csv")
    audio = pd.read_csv(DATA_DIR / "audio_features.csv")
    performance = pd.read_csv(DATA_DIR / "chart_longevity_panel.csv")

    df = metadata.merge(audio, on="track_id", validate="one_to_one")
    df = df.merge(performance, on="track_id", validate="one_to_one")
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year
    df["viral_label"] = df["is_viral_hit"].map({1: "Viral hit", 0: "Not viral"})
    return df


df = load_data()

st.title("🎵 Spotify Hits: What Makes a Song Go Viral?")
st.caption(
    "For A&R managers deciding which songs to sign and promote. "
    "If a new track's audio profile matches past viral hits, push it harder."
)

st.sidebar.header("Filters")

years = sorted(df["release_year"].dropna().astype(int).unique().tolist())
year_range = st.sidebar.select_slider(
    "Release year", options=years, value=(min(years), max(years))
)

genres = sorted(df["genre"].dropna().unique().tolist())
selected_genres = st.sidebar.multiselect(
    "Genre", options=genres, default=genres
)

filtered = df[
    df["release_year"].between(year_range[0], year_range[1])
    & df["genre"].isin(selected_genres)
]

st.caption(
    f"Data: {df['release_date'].min():%b %Y} – {df['release_date'].max():%b %Y}, "
    f"{len(df)} tracks · Kaggle snapshot · Production refresh: daily · Review: weekly"
)

if filtered.empty:
    st.warning("No tracks match. Widen the filters.")
    st.stop()

k1, k2, k3 = st.columns(3)
k1.metric("Tracks in view", f"{len(filtered):,}")
k2.metric("Viral hit rate", f"{filtered['is_viral_hit'].mean():.1%}")
k3.metric("Total streams (M)", f"{filtered['total_streams_mil'].sum():,.0f}")

st.divider()

st.subheader("Viral hit rate by genre")
genre_viral = (
    filtered.groupby("genre", as_index=False)
    .agg(viral_rate=("is_viral_hit", "mean"), tracks=("track_id", "count"))
    .sort_values("viral_rate", ascending=True)
)
fig1 = px.bar(
    genre_viral, x="viral_rate", y="genre", orientation="h",
    hover_data={"tracks": True},
    labels={"viral_rate": "Share viral", "genre": ""},
)
fig1.update_layout(margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Danceability vs Energy (green = viral hit)")
fig2 = px.scatter(
    filtered, x="danceability", y="energy",
    color="viral_label",
    color_discrete_map={"Viral hit": "#1DB954", "Not viral": "#cccccc"},
    hover_data={"track_title": True, "genre": True},
    labels={"danceability": "Danceability", "energy": "Energy", "viral_label": ""},
)
fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.caption(
    "Data note: is_viral_hit is a supplied label, not a real Spotify metric. "
    "Genre group sizes differ (Pop 318, K-Pop 59), so compare rates alongside counts. "
    "In production, streaming numbers refresh daily; A&R reviews weekly."
)
