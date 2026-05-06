import javax.swing.*;
import java.awt.event.*;
import java.util.regex.*;
import javax.swing.event.*;
import java.util.function.Consumer;
public class InterfaceController {

    private LocalLightingView view = null;
    private LocalLightingModel model = null;
    private Scene scene = null;
    private PhongModel rmodel = null;
    private int SOURCE_STEP = 20;

    public InterfaceController(LocalLightingModel model, LocalLightingView view){
        this.model=model;
        this.rmodel = model.getCurrentReflectionModel();
        this.view = view;
        this.scene = view.getScene();
        addLightSourceControl();
        addInputListeners();
        addSelectListeners();
    }   

    private void addInputListeners(){
        addInputListener(view.kd,(Double kd) -> {
            rmodel.setDiffuseReflection(kd, view.getDisplayedChannel());
            scene.repaint();
        });
        addInputListener(view.ka,(Double ka) -> {
            rmodel.setAmbientReflection(ka, view.getDisplayedChannel());
            scene.repaint();
        });
        addInputListener(view.ks,(Double ks) -> {
            rmodel.setSpecularReflection(ks, view.getDisplayedChannel());
            scene.repaint();
        });
        addInputListener(view.ia,(Double ia) -> {
            rmodel.setAmbientIntensity(ia);
            scene.repaint();
        });
        addInputListener(view.ip,(Double ip) -> {
            rmodel.setSourceIntensity(ip);
            scene.repaint();
        });
        addInputListener(view.n,(Double n) -> {
            rmodel.setSurfaceCoefficient(n);
            scene.repaint();
        });
        addInputListener(view.f,(Double f) -> {
            rmodel.setSourceDumping(f);
            scene.repaint();
        });
        addInputListener(view.b, (Double b) -> {
            rmodel.setBumpScale(b);
            scene.repaint();
        });
    }
    private void addInputListener(JTextField input, Consumer<Double> func) {
        input.getDocument().addDocumentListener(new DocumentListener() {
    
            @Override
            public void insertUpdate(DocumentEvent e) {
                updateAction();
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                updateAction();
            }

            // Wywoływane przy zmianie stylu (rzadko używane w zwykłym JTextField)
            public void changedUpdate(DocumentEvent e) {
                updateAction();
            }

            // Wspólna metoda dla wszystkich zmian
            private void updateAction() {
                String currentText = input.getText();
                if(validateInput(currentText))
                    func.accept(Double.valueOf(currentText));     
            }

        });
        
    }
    private void addLightSourceControl(){
        view.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                view.requestFocusInWindow(); // Kliknięcie w tło zabiera fokus z pola
            }
        });
        view.addKeyListener(new KeyAdapter(){
            @Override
            public void keyPressed(KeyEvent e){
                switch(e.getKeyCode()){
                        case KeyEvent.VK_UP : moveSourceUp() ; break;
                        case KeyEvent.VK_DOWN : moveSourceDown(); break;
                        case KeyEvent.VK_RIGHT : moveSourceRight(); break;
                        case KeyEvent.VK_LEFT : moveSourceLeft(); break;
                        case KeyEvent.VK_1 : {
                            rmodel.setReflectionCoefficients(PhongConstants.K_COPPER);
                            rmodel.setSurfaceCoefficient(PhongConstants.N_COPPER);
                            view.setDisplayedChannel(0);
                            scene.repaint();
                            view.setTitle("Miedź");
                            break;
                        }
                        case KeyEvent.VK_2 : {
                            rmodel.setReflectionCoefficients(PhongConstants.K_GOLD);
                            rmodel.setSurfaceCoefficient(PhongConstants.N_GOLD);
                            scene.repaint();
                            view.setDisplayedChannel(0);
                            view.setTitle("Złoto");
                            break;
                        }
                        case KeyEvent.VK_3 : {
                            rmodel.setReflectionCoefficients(PhongConstants.K_SILVER);
                            rmodel.setSurfaceCoefficient(PhongConstants.N_SILVER);
                            scene.repaint();
                            view.setDisplayedChannel(0);
                            view.setTitle("Srebro");
                            break;
                        }
                
                }
            }
        });
    }
    private void addSelectListeners() {
        view.modelSelect.addItemListener((ItemEvent e) -> model.setCurrentReflectionModel((PhongModel)e.getItem()));
        view.channelSelect.addItemListener((ItemEvent e) -> {
            char channelId = ((String)e.getItem()).charAt(6);
            switch(channelId){
                case 'R' : view.setDisplayedChannel(0); break;
                case 'G' : view.setDisplayedChannel(1); break;
                case 'B' : view.setDisplayedChannel(2); break;
            }
            
            }
        );
    }
    private void moveSourceUp() {
        int [] srcPos = rmodel.getSourcePosition();
        srcPos[1]= Math.max(0,srcPos[1]-SOURCE_STEP);
        rmodel.setSourcePosition(srcPos);
        scene.repaint();
    }
    private void moveSourceDown() {
        int [] srcPos =rmodel.getSourcePosition();
        srcPos[1]= srcPos[1]+SOURCE_STEP;
        rmodel.setSourcePosition(srcPos);
        scene.repaint();
    }
    private void moveSourceBack() {
        int [] srcPos = rmodel.getSourcePosition();
        srcPos[2]= srcPos[2]+SOURCE_STEP;
        rmodel.setSourcePosition(srcPos);
        scene.repaint();
    }
    private void moveSourceForth() {
        int [] srcPos = rmodel.getSourcePosition();
        srcPos[2]= Math.min(0,srcPos[2]-SOURCE_STEP);
        rmodel.setSourcePosition(srcPos);
        scene.repaint();
    }
    private void moveSourceLeft() {
        int [] srcPos = rmodel.getSourcePosition();
        srcPos[0]= Math.max(0,srcPos[0]-SOURCE_STEP);
        rmodel.setSourcePosition(srcPos);
        scene.repaint();
    }
    private void moveSourceRight() {
        int [] srcPos = rmodel.getSourcePosition();
        srcPos[0]= srcPos[0]+SOURCE_STEP;
        rmodel.setSourcePosition(srcPos);
        scene.repaint();
    }
    private boolean validateInput(String input){
        Pattern pattern = Pattern.compile("(([0-9]+[.][0-9]+)|([0-9]+)$)");
        Matcher matcher = pattern.matcher(input);
        return matcher.matches();
    }
    

}