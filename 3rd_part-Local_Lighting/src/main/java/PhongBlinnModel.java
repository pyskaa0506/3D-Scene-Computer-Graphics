public class PhongBlinnModel extends PhongModel implements ReflectionModel{

    @Override
    protected double getSpecular(double nx, double ny, double nz, int channel){
        double [] l = getLightVector(nx,ny,nz);
        double [] halfWay = new double [3];
        halfWay[0] = l[0];
        halfWay[1] = l[1];
        halfWay[2] = l[2]+1;
        double hLen = Math.sqrt(halfWay[0]*halfWay[0]+halfWay[1]*halfWay[1]+halfWay[2]*halfWay[2]);
        double dot = (halfWay[0]*nx+halfWay[1]*ny+halfWay[2]*nz)/hLen;
        return sourceDumping * lightIntensity[1] * reflectionCoefficients[channel][2] * Math.pow(Math.max(0,dot),surfaceCoefficient);
    }

    @Override
    public String toString(){
        return "Phong-Blinn";
    }
}