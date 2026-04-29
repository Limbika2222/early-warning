class SymptomExtractionService:
    def __init__(self):
        self.symptoms = [
            "fever",
            "cough",
            "headache",
            "fatigue",
            "nausea",
            "vomiting",
            "diarrhea",
            "dizziness",
            "pain",
            "rash",
            "chills",
            "sore throat"
        ]

    def extract_symptoms(self, text):
        text = text.lower()

        found = []

        for symptom in self.symptoms:
            if symptom in text:
                found.append(symptom)

        return list(set(found))

    def process_posts(self, posts):
        results = []

        for post in posts:
            content = f"{post.get('title', '')} {post.get('text', '')}"

            symptoms = self.extract_symptoms(content)

            if symptoms:
                results.append({
                    "date": post.get("created_date"),
                    "symptoms": symptoms,
                    "subreddit": post.get("subreddit")
                })

        return results