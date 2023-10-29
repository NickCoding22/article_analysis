import taipy as tp
from taipy import Config, Core, Gui
from Main import main
import SentimentAnalysis
import Parser
import Backend
from taipy import Gui




def main0(str):
    return str
    

def main2(str):
    sent = SentimentAnalysis.get_sentiment_from_article(Parser.parse_website(str))
    final_sent = ''
    negative_total = sent["Extremely Negative"] + sent["Very Negative"] + sent["Slightly Negative"] + sent["Negative"]
    positive_total = sent["Extremely Positive"] + sent["Very Positive"] + sent["Slightly Positive"] + sent["Positive"]
    if positive_total > sent["Neutral"] or negative_total > sent["Neutral"]:
        if positive_total > negative_total:
            final_sent = "Postive: Positive language was roughly " + str(positive_total) + " of the text."
        else:
            final_sent = "Negative: Negative language was roughly " + str(negative_total) + " of the text."
    else: 
        final_sent = "Neutral."
    return final_sent

def main3(str):
    summary = Backend.analyze_website_LLM(str)["main points"]
    return summary

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
Topic:
<|{input_topic}|input|>

<|submit|button|on_action=submit_scenario|>

Summary:
{ .blue-line }

<|{Summary}|text|>

sentiment:
<|{sentiment}|text| classname="option"|>

url:
<|{url}|text| id="my_button"|>
"""

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

    Gui(page=page, pages=None, css_file="style.css", path_mapping={}, env_filename=None, flask=None).run()
