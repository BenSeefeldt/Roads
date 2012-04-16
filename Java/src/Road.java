import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

/**
 * 
 */

/**
 * @author kahorton
 *
 */
public class Road {
	
	public double[][] importImage(BufferedImage bi){
		int pixels = bi.getHeight()*bi.getWidth();
		int width = bi.getWidth();
		System.out.println(pixels+" pixels, "+width+" height"+bi.getWidth()+" width");
		double[][] arffData = new double[pixels][];
		for (int i = 0; i < pixels; i++){
			int y = i/width;
			int x = i%width;
			arffData[i] = colorToArray(bi.getRGB(x, y));
			//System.out.println(i);
		}		
		return arffData;
	}
	
	public BufferedImage drawImage(BufferedImage source,double[][] data, int height){
		BufferedImage bi = new BufferedImage(source.getWidth(), source.getHeight(), source.getType());
		int pixels = data.length;
		for(int i=0; i < pixels; i++){
			int y = i/height;
			int x = i%height;
			//System.out.println(i);
			bi.setRGB(x, y, arrayToColor(data[i]));
			
		}		
		return bi;
	}
	
	public double[] colorToArray(int ARGB){
		double[] color = new double[3];
		int alpha = (ARGB >> 24) & 0xFF;
		color[0] =  (ARGB >> 16) & 0xFF;
		color[1] =  (ARGB >>  8) & 0xFF;
		color[2] =  (ARGB      ) & 0xFF;
		return color;
		/*
		 * 	int rgb = rgbColor.getRGB(); //always returns TYPE_INT_ARGB
			int alpha = (rgb >> 24) & 0xFF;
			int red =   (rgb >> 16) & 0xFF;
			int green = (rgb >>  8) & 0xFF;
			int blue =  (rgb      ) & 0xFF;

		 */
	}
	
	/**
	 * 
	 * int
	 * @param rgb
	 * @return
	 */
	public int arrayToColor(double[] rgb){
		return (int) (65536 * rgb[0] + 256 * rgb[1] + rgb[2]);
	}
	
	/*
	 * _: Road.java
	main()
	run()
	-load data
	-get clusters
	-display output
	 */

	/**
	 * void
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Road r = new Road();
		Kmeans K;
		BufferedImage bi = null;
		double[][] rgb = new double[3][3];
		rgb[0][0] = 255; 
		rgb[1][1] = 255;
		rgb[2][2] = 255;
		int k = 2;
		try {
			 bi = ImageIO.read(new File("/home/f09/kahorton/workspace/Roads/src/BasicRoad.jpg"));

		        long startTime = System.currentTimeMillis();
			double[][] data = r.importImage(bi);
			K = new Kmeans(data, k, "euclidian");
	        long stopTime = System.currentTimeMillis();
	        System.out.println((stopTime-startTime)+" milliseconds");
			Cluster[] cluster = K.getClusters();
			
			for(int i=0;i<k;i++){
				int[] pixels = cluster[i].pointerList();
				for(int j=0;j<pixels.length;j++){
					//data[pixels[j]] = rgb[i];

					data[pixels[j]] = cluster[i].getCentroid();
				}
			}
			BufferedImage test = r.drawImage(bi, data, bi.getWidth());
			
		    File outputfile = new File("/home/f09/kahorton/workspace/Roads/src/testOut.jpg");
		    ImageIO.write(test, "jpg", outputfile);
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}  	
		

	}

}
