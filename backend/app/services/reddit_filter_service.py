import re


class RedditFilterService:
    def __init__(self):

        # ✅ strong symptom signals
        self.symptom_terms = [
            "fever", "temperature", "cough", "headache",
            "fatigue", "pain", "sore throat", "chills",
            "nausea", "vomiting", "diarrhea", "dizziness",
            "infection", "rash", "swelling", "breathing"
        ]

        # ✅ strong medical context
        self.medical_terms = [
            "doctor", "hospital", "medicine", "diagnosed",
            "treatment", "prescribed", "infection",
            "test", "symptoms", "antibiotic"
        ]

        # ✅ personal health patterns (VERY IMPORTANT)
        self.personal_patterns = [
            r"\bi have\b",
            r"\bi feel\b",
            r"\bi've been\b",
            r"\bmy (son|daughter|baby|husband|wife)\b",
            r"\bsuffering from\b",
            r"\bhaving (a )?(fever|cough|pain)\b"
        ]

        # ❌ strong noise / NSFW / irrelevant subs
        self.blocked_subreddits = [
            "dirtyconfessiondesi",
            "18above_roleplay",
            "nsfw",
            "onlyfans",
            "sex",
            "porn"
        ]

        # ❌ misleading phrases
        self.false_positive_phrases = [
            "fever dream",
            "indiana fever",
            "cabin fever",
            "jungle fever"
        ]

        # ❌ weak-context words (filter these OUT unless strong signal exists)
        self.weak_context_terms = [
            "cologne", "game", "fan", "discount", "promo"
        ]

    def contains_symptoms(self, text):
        text = text.lower()
        return [term for term in self.symptom_terms if term in text]

    def has_medical_context(self, text):
        text = text.lower()
        return any(term in text for term in self.medical_terms)

    def has_personal_context(self, text):
        text = text.lower()
        return any(re.search(pattern, text) for pattern in self.personal_patterns)

    def is_false_positive(self, text):
        text = text.lower()
        return any(term in text for term in self.false_positive_phrases)

    def is_blocked_subreddit(self, subreddit):
        return subreddit.lower() in self.blocked_subreddits

    def has_weak_context(self, text):
        text = text.lower()
        return any(term in text for term in self.weak_context_terms)

    def filter_posts(self, posts):
        filtered = []

        for post in posts:
            title = post.get("title", "") or ""
            text = post.get("text", "") or ""
            subreddit = post.get("subreddit", "") or ""

            content = f"{title} {text}".lower()

            # ❌ block bad subreddits
            if self.is_blocked_subreddit(subreddit):
                continue

            # ❌ remove misleading phrases
            if self.is_false_positive(content):
                continue

            symptoms_found = self.contains_symptoms(content)

            # ✅ must have at least 1 symptom
            if len(symptoms_found) == 0:
                continue

            # ✅ strong signal conditions:
            strong_signal = (
                len(symptoms_found) >= 2 or
                (len(symptoms_found) >= 1 and self.has_medical_context(content)) or
                self.has_personal_context(content)
            )

            if not strong_signal:
                continue

            # ❌ remove weak-context posts (like cologne example)
            if self.has_weak_context(content) and len(symptoms_found) < 2:
                continue

            filtered.append(post)

        return filtered