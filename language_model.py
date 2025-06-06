# Final Version of L2CardSim: Peer-Based Language Practice Model

import random
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# Mapping of CEFR levels
LEVEL_LABELS = {1: "A1", 2: "A2", 3: "B1", 4: "B2", 5: "C1", 6: "C2"}

class StudentAgent(Agent):
    def __init__(self, unique_id, model, language_level):
        super(StudentAgent, self).__init__(unique_id, model)
        self.language_level = language_level  # 1 (A1) to 6 (C2)
        self.language_used = "L1"
        self.motivation = random.uniform(0.3, 0.8)
        self.memory = 0
        self.cards = 0

    def decide_language(self):
        probability_L2 = min(1.0, self.motivation + 0.1 * self.memory)
        self.language_used = "L2" if random.random() < probability_L2 else "L1"

    def interact(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        others = [a for a in cellmates if a != self]
        if self.language_used == "L2":
            self.cards += 1
            self.memory += 1
        elif self.language_used == "L1":
            self.cards = max(0, self.cards - 1)
            self.memory = max(0, self.memory - 1)

    def improve_language(self):
        if self.language_used == "L2" and random.random() < 0.1:
            if self.language_level < 6:  # Max out at C2
                self.language_level += 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.decide_language()
        self.interact()
        self.improve_language()
        self.move()

class LanguageClassModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.step_count = 0

        self.datacollector = DataCollector(
            agent_reporters={
                "Cards": lambda a: a.cards,
                "Language": lambda a: a.language_used,
                "Level": lambda a: LEVEL_LABELS.get(a.language_level, "Unknown"),
            },
            model_reporters={
                "Avg_Level": self.compute_avg_level,
                "L2_Usage": self.compute_L2_usage,
                "Card_Inequality": self.compute_card_gini,
            }
        )

        for i in range(self.num_agents):
            level = random.choice([1, 2, 3])  # A1 to B1
            agent = StudentAgent(i, self, language_level=level)
            self.schedule.add(agent)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

    def compute_avg_level(self):
        levels = [agent.language_level for agent in self.schedule.agents]
        return sum(levels) / len(levels) if levels else 0

    def compute_L2_usage(self):
        if len(self.schedule.agents) == 0:
            return 0
        l2_users = sum(1 for a in self.schedule.agents if a.language_used == "L2")
        return l2_users / len(self.schedule.agents)

    def compute_card_gini(self):
        cards = [agent.cards for agent in self.schedule.agents]
        if not cards or sum(cards) == 0:
            return 0
        cards.sort()
        n = len(cards)
        cumulative = 0
        for i, x in enumerate(cards, 1):
            cumulative += i * x
        total = sum(cards)
        gini = (2 * cumulative) / (n * total) - (n + 1) / n
        return gini

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.step_count += 1

def agent_portrayal(agent):
    if agent.language_used == "L2":
        color = "green"
    else:
        color = "red"

    portrayal = {
        "Shape": "circle",
        "Filled": True,
        "Color": color,
        "r": 0.8 * min(1, agent.cards / 10),
        "Layer": 0,
    }
    return portrayal
