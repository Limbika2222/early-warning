import requests
import time
from datetime import datetime, timedelta


class RedditService:
    BASE_URL = "https://api.pullpush.io/reddit/search/submission/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
        })

    def fetch_posts_by_keyword(self, keyword="fever", limit=50):
        """
        Fetch Reddit posts with fallback time windows
        """

        for days in [7, 30, 90]:
            try:
                now = datetime.utcnow()
                past = now - timedelta(days=days)
                after_timestamp = int(past.timestamp())

                params = {
                    "q": keyword,
                    "size": limit,
                    "sort": "desc",
                    "sort_type": "created_utc",
                    "after": after_timestamp
                }

                response = self.session.get(
                    self.BASE_URL,
                    params=params,
                    timeout=15
                )

                if response.status_code != 200:
                    print(f"⚠️ API issue ({response.status_code}) for '{keyword}'")
                    continue

                try:
                    data = response.json()
                except Exception:
                    print(f"⚠️ Invalid JSON for '{keyword}'")
                    continue

                posts = data.get("data", [])

                if posts:
                    print(f"✅ Found {len(posts)} posts for '{keyword}' (last {days} days)")
                    return self._format_posts(posts)

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Network error for '{keyword}': {e}")

        print(f"⚠️ No usable data for '{keyword}' (API limitation)")
        return []

    def _format_posts(self, posts_data):
        formatted = []

        for post in posts_data:
            try:
                created_utc = post.get("created_utc", 0)

                formatted.append({
                    "id": post.get("id"),
                    "title": post.get("title", "") or "",
                    "text": post.get("selftext", "") or "",
                    "created_utc": created_utc,
                    "created_date": datetime.utcfromtimestamp(
                        created_utc
                    ).strftime('%Y-%m-%d') if created_utc else None,
                    "subreddit": post.get("subreddit", ""),
                    "score": post.get("score", 0),
                    "num_comments": post.get("num_comments", 0),
                    "url": post.get("full_link") or post.get("url")
                })

            except Exception as e:
                print(f"⚠️ Error formatting post: {e}")
                continue

        return formatted

    def _fallback_mock_data(self):
        """
        Multi-day fallback WITH spike simulation
        """

        base = datetime.utcnow()

        def make_post(id, title, text, days_ago, subreddit):
            date = base - timedelta(days=days_ago)
            return {
                "id": id,
                "title": title,
                "text": text,
                "created_utc": int(date.timestamp()),
                "created_date": date.strftime('%Y-%m-%d'),
                "subreddit": subreddit,
                "score": 5,
                "num_comments": 2,
                "url": ""
            }

        print("\n⚠️ Using fallback mock data (with spike simulation)")

        return [
            make_post("1", "Mild headache", "small pain", 5, "Health"),
            make_post("2", "Slight fatigue", "a bit tired", 4, "Health"),
            make_post("3", "Fever started", "low fever", 3, "AskDocs"),

            # 🔥 spike day
            make_post("4", "High fever and chills", "very sick", 0, "AskDocs"),
            make_post("5", "Severe fever today", "temperature rising", 0, "medical"),
            make_post("6", "Fever and headache", "painful", 0, "AskDocs"),
            make_post("7", "Child with fever", "very high temp", 0, "Health"),
        ]

    def fetch_health_signals(self):
        """
        Fetch posts using health-related keywords + deduplication
        """

        # 🔥 IMPROVED KEYWORDS (REALISTIC)
        keywords = [
            "fever",
            "cough",
            "flu",
            "headache",
            "fatigue",
            "infection OR infected OR UTI OR wound infection OR bacterial infection"
        ]

        all_posts = []
        seen_ids = set()

        for keyword in keywords:
            try:
                print(f"\n🔍 Fetching keyword: {keyword}")

                posts = self.fetch_posts_by_keyword(keyword, limit=30)

                for post in posts:
                    if post["id"] not in seen_ids:
                        seen_ids.add(post["id"])
                        all_posts.append(post)

                time.sleep(0.5)

            except Exception as e:
                print(f"⚠️ Error fetching '{keyword}': {e}")

        # 🔥 fallback if API fails completely
        if len(all_posts) == 0:
            return self._fallback_mock_data()

        print(f"\n📊 Total unique posts collected: {len(all_posts)}")
        return all_posts