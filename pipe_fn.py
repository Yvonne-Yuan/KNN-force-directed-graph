def pipe(data,labels,words,NODES_N,SIZE=(30,30),image_dataset=True,k_neighbors=5,output_file='graphFile.json'):

    '''
    what this function does is take a dataset, compute all pairwise distances n(O^2) between the data points.
    and appends each datapoint in the json file as a node, each node given some attributes.
    then for each data point, it find the nearest 5 points, and appends a source-target reference in the links array of the json file.
    if the dataset consisted of images, it saves the images in the directory, so they'll get used when the graph visualization is displayed.


    parameters:
    data: 2d array or 2d list (your data)
    labels: 1d array or list of the associated labels of each vector
    words: the text that appears when the node is hovered above in the graph visualization
    NODES_N: how many nodes you want in the graph
    SIZE: for image datasets, the size of the image
    image_dataset: boolean
    k_neighbors: the k parameter for the graph


    '''


    #this function will shuffle the data and labels, no need to shuffle them outside
    import json
    from PIL import Image
    from scipy.misc import toimage
    from numpy.linalg import norm
    import numpy as np
    from scipy.spatial.distance import cosine

    def unison_shuffled_copies(a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]

    def node_appender(data,name,group,src):
        #data is a dictionary, loaded from a json file
        #with the initial shape :
        # {
        #   "nodes": [
        #   ],
        #   "links": [
        #   ]
        # }

        data['nodes'].append({'name':name,'group':group,'src':src})

    def link_appender(data,source=0,target=0):
        data['links'].append({'source':source,'target':target})

    data=np.array(data)
    labels=np.array(labels)
    words=np.array(words)
    
    p = np.random.permutation(len(data))
    data = data[p]
    labels= labels[p]
    words=words[p]

    data=data[:NODES_N]
    labels=labels[:NODES_N]
    words=words[:NODES_N]

    distances={}

    for i in range(NODES_N):
        distances[i]=[]
        #an O(n^2) algorithm to find pairwise distance between each data point
        for j in range(NODES_N):
            if i!=j:
                #the form of distances is distances={ 0:[(1,19),(2,3),(3,19)...(NODES_N-1,39)]  }
                distances[i].append( ( j ,cosine(data[i],data[j] ))) 



    for i in range(NODES_N):
        #sort the values of the dictionary according to the distance
        distances[i]=sorted(distances[i],key=lambda x:x[1])


    with open('structure.json') as f:
        json_graph=json.load(f)


    #add an if clause, that excutes this if a parameter in the funciton call is set to True
    #otherwise the nodes should display text


    if image_dataset is True:
        for i in range(NODES_N):
            x=data[i].reshape(SIZE)
            toimage(x).save(str(i)+'.png')



    for i in range(NODES_N):
        #add to json_graph node identified by the name 'n'+i , it's label, the str(i) fills the 'src' key in the dict 
        node_appender(json_graph,'n'+str(i),int(labels[i]), words[i] )
        for j in range(k_neighbors):
            o=distances[i][j][0]
            link_appender(json_graph,i,o)



    with open(output_file,'w') as f:
        json.dump(json_graph,f,indent=2)


def load_data_set(FILE):
    import json
    with open(FILE) as f:
        x=json.load(f)
    data=x['data']
    labels=x['labels']
    words=x['words']
    return data,words,labels

#data,words,labels=load_data_set('u.json')

#pipe(data,labels,words,1000,image_dataset=False,k_neighbors=3):


#
# data=[]
# for i in range(500):
#     data.append(np.array(Image.open('c:/guitar_normalized/guitar_'+str(i)+'.jpg')))
#
# for i in range(500):
#     data.append(np.array(Image.open('c:/cat_normalized/cat_'+str(i)+'.jpg')))
#
# pipe_fn.pipe(dataset1,labels1,1000,(30,30))
