import javax.swing.*;
import javax.swing.event.*;
import java.awt.*;
import java.awt.event.*;
import java.util.regex.*;
public class LocalLightingView extends JFrame{

    private Scene scene =null;
    public JTextField kd,ka,ks,ia,ip,f,n,b =null;
    public JComboBox modelSelect, channelSelect;
    private LocalLightingModel model=null;
    private int displayedChanel = 0;
    public LocalLightingView (LocalLightingModel model) {
        super();
        scene = new Scene(model.getCurrentReflectionModel());
        this.model = model;
        buildLayout();
        updateParamsDisplay();
        add(scene, BorderLayout.CENTER);
        setVisible(true);
        setTitle("Miedź");
        
    }
    private JTextField buildMenuInput(String label, JPanel sideMenu){
        JTextField txt = new JTextField();
        txt.setMaximumSize(new Dimension(Integer.MAX_VALUE, txt.getPreferredSize().height));
        sideMenu.add(new  JLabel(label));
        sideMenu.add(Box.createVerticalStrut(5));
        sideMenu.add(txt);
        return txt;
    }
    private JComboBox addSelect(JPanel sideMenu, Object[] models){
        
        JComboBox combo = new JComboBox(models);
        combo.setMaximumSize(new Dimension(Integer.MAX_VALUE, combo.getPreferredSize().height));
        sideMenu.add(Box.createVerticalStrut(5));
        sideMenu.add(combo);
        return combo;
    }
    private void buildLayout() {
        setSize(850,400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        JPanel sideMenu = new JPanel();
        sideMenu.setBackground(Color.LIGHT_GRAY);
        sideMenu.setPreferredSize(new Dimension(200, 0));
        sideMenu.setLayout(new BoxLayout(sideMenu, BoxLayout.Y_AXIS));
        modelSelect=addSelect(sideMenu,model.getReflectionModels());
        channelSelect = addSelect(sideMenu,model.CHANNEL_LABELS);
        sideMenu.add(Box.createVerticalStrut(5));
        kd = buildMenuInput("Wsp. odbicia św. rozprosz.:", sideMenu);
        ka = buildMenuInput("Wsp. odbicia św. z otoczenia:", sideMenu);
        ks = buildMenuInput("Wsp. odbicia św. kierunkowego:", sideMenu);
        ip = buildMenuInput("Natężenie św. punktowego:", sideMenu);
        ia = buildMenuInput("Natężenie św. z otoczenia:", sideMenu);
        f = buildMenuInput("Wsp. tłumienia św. z odległ.:", sideMenu);
        n = buildMenuInput("Wsp. gładkości powierzchni:", sideMenu);
        b = buildMenuInput("Zaburzenie wektora N:", sideMenu);
        add(sideMenu, BorderLayout.LINE_END);
    }

    public void setDisplayedChannel(int ch){
        displayedChanel = ch;
        updateParamsDisplay();
    }
    public int getDisplayedChannel(){
        return displayedChanel;
    }
    public void updateParamsDisplay(){
        double [][] k = ((PhongModel)model.getCurrentReflectionModel()).getReflectionCoefficients();
        double [] i = ((PhongModel)model.getCurrentReflectionModel()).getLightIntensities();
        double fValue = ((PhongModel)model.getCurrentReflectionModel()).getSourceDumping();
        double nValue = ((PhongModel)model.getCurrentReflectionModel()).getSurfaceCoefficient();
        double bs = ((PhongModel)model.getCurrentReflectionModel()).getBumpScale();
        ka.setText(""+k[displayedChanel][0]);
        kd.setText(""+k[displayedChanel][1]);
        ks.setText(""+k[displayedChanel][2]);
        ia.setText(""+i[0]);
        ip.setText(""+i[1]);
        f.setText(""+fValue);
        n.setText(""+ nValue);
        b.setText(""+bs);
    }
    public Scene getScene() {
        return this.scene;
    }
    
}