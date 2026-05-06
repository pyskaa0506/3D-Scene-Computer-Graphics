public class PhongModel{

    protected double [] reflectionCoefficients = new double[] {1.5,0.25,1};
    protected double [] lightIntensity = new double[]{35,400};
    protected double surfaceCoefficient = 50;
    protected double sourceDumping = 1.0;
    protected int [] sourcePos = new int []{100,0,300};
    protected double [] scenePos = null;
    protected double bumpScale = 0.1;
    
    public void setScene(double [] center){
        scenePos = center;
    }
    protected double [] bumpNormal(double nx, double ny, double nz){
        nx += (Math.sin(nx*scenePos[3] * 0.5)) * bumpScale;
        ny += (Math.sin(ny*scenePos[3] * 0.7))* bumpScale;
        nz += (Math.sin((ny+ny)*scenePos[3] * 0.07))  * bumpScale;
        double nLen = Math.sqrt(nx*nx + ny*ny + nz*nz);
        nx /= nLen; ny /= nLen; nz /= nLen;
        return new double [] {nx,ny,nz};
    }
    protected double getAmbient(){
        return lightIntensity[0] * reflectionCoefficients[0];
    }
    protected double[] getLightVector(double nx,double ny,double nz){
        double [] lv = new double [3];
        lv[0] = sourcePos[0] - (nx* scenePos[3] + scenePos[0]);
        lv[1] = sourcePos[1] - (ny* scenePos[3] + scenePos[1]);
        lv[2] = sourcePos[2] - (nz* scenePos[3] + scenePos[2]);
        double norm2 = lv[0]*lv[0] + lv[1]*lv[1] + lv[2]*lv[2];
        double lLen = Math.sqrt(norm2);
        lv[0]/=lLen;
        lv[1]/=lLen;
        lv[2]/=lLen;
        return lv;
    }
    protected double getDiffuse(double nx,double ny,double nz){
        double [] l = getLightVector(nx,ny,nz);
        double product  = l[0]*nx+l[1]*ny+l[2]*nz;

        return sourceDumping * lightIntensity[1] * reflectionCoefficients[1] * product;
    }
    protected double getSpecular(double nx, double ny, double nz) {
        double [] l = getLightVector(nx,ny,nz);
        double [] r = new double [3];
        //r[0] = 2*nx*(ny*l[2] - nz *l[1]) - 0;
        //r[1] = 2*ny*(nz*l[0] - nx*l[2]) - 0;
        //r[3] = 2*nz*(nx*l[1] - ny*l[0]) - 1;
        double dotNL = nx * l[0]+ ny * l[1] + nz * l[2];

        r[0] = 2.0 * dotNL * nx - l[0];
        r[1] = 2.0 * dotNL * ny - l[1];
        r[2] = 2.0 * dotNL * nz - l[2];
        return sourceDumping * lightIntensity[1] * reflectionCoefficients[2] * Math.pow(Math.max(0,r[2]),surfaceCoefficient);

    }
    public double getValue(double nx, double ny, double nz){
        double[] bumpedN = bumpNormal(nx,ny,nz);
        nx = bumpedN[0];
        ny = bumpedN[1];
        nz = bumpedN[2];
        double resultValue = getAmbient() + getDiffuse(nx,ny,nz) + getSpecular(nx,ny,nz);
        double result = Math.min(1,Math.max(0,resultValue/300));
        //return (result <<16) | (result<<8) | result;
        return result;
    }
    
    public String toString(){
        return "Phong model";
    }
    public void setDiffuseReflection(double kd){
        this.reflectionCoefficients[1] = kd;
    }

    public void setSourceIntensity(double ip){
        this.lightIntensity[1] = ip;
    }

    public void setSpecularReflection(double ks){
        this.reflectionCoefficients[2] = ks;
    }

    public void setAmbientReflection(double ka){
        this.reflectionCoefficients[0] = ka;
    }

    public void setAmbientIntensity(double ia){
        this.lightIntensity[0] = ia;
    }

    public void setSurfaceCoefficient(double n) {
        this.surfaceCoefficient = n;
    }

    public void setSourceDumping(double f){
        this.sourceDumping  = f;
    }

    public int [] getSourcePosition(){
        return sourcePos;
    }

    public void setSourcePosition (int[] position){
        sourcePos = position;
    }

    public void setBumpScale(double bs){
        bumpScale = bs;
    }

    public double [] getReflectionCoefficients(){
        return reflectionCoefficients;
    }

    public double [] getLightIntensities() {
        return lightIntensity;
    }

    public double getSourceDumping(){
        return sourceDumping;
    }

    public double getSurfaceCoefficient(){
        return surfaceCoefficient;
    }
    
    public double getBumpScale(){
        return bumpScale;
    }
}
