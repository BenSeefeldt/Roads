import java.util.Random;

/**
 * 
 */

/**
 * @author kahorton
 *
 */
public class Kmeans {
/*
 * _: KMeans.java
	kmeans(double[][] data, int k, String distanceMeasure)
 * 
 * 	public void kMeansEuc(int k){
		this.k = k;
		findInitCentroids();
		do{
			assignPointsEuc();
			recomputeCentroid();
		}
		while(!compareCentriods());
	}
 */
	private Cluster[] cluster;
	/**
	 * the number of clusters
	 */
	private int k;
	/**
	 * the data
	 */
	private double[][] data;
	
	/**
	 * the distance measure as an enumerated type
	 * 1 = euclidian
	 * 0 = cos
	 */
	private int dm=0;
	
	private int numAttributes, numInstances;
	
	/**
	 * 
	 * @param data
	 * @param k
	 * @param distanceMeasure
	 */
	
	public Kmeans(double[][] data, int k, String distanceMeasure){
		this.k = k;
		this.data = data;
		numInstances = data.length;
		numAttributes = data[0].length;
		if(distanceMeasure.equals("euclidian")){
			dm = 1;
		}
		cluster = new Cluster[k];
		findInitCentroids();
		do{
			assignPoints(dm);
			recomputeCentroid();
		}
		while(compareCentroids() > 0);
	}

	/**
	 * this method randomly finds k unique centroids to be initially used in the k means algorithm
	 */
 public void findInitCentroids(){
		Random r = new Random();
		int[] centroid = new int[k];
		int i = 0;
		boolean same = false;
		
		do{//Find k, random centroids
			centroid[i] = r.nextInt(numInstances);
			if(i>0){
				for(int j=0; j < i; j++){
					if(centroid[j] == centroid[i]){
						same = true;
					}
				}
			}
			if(!same) i++;
			same = false;
		}
		while(i < k);
		
		//assign centroids to element 0 or cluster arrays
		for(int j=0; j < k; j++){
			System.out.println(j);
			cluster[j] = new Cluster(numInstances);
			cluster[j].setCentroid(data[centroid[j]]);
		}
	}
 
	/**
	 * this method goes through the data set and assigns data samples the the cluster with the closest 
	 * centroid using euclidean distance 
	 */
	public void assignPoints(int dm){
		/*
		 * clean clusters
		 */
		for(int i = 0; i < k; i++){
			cluster[i].clear();
		}
		
		/*
		 * euclidian distance
		 */
		if(dm==1){
			//double closestCluster;
			int closestCluster;
			for(int i = 0; i < numInstances; i++){
				closestCluster = 0;
				for(int j = 1; j < k; j++){
					// cluster m is closer than current closest
					if( Distance.euclidian(data[i], cluster[j].getCentroid()) <
							Distance.euclidian(data[i], cluster[closestCluster].getCentroid())){
						closestCluster = j;
					}
				}
				cluster[closestCluster].addData(data[i], i);
			}
		}
		/*
		 * cosine distance
		 */
		else{//dm ==0
			//double closestCluster;
			int closestCluster;
			for(int i = 0; i < numInstances; i++){
				closestCluster = 0;
				for(int j = 1; j < k; j++){
					// cluster m is closer than current closest
					if( Distance.cosine(data[i], cluster[j].getCentroid()) <
							Distance.cosine(data[i], cluster[closestCluster].getCentroid())){
						closestCluster = j;
					}
				}
				cluster[closestCluster].addData(data[i], i);
			}
		}
	
	}
 
	/**
	 * this method recomputes the centroids of the clusters by finding the average of all of the attributes
	 */
	public void recomputeCentroid(){
		for(int i = 0; i < k; i++){
			double[] newCentroid = new double[numAttributes];
			for(int j = 0; j < numAttributes; j++){
				//System.out.println("i: "+i+", j: "+j);
				newCentroid[j] = cluster[i].mean(j);
			}
			cluster[i].setCentroid(newCentroid);
		}	
	}

	public double compareCentroids(){
		int difference = 0;
		for(int i =0; i<k; i++){
			difference += cluster[i].centroidDifference();
		}
		return difference;
	}
	
	public Cluster[] getClusters(){
		return cluster;
	}


}
