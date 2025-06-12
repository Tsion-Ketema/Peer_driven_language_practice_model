import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class StudentAgent(Agent):
    def __init__(self, unique_id, model, initial_motivation, initial_anxiety):
        super().__init__(unique_id, model)
        self.language_used = "L1"
        self.motivation = random.uniform(initial_motivation - 0.1, initial_motivation + 0.1)
        self.anxiety = random.uniform(initial_anxiety - 0.1, initial_anxiety + 0.1)
        self.cards = 1


    def decide_language(self):
        base_prob = self.motivation * 0.5 - self.anxiety * 0.4
        card_effect = min(1.5, max(0, self.cards) * self.model.card_weight)

        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        if neighbors:
            l2_neighbors = sum(1 for n in neighbors if n.language_used == "L2")
            peer_pressure = l2_neighbors / len(neighbors)
        else:
            peer_pressure = 0

        combined = base_prob + card_effect + peer_pressure * self.model.peer_influence
        probability_L2 = min(1.0, max(0.0, combined / 2))

        if random.random() < 0.05:
            self.language_used = "L1" if self.language_used == "L2" else "L2"
        else:
            self.language_used = "L2" if random.random() < probability_L2 else "L1"

    def step(self):
        self.decide_language()
        self.update_cards()

    def update_cards(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)

        if self.language_used == "L2":
            self.cards = min(50, self.cards + 1.0)  # Cap growth
            self.motivation = min(0.95, self.motivation + 0.03)
            self.anxiety = max(0.1, self.anxiety - 0.02)

            if neighbors:
                l2_count = sum(1 for n in neighbors if n.language_used == "L2")
                if l2_count >= len(neighbors) * 0.75:
                    self.cards += 0.2  # Smaller bonus for strong L2 community

        elif self.language_used == "L1":
            if random.random() < 0.3:
                self.cards = max(0, self.cards - 1.0)
            self.motivation = max(0.2, self.motivation - 0.03)
            self.anxiety = min(1.0, self.anxiety + 0.015)

class LanguageClassModel(Model):
    def __init__(self, N=25, width=5, height=5, max_steps=50,
                 initial_motivation=0.65, initial_anxiety=0.3,
                 peer_influence=0.4, card_weight=0.7):

        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.current_step = 0
        self.max_steps = max_steps

        self.initial_motivation = initial_motivation
        self.initial_anxiety = initial_anxiety
        self.peer_influence = peer_influence
        self.card_weight = card_weight



        self.datacollector = DataCollector(
            model_reporters={
                "L2_Usage": lambda m: sum(1 for a in m.schedule.agents if a.language_used == "L2") / m.num_agents,
                "L1_Usage": lambda m: sum(1 for a in m.schedule.agents if a.language_used == "L1") / m.num_agents,
                "Avg_Cards": lambda m: sum(a.cards for a in m.schedule.agents) / m.num_agents,
                "Low_Card_Students": lambda m: sum(1 for a in m.schedule.agents if a.cards <= 0),
                "Avg_Motivation": lambda m: sum(a.motivation for a in m.schedule.agents) / m.num_agents,
                "Avg_Anxiety": lambda m: sum(a.anxiety for a in m.schedule.agents) / m.num_agents,
            }
        )

        for i in range(self.num_agents):
            agent = StudentAgent(i, self, self.initial_motivation, self.initial_anxiety)
            self.schedule.add(agent)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        self.datacollector.collect(self)

    def step(self):
        if self.current_step < self.max_steps:
            self.schedule.step()
            self.datacollector.collect(self)
            self.current_step += 1
        else:
            self.running = False


