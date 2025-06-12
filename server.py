# server.py
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from language_model import LanguageClassModel

# Agent display logic
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.8,
        "Color": "green" if agent.language_used == "L2" else "red",
        "Layer": 0,
        "text": str(int(agent.cards)),
        "text_color": "black"
    }
    return portrayal

# Canvas grid
grid = CanvasGrid(agent_portrayal, 5, 5, 500, 500)

# Chart 1: L2 vs L1 Usage (to show opposing behavior clearly)
usage_chart = ChartModule(
    [
        {"Label": "L2_Usage", "Color": "green"},
        {"Label": "L1_Usage", "Color": "red"}
    ],
    data_collector_name='datacollector'
)

# Chart 2: Motivation, Anxiety, Cards, and Low Card Students
stats_chart = ChartModule(
    [
        {"Label": "Avg_Cards", "Color": "blue"},
        {"Label": "Low_Card_Students", "Color": "orange"},
        {"Label": "Avg_Motivation", "Color": "purple"},
        {"Label": "Avg_Anxiety", "Color": "brown"},
    ],
    data_collector_name='datacollector'
)

# Interactive sliders
model_params = {
    "N": UserSettableParameter("slider", "Number of Students", 25, 5, 50, 1),
    "width": 5,
    "height": 5,
    "max_steps": UserSettableParameter("slider", "Max Steps", 50, 10, 200, 10),
    "initial_motivation": UserSettableParameter("slider", "Initial Motivation (avg)", 0.65, 0.1, 1.0, 0.05),
    "initial_anxiety": UserSettableParameter("slider", "Initial Anxiety (avg)", 0.3, 0.1, 1.0, 0.05),
    "peer_influence": UserSettableParameter("slider", "Peer Pressure Weight", 0.4, 0.0, 1.0, 0.1),
    "card_weight": UserSettableParameter("slider", "Card Effect Weight", 0.7, 0.0, 1.5, 0.1)
}

# Server setup
server = ModularServer(
    LanguageClassModel,
    [grid, usage_chart, stats_chart],
    "Language Learning Classroom Simulation",
    model_params
)

server.port = 8521
server.launch()
