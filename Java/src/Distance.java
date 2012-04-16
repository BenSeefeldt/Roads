/**
 * 
 */

/**
 * @author kahorton
 *
 */
public class Distance {
	/*
	euc(double[] a, double[] b)
	cos(double[] a, double[] b)
	*/
	public static double euclidian(double[] a, double[] b){
		double dist = 0;
		for(int i =0; i < a.length; i++){
			dist += Math.pow(a[i]-b[i], 2);
			}
		return Math.sqrt(dist);
	}
	
	public static double cosine(double[] a, double[] b){
		double dist = 0;
		double lengthx = 0;
		double lengthy = 0;
		for(int i =0; i < a.length; i++){
			
		}
		return dist;
	}
	

}
