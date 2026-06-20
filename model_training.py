import pandas as pd
from sklearn.cluster import KMeans
import joblib
from kneed import KneeLocator
import matplotlib.pyplot as plt

#load the saved models
scale_data = joblib.load("models/scale_data.pkl")
data_pca = joblib.load("models/data_pca.pkl")

#Here we need data_pca 

cluster_range = range(1 , 21)
wcss = []
for k in range(1 , 21):
    kmeans = KMeans(n_clusters = k , init= "k-means++")
    kmeans.fit(data_pca)
    wcss.append(kmeans.inertia_)
print(wcss)

#using knee locator to find the best value of k 
kn = KneeLocator(range(1 , 21) ,  wcss , curve="convex" , direction="decreasing")
print("K - value : " , kn.knee)


#Now apply k means
kmeans = KMeans(n_clusters=kn.knee , init= "k-means++" , random_state=42)
cluster_labels = kmeans.fit_predict(data_pca)  #We use fit predict here because we need the data points to belongs to which cluster not distance ( and for calculating the distance we need fit_transform)
print(cluster_labels)

#now saved the files
joblib.dump(kmeans , "models/kmeans.pkl")
joblib.dump(cluster_labels , "models/cluster_labels.pkl")
print("All files saved.")