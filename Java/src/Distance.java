/**
 * 
 */

/**
 * this distance class contains methods for to find the euclidian and 
 * cosine differences between arrays of doubles
 * @author kahorton
 *
 */
public class Distance {

	/**
	 * finds the euclidian distance between two double arrays given the same length
	 * double
	 * @param a
	 * @param b
	 * @return the euclidian distance between the two arrays values
	 */
	public static double euclidian(double[] a, double[] b){
		double dist = 0;
		for(int i =0; i < a.length; i++){
			dist += Math.pow(a[i]-b[i], 2);
			}
		return Math.sqrt(dist);
	}
	/**
	 * finds the cosine difference between two double arrays given the same length
	 * double
	 * @param a
	 * @param b
	 * @return the cosine difference between the two arrays values
	 */
	public static double cosine(double[] a, double[] b){
		double dist = 0;
		double lengthx = 0;
		double lengthy = 0;
		for(int i =0; i < a.length; i++){
			dist+= a[i]*b[i];
			lengthx += a[i]*a[i];
			lengthy += b[i]*b[i];
		}
		lengthx = Math.sqrt(lengthx);
		lengthy = Math.sqrt(lengthy);
		return 1-(dist/(lengthx*lengthy));
	}
	

}
