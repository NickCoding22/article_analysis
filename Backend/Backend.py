#https://docs.taipy.io/en/latest/knowledge_base/demos/image_classif/
import together
import Parser as parser
together.api_key = "xxxxxx"

def analyze_website_LLM(website_url): 
    article_paragraph = ""
    five_key_points = ""

    #article_paragraph = parser.parse_website("https://www.sfchronicle.com/bayarea/article/sf-city-college-revive-18417567.php");
    #article_paragraph = parser.parse_website("https://www.defense.gov/News/News-Stories/Article/Article/3570190/dod-announces-up-to-150m-in-aid-for-ukraine/")
    article_paragraph = parser.parse_website(website_url)
    prompt_request = "Summarize the following article in 3 sentences: [" + article_paragraph + "]"

    output = together.Complete.create(
        prompt = prompt_request,
        model = "togethercomputer/llama-2-7b-chat", 
        max_tokens = 256,
        temperature = 0.7,
        top_k = 50,
        top_p = 0.7,
        repetition_penalty = 1
    )


    five_key_points = output['output']['choices'][0]['text']
    # print(five_key_points)
    return {"article paragraph": article_paragraph, "main points": five_key_points}