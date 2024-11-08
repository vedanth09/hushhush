import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pickle
import sqlite3


#connecting to database and load the tables
conn = sqlite3.connect('hushhushDB.db')

df = pd.read_sql_query("SELECT * FROM live_data", conn)

df = pd.read_csv("dataclean.csv")
df2 = df.drop(columns=['Name', 'Email','Public Reposcount','Public Gistscount'])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df2)

sse = []
k_range = range(1,25)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    sse.append(kmeans.inertia_)

# Elbow Method Graph
plt.figure(figsize=(10, 6))
plt.plot(k_range, sse, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Sum of Squared Errors (SSE)')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.grid(True)
plt.show()


# Based on the Elbow plot, choose the optimal number of clusters
optimal_k = 2

# Fit KMeans with the optimal number of clusters
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(X_scaled)
cluster = kmeans.predict(X_scaled)
filename = "kmeans.pickle"
pickle.dump(kmeans, open(filename, "wb"))

df2['clusters'] = cluster

pca = PCA(n_components=2)
X_pca = pca.fit_transform(df2)

# Add PCA components to the DataFrame
df2['PCA1'] = X_pca[:, 0]
df2['PCA2'] = X_pca[:, 1]

# Plot the clusters using seaborn
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df2, x='PCA1', y='PCA2', hue='clusters', palette='viridis')

# Add plot details
plt.title('K-Means Clustering with PCA Components')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.grid(True)
plt.show()
