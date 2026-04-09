import subprocess
import json

def scrape_tweets(keyword, limit=20):
    tweets = []

    command = [
        "snscrape",
        "--jsonl",
        "--max-results", str(limit),
        "twitter-search",
        keyword
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    for line in result.stdout.splitlines():
        tweet = json.loads(line)
        tweets.append({
            "text": tweet["content"],
            "date": tweet["date"][:10]
        })

    return tweets


if __name__ == "__main__":
    print("Testing scraper...")

    tweets = scrape_tweets("malaria", 10)

    print("Tweets found:", len(tweets))
    for t in tweets:
        print(t)