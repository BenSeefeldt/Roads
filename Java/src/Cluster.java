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
	 * the data structure holding the data points in the cluster
	 */
	private double[][] data;

	/**
	 * @return the centroid
	 */
	public double[] getCentroid() {
		return centroid;
	}

	/**
	 * @param centroid the centroid to set
	 */
	private void setCentroid(double[] centroid) {
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
	private void setData(double[][] data) {
		this.data = data;
	}
	

}
