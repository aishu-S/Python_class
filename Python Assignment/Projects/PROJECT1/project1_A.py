import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data_banknote_authentication.txt", header=None)

# Displaying the covariance matrix
print("Covariance matrix: \n", df.cov())

# Plotting the scatter matrix
pd.plotting.scatter_matrix(df, figsize=(13, 13))
plt.show()
