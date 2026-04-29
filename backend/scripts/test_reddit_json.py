from app.services.reddit_service import RedditService
from app.services.reddit_filter_service import RedditFilterService
from app.services.symptom_extraction_service import SymptomExtractionService
from app.services.time_series_service import TimeSeriesService
from app.services.ewma_service import EWMASignalService


if __name__ == "__main__":
    reddit_service = RedditService()
    filter_service = RedditFilterService()
    extractor = SymptomExtractionService()
    ts_service = TimeSeriesService()
    ewma_service = EWMASignalService()

    print("\n[ Reddit Health Signals Test ]\n")

    # 🔹 Step 1: Fetch posts
    posts = reddit_service.fetch_health_signals()
    print(f"\n📊 Total posts fetched: {len(posts)}")

    # 🔹 Step 2: Filter posts
    filtered_posts = filter_service.filter_posts(posts)
    print(f"🧹 Filtered health posts: {len(filtered_posts)}\n")

    # 🔹 Step 3: Show sample filtered posts
    print("🔍 SAMPLE FILTERED POSTS:\n")

    for i, post in enumerate(filtered_posts[:5], 1):
        print(f"--- HEALTH POST {i} ---")
        print("TITLE:", post.get("title"))
        print("DATE:", post.get("created_date"))
        print("SUBREDDIT:", post.get("subreddit"))
        print("TEXT:", (post.get("text") or "")[:120])
        print("-" * 60)

    # 🔹 Step 4: Extract symptoms
    signals = extractor.process_posts(filtered_posts)

    print(f"\n🧠 Extracted signals: {len(signals)}\n")

    for i, signal in enumerate(signals[:5], 1):
        print(f"--- SIGNAL {i} ---")
        print("DATE:", signal.get("date"))
        print("SYMPTOMS:", signal.get("symptoms"))
        print("SUBREDDIT:", signal.get("subreddit"))
        print("-" * 60)

    # 🔹 Step 5: Generate time series
    time_series = ts_service.generate_time_series(signals)

    # 🔥 CRITICAL FIX: per-symptom timeline with zero-fill
    flattened = ts_service.fill_missing_dates_per_symptom(time_series)

    print("\n📈 TIME SERIES DATA:\n")

    for item in flattened:
        print(item)

    # 🔹 Step 6: EWMA Spike Detection
    alerts = ewma_service.detect_spikes(flattened)

    print("\n🚨 ALERTS:\n")

    if not alerts:
        print("No spikes detected")
    else:
        for alert in alerts:
            print(alert)