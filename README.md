# Spotify Hits Dashboard — What Makes a Song Go Viral?

## Step 1: Dataset and Decision-Maker

**Dataset:** Global Spotify Hits — Song Longevity & Audio Dynamics (2018–2026)
- 1,200 charting tracks, three CSVs joined by `track_id`: track metadata, audio features, chart longevity.
- Columns: genre, release date, BPM, danceability, energy, valence, peak chart rank, weeks on chart, total streams, and an `is_viral_hit` flag.
- Source: Kaggle snapshot, 2018–2026.

**Decision-maker:** An A&R (Artist & Repertoire) manager at a record label.
They decide which new songs to sign, which artists to push, and how to spend promotion budget.

## Step 2: Why a Dashboard?

1. **Who looks, how often?** The A&R manager reviews this weekly when planning the next quarter's promotion slate.
2. **What decision does it support?** If a new track's audio profile (danceability, energy, genre) matches past viral hits, the manager allocates more playlist-promotion budget to it.
3. **What do they do today?** They rely on gut feel and a few known hit examples, which means they either over-invest in proven genres or miss surprises.
4. **Why a dashboard?** The same question ("which songs have the viral profile?") comes up every week for every new release. A weekly report would lag; a live dashboard lets them compare a new demo against historical hits immediately.

## Step 3: What We Show (and What We Cut)

**Three KPI cards (top):**
- Tracks in view — how many songs match the current filter.
- Viral hit rate — share of tracks that went viral, the number the manager cares about.
- Total streams (M) — overall scale.

**Two supporting charts:**
- *Viral hit rate by genre* — which genres historically produce viral hits most often.
- *Danceability vs. Energy scatter* — visualizes the audio "shape" of viral songs (green) vs. non-viral (gray), so the manager can see where a new demo would land.

**Filters:** Genre multi-select + release-year slider. These are the two cuts an A&R actually makes.

**Two things we chose NOT to show:**
- *Musical key and mode* — interesting for music theorists, but a major/minor key doesn't change a promotion decision.
- *Liveness and acousticness* — looked varied in EDA, but viral hits span the whole range; adding them would add noise without changing the decision.

**Misleading-data note:** `is_viral_hit` is a binary flag supplied in the dataset, not a real label from Spotify. The dashboard uses it as a teaching proxy; in production, "viral" would be defined by weeks-on-chart or stream velocity thresholds.

**Page order:** KPIs first (is anything off right now?), then the genre bar chart (which genres win), then the scatter (what audio profile wins), then the data-period footnote.

## Step 4: Refresh Frequency

- **Data refresh:** Streaming numbers update daily from Spotify in production. Real-time is unnecessary because promotion decisions are made weekly, not by the minute.
- **Manager review:** Weekly, on Mondays when planning the week's playlist pushes.
- **Trigger for action:** If a newly released song's first-week stream velocity exceeds the 90th percentile of past viral hits, the A&R manager should call the promotion team the same day — this becomes an alert, not a dashboard check.
- **Cost of stale data:** A one-day delay is fine for weekly planning; a one-week delay means the label wastes promotion budget on songs that have already faded.

*This snapshot: 2018–2026, 1,200 tracks. Production refresh: daily. Review: weekly.*

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
