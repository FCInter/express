import jsprit.core.problem.Location;
import jsprit.core.problem.driver.Driver;
import jsprit.core.problem.vehicle.Vehicle;
import jsprit.core.util.*;

/**
 * Created by xfz on 8/9/16.
 */
public class myGreatCircleCosts  extends GreatCircleCosts{
    private double speed = 250.0D;
    private double detour = 1.0D;
    private Locations locations;
    private DistanceUnit distanceUnit;

    public void setSpeed(double speed) {
        this.speed = speed;
    }

    public void setDetour(double detour) {
        this.detour = detour;
    }

    /** @deprecated */
    @Deprecated
    public myGreatCircleCosts(Locations locations) {
        this.distanceUnit = DistanceUnit.Meter;
        this.locations = locations;
    }

    public myGreatCircleCosts() {
        this.distanceUnit = DistanceUnit.Meter;
    }

    /** @deprecated */
    @Deprecated
    public myGreatCircleCosts(Locations locations, DistanceUnit distanceUnit) {
        this.distanceUnit = DistanceUnit.Meter;
        this.locations = locations;
        this.distanceUnit = distanceUnit;
    }

    public myGreatCircleCosts(DistanceUnit distanceUnit) {
        this.distanceUnit = DistanceUnit.Meter;
        this.distanceUnit = distanceUnit;
    }

    public double getTransportCost(Location from, Location to, double time, Driver driver, Vehicle vehicle) {
        double distance;
        try {
            distance = this.calculateDistance(from, to);
        } catch (NullPointerException var11) {
            throw new NullPointerException("cannot calculate euclidean distance. coordinates are missing. either add coordinates or use another transport-cost-calculator.");
        }

        double costs = distance;
        if(vehicle != null && vehicle.getType() != null) {
            costs = distance * vehicle.getType().getVehicleCostParams().perDistanceUnit;
        }

        return costs;
    }

    private double calculateDistance(Location fromLocation, Location toLocation) {
        Coordinate from = null;
        Coordinate to = null;
        if(fromLocation.getCoordinate() != null & toLocation.getCoordinate() != null) {
            from = fromLocation.getCoordinate();
            to = toLocation.getCoordinate();
        } else if(this.locations != null) {
            from = this.locations.getCoord(fromLocation.getId());
            to = this.locations.getCoord(toLocation.getId());
        }

        if(from != null && to != null) {
            double lon1 = from.getX();
            double lon2 = to.getX();
            double lat1 = from.getY();
            double lat2 = to.getY();
            double delta_Lat = Math.toRadians(lat2 - lat1);
            double delta_Lon = Math.toRadians(lon2 - lon1);
            lat1 = Math.toRadians(lat1);
            lat2 = Math.toRadians(lat2);
            double a = Math.sin(delta_Lat / 2.0D) * Math.sin(delta_Lat / 2.0D) + Math.sin(delta_Lon / 2.0D) * Math.sin(delta_Lon / 2.0D) * Math.cos(lat1) * Math.cos(lat2);
            double c = 2.0D * Math.asin(Math.sqrt(a));
            double distance = 6378137D * c;
            if(distanceUnit.equals(DistanceUnit.Kilometer)) {
                distance /= 1000.0D;
            }

            return distance;
        } else {
            throw new NullPointerException("either from or to location is null");
        }
    }

    public double getTransportTime(Location from, Location to, double time, Driver driver, Vehicle vehicle) {

        return this.calculateDistance(from, to) / this.speed;
    }

    /** @deprecated */
    @Deprecated
    public double getDistance(String fromId, String toId) {
        Coordinate from = this.locations.getCoord(fromId);
        Coordinate to = this.locations.getCoord(toId);
        double lon1 = from.getX();
        double lon2 = to.getX();
        double lat1 = from.getY();
        double lat2 = to.getY();
        double delta_Lat = Math.toRadians(lat2 - lat1);
        double delta_Lon = Math.toRadians(lon2 - lon1);
        lat1 = Math.toRadians(lat1);
        lat2 = Math.toRadians(lat2);
        double a = Math.sin(delta_Lat / 2.0D) * Math.sin(delta_Lat / 2.0D) + Math.sin(delta_Lon / 2.0D) * Math.sin(delta_Lon / 2.0D) * Math.cos(lat1) * Math.cos(lat2);
        double c = 2.0D * Math.asin(Math.sqrt(a));
        double distance = 6378137D * c;
        if(distanceUnit.equals(DistanceUnit.Kilometer)) {
            distance /= 1000.0D;
        }

        return distance;
    }

    public double getDistance(Location from, Location to) {
        return this.calculateDistance(from, to);
    }
}
