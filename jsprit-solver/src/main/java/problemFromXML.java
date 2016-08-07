/*
 * Licensed to GraphHopper GmbH under one or more contributor
 * license agreements. See the NOTICE file distributed with this work for
 * additional information regarding copyright ownership.
 *
 * GraphHopper GmbH licenses this file to you under the Apache License,
 * Version 2.0 (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


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
import jsprit.core.problem.solution.VehicleRoutingProblemSolution;
import jsprit.core.problem.vehicle.Vehicle;
import jsprit.core.reporting.SolutionPrinter;
import jsprit.core.problem.cost.TransportDistance;


import java.io.File;
import java.util.Collection;

public class problemFromXML {

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

		/*
         * Build the problem.
		 *
		 * But define a problem-builder first.
		 */
        VehicleRoutingProblem.Builder vrpBuilder = VehicleRoutingProblem.Builder.newInstance();

		/*
         * A solomonReader reads solomon-instance files, and stores the required information in the builder.
		 */
           // new VrpXMLReader(vrpBuilder).read("/home/xfz/sandBox/jsprit/jsprit-examples/input/pickups_and_deliveries_solomon_r101.xml");
        new VrpXMLReader(vrpBuilder).read("input/test.xml");
		/*
         * Finally, the problem can be built. By default, transportCosts are crowFlyDistances (as usually used for vrp-instances).
		 */

        final VehicleRoutingProblem vrp = vrpBuilder.build();

        new Plotter(vrp).plot("output/pd_solomon_r101.png", "pd_r101");
        ;


		/*
         * Define the required vehicle-routing algorithms to solve the above problem.
		 *
		 * The algorithm can be defined and configured in an xml-file.
		 */
//		VehicleRoutingAlgorithm vra = new SchrimpfFactory().createAlgorithm(vrp);
        VehicleRoutingAlgorithm vra = Jsprit.createAlgorithm(vrp);
        vra.getAlgorithmListeners().addListener(new AlgorithmSearchProgressChartListener("output/sol_progress.png"));
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
        new GraphStreamViewer(vrp, solution).labelWith(GraphStreamViewer.Label.ID).setRenderDelay(200).display();
		/*

		 * print solution
		 */
        SolutionPrinter.print(solution);

		/*
		 * Plot solution.
		 */
//		SolutionPlotter.plotSolutionAsPNG(vrp, solution, "output/pd_solomon_r101_solution.png","pd_r101");
        Plotter plotter = new Plotter(vrp, solution);
        plotter.setLabel(Plotter.Label.SIZE);
        plotter.plot("output/pd_solomon_r101_solution.png", "pd_r101");

        //some stats
        SolutionAnalyser analyser = new SolutionAnalyser(vrp, solution, new TransportDistance() {

            //@Override
            public double getDistance(Location from, Location to) {
                return vrp.getTransportCosts().getTransportCost(from, to, 0., null, null);
            }

        });

        System.out.println("tp_distance: " + analyser.getDistance());
        System.out.println("tp_time: " + analyser.getTransportTime());
        System.out.println("waiting: " + analyser.getWaitingTime());
        System.out.println("service: " + analyser.getServiceTime());
        System.out.println("#picks: " + analyser.getNumberOfPickups());
        System.out.println("#deliveries: " + analyser.getNumberOfDeliveries());


    }

}