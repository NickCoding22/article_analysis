import Backend
import Parser
import SentimentAnalysis

# Returns the sentiment
def main (url):
    sent = SentimentAnalysis.get_sentiment_from_article(Parser.parse_website(url))
    final_sent = 0
    negative_total = sent["Extremely Negative"] + sent["Very Negative"] + sent["Slightly Negative"] + sent["Negative"]
    positive_total = sent["Extremely Positive"] + sent["Very Positive"] + sent["Slightly Positive"] + sent["Positive"]
    if positive_total > sent["Neutral"] or negative_total > sent["Neutral"]:
        if positive_total > negative_total:
            final_sent = "Postive: Positive language was roughly " + str(positive_total) + " of the text."
        else:
            final_sent = "Negative: Negative language was roughly " + str(negative_total) + " of the text."
    else: 
        final_sent = "Neutral."
        
    summary = Backend.analyze_website_LLM(url)["main points"]
    return [url, final_sent, summary]

# Neutral
# print(main("https://www.sfchronicle.com/bayarea/article/sf-city-college-revive-18417567.php"))
# Neutral 
# print(main("https://www.defense.gov/News/News-Stories/Article/Article/3570190/dod-announces-up-to-150m-in-aid-for-ukraine/"))
# Positive 
# print(main("https://www.washingtonpost.com/opinions/2023/10/26/biden-constraining-israel-drawbacks/"))