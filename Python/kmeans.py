#! /usr/bin/env python
import arff
import math
import sys
import os.path
import dist
import Image
from time import time
#INPUT is file and k

data=[]
data_labels=[]
classes=[]

def main():
  ins=sys.argv
  if len(ins)==2:
    runAll(ins)
  elif len(ins)<2 or len(ins)==3 or len(ins)>4:
    sys.exit("You must provide 1 file on the command line followed by a number of k and either \"euc\" or \"cos\".\nOr you can provide just the file and the program will run for all distance measures and 3 different values for k.")
  elif len(ins)==4:
    loadAndRun(ins)
  if not os.path.isfile(ins[1]):
    sys.exit("Please check that a file exists at the given path.")

def load_image_data(path):
  img=Image.open(path)
  for i in list(img.getdata()):
    data.append(list(i))
  return img.size
  


def load_global_data(path):
  '''Takes a filepath from the command line arguments and loads
  in the appropriate data to the global variables.'''
  #raw-ish arff data
  data_in=list(arff.load(path))
  for i in range(len(data_in)):
    a=[]
    for j in range(len(data_in[0])-1):
      a.append(data_in[i][j])
    data_labels.append(data_in[i][len(data_in[0])-1])
    data.append(a)
  #gathers all the class labels. They'll probably come in handy.
  for i in range(len(data_in)):
    val=data_in[i]._asdict().values()[len(data_in[i])-1]
    if val not in classes:
      classes.append(val)
  

def k_means(dist,k):
  '''Runs the k means algorithm with the specified distance measure
  and number of clusters.
  
  dist -- distance function
  k -- number of clusters
  
  returns -- returns list of centroids and list of clusters (which is a list of points' indicies)
  prints out header and cluster on stout.  
  '''
  #We will arbitrarily pick the first k points as centroids.
  #Please note that centroid will not always be data points.
  #len(centroids)==k
  cycles=0
  centroids=[]
  if k>len(data):
    print "Error: k should be less than the number of records"
    sys.exit(0)
  for i in range(k):
    centroids.append(data[i][:])
  clusters_changed=True
  #This array will contain arrays of indexes of data points
  clusters=[]
  #initialize it so that we don't get index out of range problems down the line.
  for w in range(k):
    clusters.append([])
  while clusters_changed:
    #print "centroids",centroids
    #We need to store both old clusters and new, so that we can compare them.
    new_clusters=[]
    #initialize new clusters
    for w in range(k):
      new_clusters.append([])
    #For every point, we must place it in a centroid. j is the point's index.
    #print "data",data
    for j in range(len(data)):
      
      #Find the closest centroid.
      sortable=[]
      for c in range(len(centroids)):
        d=dist(centroids[c],data[j])
        t=d,c
        sortable.append(t)
      list.sort(sortable)
      #print j,sortable
      #Places point index in closest centroid. (e.g. shortest distance)
      new_clusters[sortable[0][1]].append(j)
    #At this point we have successfully created our new clusters. Now we need to compare them to the original clusters
    #Please note: We just need to check new[i] against old[i]. They should line up.
    #print new_clusters
    #print clusters
    same=True
    for i in range(k):
      #we only sort new clusters. Old clusters have been sorted because they used to be new clusters.
      new_clusters[i].sort()
      #Clusters have changed.
      if(clusters[i]!=new_clusters[i]):
        same=False
        break;
    if(same==False):
      #print "data beginning recompute",data
      #print "centroids en recomp",centroids
      #reassign, recompute centroids and continue
      cycles+=1
      clusters=new_clusters
      for q in range(k):
        for w in range(len(data[0])):
          runtot=0.0
          for e in range(len(clusters[q])):
            index=clusters[q][e]
            runtot+=data[index][w]
          val=len(clusters[q])
          if val!=0:
            runtot=runtot/len(clusters[q])
          else:
            runtot=0
          centroids[q][w]=runtot
      #print "data end recompue",data

          
    else:
      #We've found the stuff, so print stuff and return.
      #print "**********For",k,"Clusters***********"
      #for i in range(k):
        #print "Cluster",i,"centroid is:",centroids[i]
        #print "\tContaining points:", clusters[i]
        #for j in range(len(clusters[i])):
          #print data_labels[clusters[i][j]]
          
        #print "cycles to complete:",cycles
      #print "cycles to complete:",cycles
      return centroids, clusters

def computeWSS(centroids, clusters,dist=dist.euclidiandist):
  '''Computes the WSS.
  centroids -- a list of records that form the centroids for the given clusters.
  clusters -- a list of lists which hold the indexes for the points in each clusters. Corresponds to globally stored data.
  dist -- the distance function used to compute WSS. Defaults to euclidian dist.

  returns -- the WSS.
  '''
  WSS=0.0
  for i in range(len(clusters)):
    for j in range(len(clusters[i])):
      dis=dist(centroids[i],data[clusters[i][j]])
      dis=math.pow(dis,2)
      WSS+=dis
  return WSS

