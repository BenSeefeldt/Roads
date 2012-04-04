import math

#Contains the distance formulas. Each take in a vector(list) and
# will return a single number for an answer
def euclidiandist(r1,r2):
  '''Computes the Euclidian distance between two vectors.
  
  r1 -- the first list of values.
  r2 -- the second list of values.
  
  Returns: float
  '''
  if len(r1)!=len(r2):
    sys.exit("Length Mismatch Error From EC Dist")
  rs=0.0
  for i in range(len(r1)):
    rs+=pow(r1[i]-r2[i],2)
  return math.sqrt(rs)
  
def chebyshevdist(r1,r2):
  '''Computes the Chebyshev distance between two vectors.
  
  r1 -- the first list of values.
  r2 -- the second list of values.
  
  Returns: float
  '''
  if len(r1)!=len(r2):
    sys.exit("Length Mismatch Error From CH Dist")
  a=[]
  for i in range(len(r1)):
    a.append(abs(r1[i]-r2[i]))
  return max(a)
    
def cityblockdist(r1,r2):
  '''Computes the City Block distance between two vectors.
  
  r1 -- the first list of values.
  r2 -- the second list of values.
  
  Returns: float
  '''
  if len(r1)!=len(r2):
    sys.exit("Length Mismatch Error From CB Dist")
  rs=0.0
  for i in range(len(r1)):
    rs+=abs(r1[i]-r2[i])
  return rs
    
def cosdissimilarity(r1,r2):
  '''Computes the Cos dissimilarity between two vectors.
  This just adds 1-cos_similarity, so that all of these 
  measure work in the same direction.
  
  r1 -- the first list of values.
  r2 -- the second list of values.
  
  Returns: float
  '''
  if len(r1)!=len(r2):
    sys.exit("Length Mismatch Error From CS Dist")
  dot=0
  ax=0
  ay=0
  for i in range(len(r1)):
    dot+=r1[i]*r2[i]
    ax+=pow(r1[i],2)
    ay+=pow(r2[i],2)
  ax=math.sqrt(ax)
  ay=math.sqrt(ay)
  return 1-(dot/(ax*ay))
