from hume import HumeBatchClient
from hume.models.config import LanguageConfig
from hume.models.config import NerConfig

from typing import Any, Dict, List

import Keys

def get_sentiment_from_article(full_text):

    f = open("article.txt", "w")
    f.write(full_text)
    f.close()

    def get_sentiment_map(sentiment: List[Dict[str, Any]]) -> None:
        sentiment_map = {e["name"]: e["score"] for e in sentiment}
        return sentiment_map

    client = HumeBatchClient(Keys.hume_api_key)
    #urls = ["https://storage.googleapis.com/hume-test-data/text/happy.txt"]
    config = LanguageConfig(sentiment={})
    #job = client.submit_job(urls, [config])
    files = ["article.txt"]
    #config = NerConfig()
    job = client.submit_job([], [config], files=files)

    print("Running...", job)

    job.await_complete()
    print("Job completed with status: ", job.get_status())

    full_predictions = job.get_predictions()
    sentiments = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total = 0
    for source in full_predictions:
        #source_name = source["source"]["url"]
        #if "results" in source.keys():
        #    if "predictions" in source["results"].keys():
        predictions = source["results"]["predictions"]
        for prediction in predictions:
            language_predictions = prediction["models"]["language"]["grouped_predictions"]
            for language_prediction in language_predictions:
                for chunk in language_prediction["predictions"]:
                    sent_map = get_sentiment_map(chunk["sentiment"])
                    for i in range(1, 10):
                        sentiments[i] += sent_map[str(i)]
                    total += 1
    for i in range(1, 10):
        sentiments[i] = sentiments[i] / total
    print(sentiments[1:])
    return(sentiments[1:])

get_sentiment_from_article("Hey")