import taipy as tp
from taipy import Config, Core, Gui
from Main.py import main



def main0(str):
    return main(str)[0]

def main2(str):
    return main(str)[1]

def main3(str):
    return main(str)[2]

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

input_topic = "Taipy"
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
<|{Summary[0]}|text|>
<|{Summary[1]}|text|>
<|{Summary[2]}|text|>

sentiment:
<|{sentiment[0]}|text|>
<|{sentiment[1]}|text|>
<|{sentiment[2]}|text|>

url:
<|{url[0]}|text|>
<|{url[1]}|text|>
<|{url[2]}|text|>
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

    Gui(page).run()
