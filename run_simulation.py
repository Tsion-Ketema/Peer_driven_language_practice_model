from language_model import LanguageClassModel
import matplotlib.pyplot as plt

# Initialize and run the model
model = LanguageClassModel(N=25, width=5, height=5)
for _ in range(100):
    model.step()

# Retrieve data
model_df = model.datacollector.get_model_vars_dataframe()

# Plot L2 usage over time
model_df["L2_Usage"].plot(title="L2 Usage Over Time")
plt.xlabel("Step")
plt.ylabel("L2 Usage Ratio")
plt.show()

# Plot average language level
model_df["Avg_Level"].plot(title="Average Language Level Over Time")
plt.xlabel("Step")
plt.ylabel("Average Level")
plt.show()
