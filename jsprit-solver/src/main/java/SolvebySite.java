import jsprit.analysis.toolbox.AlgorithmSearchProgressChartListener;
import jsprit.analysis.toolbox.GraphStreamViewer;
import jsprit.analysis.toolbox.Plotter;
import jsprit.core.algorithm.VehicleRoutingAlgorithm;
import jsprit.core.algorithm.box.Jsprit;
import jsprit.core.algorithm.selector.SelectBest;
import jsprit.core.analysis.SolutionAnalyser;
import jsprit.core.problem.Location;
import jsprit.core.problem.VehicleRoutingProblem;
import jsprit.core.problem.cost.TransportDistance;
import jsprit.core.problem.io.VrpXMLReader;
import jsprit.core.problem.io.VrpXMLWriter;
import jsprit.core.problem.solution.VehicleRoutingProblemSolution;
import jsprit.core.reporting.SolutionPrinter;
import jsprit.core.util.Coordinate;
import jsprit.core.util.DistanceUnit;
import jsprit.core.util.GreatCircleCosts;

import java.io.*;
import java.util.Collection;

/**
 * Created by xfz on 8/8/16.
 */
public class SolvebySite {
    public static void main(String[] args) {

		/*
         * some preparation - create output folder
		 */
        File dir = new File("output");
        // if the directory does not exist, create it
        if (!dir.exists()){
            System.out.println("creating directory ./output");
            boolean result = dir.mkdir();
            if(result) System.out.println("./output created");
        }


        FileReader f ;
        BufferedReader buffer;
        try {
            f =   new FileReader("input/xmlName.txt");
            buffer = new BufferedReader(f);
            String line;
            try {
                    while ((line = buffer.readLine()) != null)
                    {
                        VehicleRoutingProblem.Builder vrpBuilder = VehicleRoutingProblem.Builder.newInstance();
                        new VrpXMLReader(vrpBuilder).read("input/" +line );
                        vrpBuilder.setRoutingCost(new GreatCircleCosts() {
                            // @overide
                            public double calculateDistance(Coordinate coord1, Coordinate coord2, DistanceUnit distanceUnit) {
                                double lon1 = coord1.getX();
                                double lon2 = coord2.getX();
                                double lat1 = coord1.getY();
                                double lat2 = coord2.getY();
                                double r = 6378.137;

                                double delta_Lat = Math.toRadians(lat2 - lat1);
                                double delta_Lon = Math.toRadians(lon2 - lon1);
                                lat1 = Math.toRadians(lat1);
                                lat2 = Math.toRadians(lat2);

                                double a = Math.sin(delta_Lat / 2) * Math.sin(delta_Lat / 2) + Math.sin(delta_Lon / 2) * Math.sin(delta_Lon / 2) * Math.cos(lat1) * Math.cos(lat2);
                                double c = 2 * Math.asin(Math.sqrt(a));
                                double distance = r * c;
                                if (distanceUnit.equals(DistanceUnit.Meter)) {
                                    distance = distance * 1000.;

                                }
                                return distance;

                            }

                            ;

                        });
                        final VehicleRoutingProblem vrp = vrpBuilder.build();
                        VehicleRoutingAlgorithm vra = Jsprit.createAlgorithm(vrp);

        /*
         * Solve the problem.
		 *
		 *
		 */

                        Collection<VehicleRoutingProblemSolution> solutions = vra.searchSolutions();

		/*
         * Retrieve best solution.
		 */
                        VehicleRoutingProblemSolution solution = new SelectBest().selectSolution(solutions);

                        new VrpXMLWriter(vrp, solutions).write("output/solution" + line);

                    }
                }
            catch(IOException e)
            {
                e.printStackTrace();
            }
        }
        catch (FileNotFoundException e )
        {
            e.printStackTrace();
        }

		/*
         * Define the required vehicle-routing algorithms to solve the above problem.
		 *
		 * The algorithm can be defined and configured in an xml-file.
		 */
//		VehicleRoutingAlgorithm vra = new SchrimpfFactory().createAlgorithm(vrp);


    }
}
