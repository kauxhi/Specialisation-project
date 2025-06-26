import feedparser
from newspaper import Article
from datetime import datetime

# ------------------------------
# 🔧 ADMIN CONFIGURATION
# ------------------------------
config = {
    "is_active": True,
    "keywords": ["startup", "EV", "funding", "AI", "mobility"],
    "locations": {
        "bengaluru": ["bengaluru", "bangalore"],
        "india": ["mumbai", "delhi", "chennai", "hyderabad", "pune", "india"]
    },
    "rss_feeds": [
        "https://news.google.com/rss/search?q=bengaluru+startup",
        "https://news.google.com/rss/search?q=india+startup",
        "https://news.google.com/rss/search?q=global+startup"
    ]
}
# ------------------------------
# 🧠 CLASSIFY NEWS LOCATION
# ------------------------------
def classify_location(text):
    text = text.lower()
    for city in config["locations"]["bengaluru"]:
        if city in text:
            return "Bengaluru"
    for city in config["locations"]["india"]:
        if city in text:
            return "India"
    return "Global"

# ------------------------------
# 🖼️ EXTRACT IMAGE FROM ARTICLE
# ------------------------------
def extract_image(link):
    try:
        article = Article(link)
        article.download()
        article.parse()
        return article.top_image
    except:
        return ""

# ------------------------------
# 📡 FETCH & GENERATE HTML CARDS
# ------------------------------
def fetch_and_generate_html():
    if not config["is_active"]:
        print("⚠️ Bot is deactivated by admin.")
        return

    cards = []

    for feed_url in config["rss_feeds"]:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.summary
            link = entry.link
            pub_date = entry.get("published", datetime.now().strftime("%Y-%m-%d"))

            combined_text = f"{title} {summary}".lower()
            if any(k.lower() in combined_text for k in config["keywords"]):
                location = classify_location(combined_text)
                image = extract_image(link)
                cards.append(generate_card(title, summary, link, image, location, pub_date))

    save_html(cards)

# ------------------------------
# 🎨 GENERATE HTML CARD
# ------------------------------
def generate_card(title, summary, link, image, location, date):
    return f"""
    <div class="news-card">
        <img src="{image}" alt="News image" class="news-image">
        <div class="news-content">
            <h3>{title}</h3>
            <p>{summary}</p>
            <a href="{link}" target="_blank">Read more</a>
            <div class="meta">
                <span class="tag">📍 {location}</span>
                <span class="date">🗓️ {date}</span>
            </div>
        </div>
    </div>
    """

# ------------------------------
# 💾 SAVE HTML PAGE
# ------------------------------
def save_html(cards):
    with open("news_feed.html", "w", encoding="utf-8") as f:
        f.write("""
        <html>
        <head>
        <meta charset="UTF-8">
        <title>Startup News Feed</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f4f4f4; }
            .news-card { background: white; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; margin: 20px 0; display: flex; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            .news-image { width: 200px; height: auto; object-fit: cover; }
            .news-content { padding: 20px; flex: 1; }
            .news-content h3 { margin: 0 0 10px; font-size: 20px; color: #333; }
            .news-content p { font-size: 14px; color: #555; }
            .news-content a { display: inline-block; margin-top: 10px; color: #007BFF; text-decoration: none; }
            .meta { margin-top: 10px; font-size: 13px; color: #777; }
            .tag { background: #e0e0e0; padding: 2px 6px; border-radius: 4px; margin-right: 10px; }
        </style>
        </head>
        <body>
        <h2>📰 AutoBot - Latest Tech & Startup News</h2>
        """)
        for card in cards:
            f.write(card)
        f.write("</body></html>")
    print("✅ HTML feed saved as: news_feed.html")

# ------------------------------
# ▶️ MAIN EXECUTION
# ------------------------------
if __name__ == "__main__":
    fetch_and_generate_html()
