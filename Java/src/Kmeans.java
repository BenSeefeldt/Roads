import java.util.Random;

/**
 * 
 */

/**
 * @author kahorton
 *
 */
public class Kmeans {

	/**
	 * the array of Cluster objects that hold the clusters for the kmeans algorithm
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
	
	/**
	 * variables that hold the number of attributes and instances in the data set
	 */
	private int numAttributes, numInstances;
	
	/**
	 * the Kmeans algorithm. it takes a data set and clusters it into k different clusters 
	 * using a distance measure provided by the user
	 * @param data the data set formatted as an array of double arrays 
	 * 			where each array is a data sample
	 * @param k the integer value of the desired amount of clusters
	 * @param distanceMeasure the name of the distance measure to be used in the k means algorithm
	 * 			this implementation supports "euclidian", and "cosine" with cosine as the default
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
	 * this method randomly finds k unique centroids to be initially used in the 
	 * k means algorithm. it also initializes the clusters
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
  * this method goes through the data set and assigns data samples to 
  * the cluster with the closest cluster using the given distance measure
  * void
  * @param dm the distance measure as an enumerated type
  * 		1 = euclidian; 0 = cosine
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
	 * this method recomputes the centroids of the clusters by finding the 
	 * average values of all of the attributes and using them as the new centroid
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

	/**
	 * this method finds the sum of all of the differences between new and 
	 * old centroids
	 * double
	 * @return the double value of the sum of all of the differences between 
	 * 			previous and current centroids
	 */
	public double compareCentroids(){
		int difference = 0;
		for(int i =0; i<k; i++){
			difference += cluster[i].centroidDifference();
		}
		return difference;
	}
	
	/**
	 * this method returns the Clusters found by the kmeans algorithm
	 * Cluster[]
	 * @return the array of Clusters
	 */
	public Cluster[] getClusters(){
		return cluster;
	}


}
