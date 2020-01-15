'''
Created on Jan 14, 2019

@author: nanda

dst
python ~/aTools/utilities/k-means.py

'''

from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
data = pd.read_csv("chr13-cluster13-trans.matrix",delimiter='\t', index_col=0)
df = data.fillna(0)

kmeans = KMeans(n_clusters=20, random_state=0).fit(df)
labels = kmeans.predict(df)
headers=[]
headers=list(df.index)
clusters = {}
n = 0
for item in labels:
    if item in clusters:
        clusters[item].append(df.loc[headers[n],:])
    else:
        clusters[item] = [df.loc[headers[n],:]]
    n +=1

with open("clustered-header","w") as fh:
    for item in clusters:
        #print("Cluster ", item, clusters[item][0].name)
        for i in clusters[item]:
            fh.write(i.name+"\n")
