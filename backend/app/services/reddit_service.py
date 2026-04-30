import requests
import time
import random
from datetime import datetime, timedelta


class RedditService:
    BASE_URL = "https://api.pullpush.io/reddit/search/submission/"
    # 🔥 GLOBAL CACHE
    _cached_posts = None
    _last_update_time = None

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        })

        # 🔥 persistent state
        self.posts = []
        self.daily_cache = {}   # 🔒 LOCKED DATA PER DAY
        self.last_update = None

    def _generate_realistic_posts(self):
        now = datetime.utcnow()
        base_date = now - timedelta(days=6)
        all_posts = []
        daily_cache = {}
        for i in range(7):
            date_obj = base_date + timedelta(days=i)
            date_str = date_obj.strftime("%Y-%m-%d")
            daily_posts = []
            num_posts = i + 2
            for _ in range(num_posts):
                symptoms = self._generate_symptoms(i)
                post = self._generate_post(symptoms, date_obj)
                daily_posts.append(post)
            daily_cache[date_str] = daily_posts
        
        for posts in daily_cache.values():
            all_posts.extend(posts)
            
        return all_posts[-100:]

    # -------------------------------------------------
    # 🔹 API FETCH (UNCHANGED)
    # -------------------------------------------------
    def fetch_pullpush(self, keyword, limit=50):
        for days in [7, 30, 90]:
            try:
                now = datetime.utcnow()
                past = now - timedelta(days=days)

                params = {
                    "q": keyword,
                    "size": limit,
                    "sort": "desc",
                    "sort_type": "created_utc",
                    "after": int(past.timestamp())
                }

                response = self.session.get(self.BASE_URL, params=params, timeout=15)

                if response.status_code != 200:
                    continue

                data = response.json()
                posts = data.get("data", [])

                if posts:
                    return self._format_posts(posts)

            except Exception:
                continue

        return []

    def fetch_reddit_json(self, keyword, limit=25):
        try:
            url = f"https://www.reddit.com/search.json?q={keyword}&limit={limit}"

            response = requests.get(url, headers=self.session.headers, timeout=10)

            if response.status_code != 200:
                return []

            data = response.json()

            posts = []
            for item in data.get("data", {}).get("children", []):
                post = item.get("data", {})
                created = post.get("created_utc", 0)

                posts.append({
                    "id": post.get("id"),
                    "title": post.get("title", ""),
                    "text": post.get("selftext", "") or "",
                    "created_utc": created,
                    "created_date": datetime.utcfromtimestamp(created).strftime('%Y-%m-%d') if created else None,
                    "subreddit": post.get("subreddit", ""),
                    "score": post.get("score", 0),
                    "num_comments": post.get("num_comments", 0),
                    "url": post.get("url")
                })

            return posts

        except Exception:
            return []

    def _format_posts(self, posts_data):
        formatted = []

        for post in posts_data:
            try:
                created_utc = post.get("created_utc", 0)

                formatted.append({
                    "id": post.get("id"),
                    "title": post.get("title", ""),
                    "text": post.get("selftext", "") or "",
                    "created_utc": created_utc,
                    "created_date": datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d') if created_utc else None,
                    "subreddit": post.get("subreddit", ""),
                    "score": post.get("score", 0),
                    "num_comments": post.get("num_comments", 0),
                    "url": post.get("full_link") or post.get("url")
                })

            except Exception:
                continue

        return formatted

    # -------------------------------------------------
    # 🔥 MAIN METHOD
    # -------------------------------------------------
    def fetch_health_signals(self):
        from datetime import datetime, timedelta

        now = datetime.utcnow()

        # ---------------------------------
        # FIRST LOAD → GENERATE DATA
        # ---------------------------------
        if RedditService._cached_posts is None:
            RedditService._cached_posts = self._generate_realistic_posts()
            RedditService._last_update_time = now
            return RedditService._cached_posts

        # ---------------------------------
        # CONTROLLED UPDATE (ONLY EVERY 30 MIN)
        # ---------------------------------
        if RedditService._last_update_time and now - RedditService._last_update_time < timedelta(minutes=30):
            return RedditService._cached_posts

        # ---------------------------------
        # UPDATE ONLY MOST RECENT DATE
        # ---------------------------------
        latest_date = max(post["created_date"] for post in RedditService._cached_posts)

        updated_posts = []

        for post in RedditService._cached_posts:
            if post["created_date"] == latest_date:
                # small variation
                post["text"] += ""  # (you can later randomize slightly)
            updated_posts.append(post)

        RedditService._cached_posts = updated_posts
        RedditService._last_update_time = now

        return RedditService._cached_posts

    # -------------------------------------------------
    # 🔥 STABLE SIMULATION (FIXED VERSION)
    # -------------------------------------------------
    def _stable_simulation(self):
        now = datetime.utcnow()

        # 🔒 ONLY UPDATE EVERY 30 MINUTES
        if self.last_update and (now - self.last_update).seconds < 1800:
            return self.posts

        self.last_update = now

        base_date = now - timedelta(days=6)

        # 🔥 GENERATE DATA PER DAY (LOCKED)
        for i in range(7):
            date_obj = base_date + timedelta(days=i)
            date_str = date_obj.strftime("%Y-%m-%d")

            # 🔒 DO NOT CHANGE EXISTING DAY
            if date_str in self.daily_cache:
                continue

            daily_posts = []

            # 🔥 controlled outbreak growth
            num_posts = i + 2

            for _ in range(num_posts):
                symptoms = self._generate_symptoms(i)
                post = self._generate_post(symptoms, date_obj)
                daily_posts.append(post)

            self.daily_cache[date_str] = daily_posts

        # 🔥 FLATTEN DATA
        all_posts = []
        for posts in self.daily_cache.values():
            all_posts.extend(posts)

        # 🔥 LIMIT SIZE
        self.posts = all_posts[-100:]

        return self.posts

    # -------------------------------------------------
    # 🧠 SYMPTOM PROGRESSION
    # -------------------------------------------------
    def _generate_symptoms(self, day_index):
        if day_index < 2:
            return random.choice([
                ["mild fever"],
                ["headache"],
                ["fatigue"]
            ])

        elif day_index < 4:
            return random.choice([
                ["fever", "fatigue"],
                ["cough", "fever"],
                ["headache", "fatigue"]
            ])

        else:
            return random.choice([
                ["high fever", "chills"],
                ["fever", "cough", "fatigue"],
                ["body pain", "fever"]
            ])

    # -------------------------------------------------
    # 💬 REALISTIC POSTS
    # -------------------------------------------------
    def _generate_post(self, symptoms, date):
        templates = [
            "I've had {symptoms} for a few days",
            "Anyone else experiencing {symptoms}?",
            "Should I be worried about {symptoms}?",
            "This started with {symptoms} and is getting worse",
            "Feeling really bad with {symptoms}",
        ]

        descriptions = [
            "It's getting worse.",
            "I can barely move.",
            "Thinking of seeing a doctor.",
            "No idea what's going on.",
        ]

        symptom_text = " and ".join(symptoms)

        return {
            "id": f"sim_{random.randint(100000,999999)}",
            "title": random.choice(templates).format(symptoms=symptom_text),
            "text": random.choice(descriptions),
            "created_utc": int(date.timestamp()),
            "created_date": date.strftime('%Y-%m-%d'),
            "subreddit": random.choice(["AskDocs", "Health"]),
            "score": random.randint(1, 50),
            "num_comments": random.randint(0, 20),
            "url": ""
        }