#! /usr/bin/env python
import sys
import arff
import math
import os.path
import Image
import dist
import kmeans
from time import time
from optparse import OptionParser

def serial_kmeans(data, k, dist):
  return kmeans.k_means(data,k,dist)

#The main method for running the k-means algorithm.
#This file will evolve with the project, adding options as far
#as specifics of running and timing go

def main():
  parser = OptionParser(usage="usage: %prog [options] filename",
             version="%prog 1.0")
  parser.add_option("-p", "--parallel",
           action="store_true",
           dest="parallel_run",
           default=False,
           help="Runs the kmeans algorithm in parallel execution. Default serial.")
  parser.add_option("-i", "--image",
           action="store",
           dest="image",
           default="",
           help="File input is an picture file. Without flag, assumes a arff. Takes output path.") 
  parser.add_option("-c","--cos",
           action="store_true",
           dest="cos",
           default=False,
           help="Use cos similarity for the distance measrue, defaults to euclidean.")
  parser.add_option("-k", "--numk",
           action="store", # optional because action defaults to "store"
           dest="k",
           default=3,
           help="You must give a value for the number of clusters, defaults to 3.",)
  
  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.error("wrong number of arguments")
  #Parses k.
  options.k=int(options.k)
  dist_measure=dist.euclidiandist
  if options.cos:
    dist_measure=dist.cosdissimilarity
  
  size=0,0
  #LOADS IN DATA
  a=time()
  data=[]
  if not options.image:
    data_in=list(arff.load(args[0]))
    for i in range(len(data_in)):
      a=[]
      for j in range(len(data_in[0])-1):
        a.append(data_in[i][j])
      data_labels.append(data_in[i][len(data_in[0])-1])
      data.append(a)  
  else:
    img=Image.open(args[0])
    for i in list(img.getdata()):
      data.append(list(i))
    size=img.size
  #END LOAD DATA
  print "Loading completed in "+str(time()-a)+" sec."
  
  centroids=[]
  clusters=[]
  if not options.parallel_run:
    print "Running Serial Exeuction."
    a=time()
    centroids,clusters=serial_kmeans(data,options.k,dist_measure)  
    print "Serial execution completed in "+str(time()-a)+" sec."
  else:
    print "Parallel kmeans is not yet implemented"
    #parallel_kmeans()
    
  if not options.image:
    #handle the output of clusters
    pass
  else:
    img=Image.new("RGB",size)
    px=img.load()
    colors=[]
    for i in centroids:
      t=(int(i[0]),int(i[1]),int(i[2]))
      colors.append(t)
    for i in range(len(clusters)):
      for k in clusters[i]:
        y=(k/size[0])
        x=(k%size[0])
        #print k,x,y
        px[x,y]=colors[i]
    #img.show()
    img.save(options.image+".tiff","TIFF")

  
  
if __name__ == '__main__':
  main()
