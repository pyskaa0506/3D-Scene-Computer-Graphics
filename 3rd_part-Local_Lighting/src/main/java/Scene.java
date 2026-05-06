import java.awt.*;
import javax.swing.*;
import java.awt.image.BufferedImage;
public class Scene extends JPanel {

    private double [] sphere = new double [] {400,200,0,70};
    private PhongModel lightingModel = null;
    
    public Scene (PhongModel model){
        lightingModel = model;
        lightingModel.setScene(sphere);

    }

    public PhongModel getLightingModel(){
        return lightingModel;
    } 
    
    public void renderScene(Graphics2D graphics){
        int w = getWidth(), h = getHeight();
        sphere[0] = w/2;
        sphere[1] = h/2;
        BufferedImage img = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
        int radius = (int)sphere[3];
        for (int y = -radius; y < radius;y++){
            int color = 0xFFFFFF;
            for (int x = -radius; x < radius;x++){
                int distSq = x*x + y*y;

                if(distSq <= radius*radius) {
                    double z = Math.sqrt(radius * radius - distSq);
                    float brightness = (float)lightingModel.getValue(x/(double)radius,y/(double)radius,z/(double)radius);
                    color = Color.HSBtoRGB(0.0875f,1f,brightness);
                    img.setRGB((int)(sphere[0]+x), (int)(sphere[1]+y), color);
                }
                
            }
        }
        graphics.drawImage(img, 0, 0, null);

    }

    @Override
    public void paintComponent(Graphics comp) {
        super.paintComponent(comp);
        Graphics2D comp2D = (Graphics2D) comp;
        renderScene(comp2D);
    }

}