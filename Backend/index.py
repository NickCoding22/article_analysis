import taipy as tp
from taipy import Config, Core, Gui
from Main import main
import SentimentAnalysis
import Parser
import Backend
from taipy import Gui

myTheme  = {
        "palette": {
            "mode": 'dark',
            "primary": {
            "main": '#00a2a2',
            },
            "secondary": {
            "main": '#f50057',
            
            },
            "background": {
            "default": '#121212',
            "paper": '#040404',
            },
        },
        };


def main0(str):
    return str
    

def main2(str1):
    sent = SentimentAnalysis.get_sentiment_from_article(Parser.parse_website(str1))
    final_sent = ''
    negative_total = sent["Extremely Negative"] + sent["Very Negative"] + sent["Slightly Negative"] + sent["Negative"]
    positive_total = sent["Extremely Positive"] + sent["Very Positive"] + sent["Slightly Positive"] + sent["Positive"]
    neg = str(negative_total)[:5]
    pos = str(positive_total)[:5]
    if positive_total > sent["Neutral"] or negative_total > sent["Neutral"]:
        if positive_total > negative_total:
            final_sent = "This article takes a POSITIVE perspective with an index of: " + pos
        else:
            final_sent = "This article takes a NEGATIVE perspective with an index of: " + neg
    else: 
        final_sent = "Neutral."
    print(final_sent,"lokawdwa")
    return final_sent

def main3(str):
    summary = Backend.analyze_website_LLM(str)["main points"]
    print(summary,"summary")
    return summary
    """return "Together API: Down"""

################################################################
# Configure application
################################################################

def build_Summary(topic):
    return main0(topic)

def build_sentiment(topic):
    return main2(topic)

def build_url(topic):
    return main3(topic)

# Data node configurations to model the input topic.
input_topic_data_node_cfg = Config.configure_data_node(id="input_topic")
# Data node configurations to model the Summarys to display.
Summary_data_node_cfg = Config.configure_data_node(id="Summary")
Summary_data_node_cfg2 = Config.configure_data_node(id="sentiment")
Summary_data_node_cfg3 = Config.configure_data_node(id="url")

# Task configurations to model the build_Summary functions.
build_msg_task_cfg = Config.configure_task("build_msg", build_Summary, input_topic_data_node_cfg, Summary_data_node_cfg)
build_msg_task_cfg2 = Config.configure_task("build_msg2", build_sentiment, input_topic_data_node_cfg, Summary_data_node_cfg2)
build_msg_task_cfg3 = Config.configure_task("build_msg3", build_url, input_topic_data_node_cfg, Summary_data_node_cfg3)

# The scenario configuration represents the whole execution graph.
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg, build_msg_task_cfg2, build_msg_task_cfg3])

################################################################
# Design graphical interface
################################################################

input_topic = "https://www.sfchronicle.com/bayarea/article/sf-city-college-revive-18417567.php"
Summary = None
sentiment = None
url = None

def submit_scenario(state):
    state.scenario.input_topic.write(state.input_topic)
    state.scenario.submit()
    state.Summary = state.scenario.Summary.read()
    state.sentiment = state.scenario.sentiment.read()
    state.url = state.scenario.url.read()

page = """
Article Sentiment Comprehenseion (ASC)

Topic:
<|{input_topic}|input|>

<|submit|button|on_action=submit_scenario|>

URL:

<|{Summary}|text|>

Sentiment:
<|{sentiment}|text|>

Summary:
<|{url}|text|>
"""
newGui = Gui(page,css_file = "style.css")


if __name__ == "__main__":
    ################################################################
    # Instantiate and run Core service
    ################################################################
    Core().run()

    ################################################################
    # Manage scenarios and data nodes
    ################################################################
    scenario = tp.create_scenario(scenario_cfg)

    ################################################################
    # Instantiate and run Gui service
    ################################################################
   

    newGui.run(theme = myTheme)
