import Keys
from typing import Any, Dict, List

def get_sentiment_map(sentiment: List[Dict[str, Any]]) -> None:
        sentiment_map = {e["name"]: e["score"] for e in sentiment}
        return sentiment_map

import asyncio
import time
import traceback

from hume import HumeStreamClient
from hume.models.config import LanguageConfig


def get_sentiment_from_article (text):
    sentiments = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    text_example = text
    async def main():
        try:
            client = HumeStreamClient(Keys.hume_api_key)
            config = LanguageConfig(sentiment={})
            async with client.connect([config]) as socket:
                result = await socket.send_text(text_example)
                sent_map = get_sentiment_map(result["language"]["predictions"][0]["sentiment"])
                for i in range(1, 10):
                    sentiments[i] += sent_map[str(i)]
        except Exception:
            print(traceback.format_exc())
            
    asyncio.run(main())

    return_sentiments = {"Extremely Negative": sentiments[1], 
        "Very Negative": sentiments[2],
        "Slightly Negative": sentiments[3],
        "Negative": sentiments[4],
        "Neutral": sentiments[5],
        "Slightly Positive": sentiments[6],
        "Positive": sentiments[7],
        "Very Postive": sentiments[8], 
        "Extremely Positive": sentiments[9]
    }
    return return_sentiments

#print(get_sentiment_from_article("President Obama called Wednesday on Congress to extend a tax break for students included in last year's economic stimulus package, arguing that the policy provides more generous assistance. The American Opportunity Tax Credit program, which will cost $58 billion over a decade, is due to expire at the end of this year. In a statement to reporters in the White House Rose Garden, Obama said the tax breaks help make a college education more affordable for Americans. 'I am calling on Congress to make this tax credit permanent,"))