def computeBSS(centroids, clusters, dist=dist.euclidiandist):
  '''Computes the BSS.
  centroids -- a list of records that form the centroids for the given data.
  clusters -- a list of lists which hold the indexes for the points in each cluster. Corresponds to globally stored data
  dist -- the distance function used to compute BSS. Defaults to euclidian dist.

  returns -- the BSS
  '''
  BSS=0.0
  all_centroid=[]
  #First we must compute the centroid of the entire data set.
  for i in range(len(data[0])):
    run_tot=0.0
    for j in data:
      run_tot+=j[i]
    all_centroid.append(run_tot/len(data))
  #Now we can compute the BSS
  for i in range(len(clusters)):
    BSS+=len(clusters[i])*math.pow(dist(all_centroid,centroids[i]),2)
  return BSS
  
def computeEntropy(clusters):
  '''Computes the Entropy of these clusters based off globally stored class labels.
  clusters -- a list of lists which hold the indexes for the poitns in each cluster. Corresponds to globally stored data
  
  returns -- first entropy, which is list of values corresponding to clusters then weighted, which is total weighted entropy.
  '''
  entropy=[]
  weighted=0.0
  for i in clusters:
    if len(i)==(0 or 1):
      entropy.append(0)
    else:
      e=0.0
      #We need to compute class counts
      counts=[]
      for cl in classes:
        counts.append(0)
      for j in i:
        labl=data_labels[j]
        counts[classes.index(labl)]+=1
      tot=len(i)
      for ct in counts:
        #We include this because we get a domain error if we try to take a log with 0
        if ct!=0:
          #print "ct",ct
          #print "tot", tot
          v=((ct*1.0)/(tot*1.0))
          e+=(-v*math.log(v,2))
      entropy.append(e)
  #Now to find weighted entropy
  total_count=0
  for i in clusters:
    total_count+=len(i)
  for i in range(len(clusters)):
    v=((len(clusters[i])*1.0)/(total_count*1.0))
    weighted+=(v*entropy[i])
  
  return entropy,weighted

def doAll(adist,k):
  centroids, clusters=k_means(adist,k)
  WSS=computeWSS(centroids, clusters, adist)
  BSS=computeBSS(centroids, clusters, adist)
  entropy,weighted=computeEntropy(clusters)
  print "WSS:",WSS
  print "BSS:",BSS
  print "Total:",WSS+BSS
  print "Entropies",entropy
  print "Total Entropy",weighted

def runAll(ins):
  load_global_data(ins[1])
  print "---------USING EUCLIDIAN DISTANCE-------------"
  doAll(dist.euclidiandist,len(classes))
  doAll(dist.euclidiandist,len(classes)*2)
  doAll(dist.euclidiandist,len(classes)*3)
  print "---------USING COSINE SIMILIARITY-------------"
  doAll(dist.cosdissimilarity,len(classes))
  doAll(dist.cosdissimilarity,len(classes)*2)
  doAll(dist.cosdissimilarity,len(classes)*3)
  
  
  

def loadAndRun(ins):
  '''Gets this whole show on the road'''
  #loads in data
  k=int(ins[2])
  d=ins[3]
  mydist=""
  if d=="euc":
    mydist=dist.euclidiandist
  elif d=="cos":
    mydist=dist.cosdissimilarity
  else:
    print "Not a valid distance measure"
    return
  load_global_data(ins[1])
  #print "data",data
  #print "data_labels",data_labels
  #print "classes",classes
  centroids, clusters=k_means(mydist,k)
  WSS=computeWSS(centroids, clusters, mydist)
  BSS=computeBSS(centroids, clusters, mydist)
  entropy,weighted=computeEntropy(clusters)
  print "WSS:",WSS
  print "BSS:",BSS
  print "Total:",WSS+BSS
  print "Entropies",entropy
  print "Total Entropy",weighted

def picMain():
  filename="sesame"
  size=load_image_data(filename+".jpg")
  w=size[0]
  h=size[1]
  #print len(data)
  start=time()
  centr,clusters=k_means(dist.euclidiandist,4)
  end=time()
  totaltime=end-start
  img=Image.new("RGB",size)
  px=img.load()
  colors=[]
  for i in centr:
    t=(int(i[0]),int(i[1]),int(i[2]))
    colors.append(t)
  #colors=[(0,255,255),(255,0,255),(255,255,0),(140,140,140),(25,140,250)]
  print "For an image dimensions:",size,"using",len(clusters),"clusters, the computation took:",totaltime
  #print img.size
  #print w
  #print h
  #print len(clusters)
  for i in range(len(clusters)):
    for k in clusters[i]:
      y=(k/w)
      x=(k%w)
      #print k,x,y
      px[x,y]=colors[i]
  #img.show()
  img.save(filename+"_clustered4.tiff","TIFF")
    

# -- START OF EXECUTION-- 
if __name__=='__main__':
  picMain()
