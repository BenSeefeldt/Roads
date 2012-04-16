/**
 * 
 */

/**
 * @author kahorton
 *
 */
public class Cluster {
	/*
	centroid	double[] 
	data		double[][]
	getCentriod()	double[]
	setCentroid(double[] centroid)
	getData()	double[][]
	setData(double[][] data)
	*/
	/**
	 * the data structure holding the values for centroid of the cluster
	 */
	private double[] centroid;
	
	/**
	 * 
	 */
	private double[] oldCentroid;
	
	/**
	 * the data structure holding the data points in the cluster
	 */
	private double[][] data;
	
	/**
	 * the size and current index for the last piece of data in the cluster
	 */
	private int size = 0;

	private int numInstances;

	/**
	 * the indices of the data in this cluster
	 */
	private int[] pointers;


	/**
	 * 
	 */
	public Cluster(int numInstances) {
		this.numInstances = numInstances;
		clear();
	}

	/**
	 * @return the centroid
	 */
	public double[] getCentroid() {
		return centroid;
	}

	/**
	 * sets a new centroid and assigns the old one to oldCentroid
	 * @param centroid the centroid to set
	 */
	public void setCentroid(double[] centroid) {
		oldCentroid = this.centroid;
		this.centroid = centroid;
		
	}

	/**
	 * @return the data
	 */
	public double[][] getData() {
		return data;
	}

	/**
	 * @param data the data to set
	 */
	public void setData(double[][] data) {
		this.data = data;
	}
	
	/**
	 * this method adds an instance of data to the cluster
	 * void
	 * @param instance
	 */
	public void addData(double[] instance, int index){
		data[size] = instance;
		pointers[size] = index;
		size++;
	}
	
	public double mean(int attribute){
		double sum = 0;
		for(int i =0; i< data[0].length; i++){
			sum += data[i][attribute];
		}
		return sum / data[attribute].length;
	}
	
	public double centroidDifference(){
		return Distance.euclidian(oldCentroid, centroid);
	}
	
	public void clear(){
		setData(new double[numInstances][]);
		pointers = new int[numInstances];
		size = 0;
	}
	public int[] pointerList(){
		return pointers;
	}
	public void addPointer(int index){
		pointers[size]=index;
	}
	

}
