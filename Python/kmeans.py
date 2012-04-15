#! /usr/bin/env python
import math
import sys
import os.path
import dist
from time import time

#Contains only one method. The kmeans computation. 

def k_means(data,k,dist):
  '''Runs the k means algorithm with the specified distance measure
  and number of clusters.
  data -- properly formated 2-d array of data
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
#END OF KMENAS