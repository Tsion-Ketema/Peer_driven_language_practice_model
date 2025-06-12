# visualization.py

import matplotlib.pyplot as plt
import pandas as pd
from language_model import LanguageClassModel

# Run the model silently for data collection
model = LanguageClassModel(
    N=25, width=5, height=5, max_steps=100,
    initial_motivation=0.65,
    initial_anxiety=0.3,
    peer_influence=0.4,
    card_weight=0.7
)

while model.running:
    model.step()

# Collect the results into a DataFrame
results = model.datacollector.get_model_vars_dataframe()

# Plot 1: L2 Usage vs Time
plt.figure(figsize=(10, 4))
plt.plot(results['L2_Usage'], label="L2 Usage", color='green')
plt.title("L2 Usage Over Time")
plt.xlabel("Steps")
plt.ylabel("L2 Usage")
plt.grid(True)
plt.legend()
plt.show()

# Plot 2: L1 Usage vs Time (inferred)
plt.figure(figsize=(10, 4))
plt.plot(results['L1_Usage'], label="L1 Usage", color='red')
plt.title("L1 Usage Over Time")
plt.xlabel("Steps")
plt.ylabel("L1 Usage")
plt.grid(True)
plt.legend()
plt.show()

# Plot 3: Motivation vs Anxiety
plt.figure(figsize=(10, 4))
plt.plot(results['Avg_Motivation'], label="Avg Motivation", color='purple')
plt.plot(results['Avg_Anxiety'], label="Avg Anxiety", color='brown')
plt.title("Motivation vs Anxiety Over Time")
plt.xlabel("Steps")
plt.ylabel("Value")
plt.grid(True)
plt.legend()
plt.show()

# Plot 4: Avg Cards vs Low Card Students
plt.figure(figsize=(10, 4))
plt.plot(results['Avg_Cards'], label="Average Cards", color='blue')
plt.plot(results['Low_Card_Students'], label="Low Card Students", color='orange')
plt.title("Cards vs Low Card Students Over Time")
plt.xlabel("Steps")
plt.ylabel("Value")
plt.grid(True)
plt.legend()
plt.show()
