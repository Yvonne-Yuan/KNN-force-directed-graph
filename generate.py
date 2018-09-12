import pandas as pd
from pipe_fn import *
df=pd.read_csv('vecs.csv')
vecs=df.iloc[:,:-2].values
labels=df[df.columns[-1]].values
titles=df[df.columns[-2]].values

pipe(vecs,labels,titles,400,image_dataset=False,k_neighbors=5,output_file='static/graphFile.json')