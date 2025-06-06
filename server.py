from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from language_model import LanguageClassModel, agent_portrayal

# Set up the agent display grid
grid = CanvasGrid(agent_portrayal, 5, 5, 500, 500)

# Set up the live charts for key metrics
chart = ChartModule([
    {"Label": "L2_Usage", "Color": "green"},
    {"Label": "Avg_Level", "Color": "blue"},
    {"Label": "Card_Inequality", "Color": "red"},
])

# Launch the interactive browser-based server
server = ModularServer(
    LanguageClassModel,
    [grid, chart],
    "L2CardSim: Peer-Based Language Practice Model",
    {"N": 25, "width": 5, "height": 5}
)

server.port = 8521  # Optional: can change if needed
server.launch()
