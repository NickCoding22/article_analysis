import Backend
import Parser
import SentimentAnalysis

# Returns the sentiment
def main (url):
    sent = SentimentAnalysis.get_sentiment_from_article(Parser.parse_website(url))
    final_sent = 0
    for s in sent.keys():
        if sent[s] > final_sent:
            final_sent = sent[s]
        
    summary = Backend.analyze_website_LLM(url)["main points"]
    return [url, final_sent, summary]

# print(main("https://www.sfchronicle.com/bayarea/article/sf-city-college-revive-18417567.php"))