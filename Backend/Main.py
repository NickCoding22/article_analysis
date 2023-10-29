import Backend
import Parser
import SentimentAnalysis

# Returns the sentiment
def main (url):
    sent = SentimentAnalysis.get_sentiment_from_article(Parser.parse_website(url))
    summary = Backend.analyze_website_LLM(url)["main points"]
    return [url, sent, summary]

# print(main("https://www.sfchronicle.com/bayarea/article/sf-city-college-revive-18417567.php"))