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
    }   

    private void addInputListeners(){
        addInputListener(view.kd,(Double kd) -> {
            rmodel.setDiffuseReflection(kd);
            scene.repaint();
        });
        addInputListener(view.ka,(Double ka) -> {
            rmodel.setAmbientReflection(ka);
            scene.repaint();
        });
        addInputListener(view.ks,(Double ks) -> {
            rmodel.setSpecularReflection(ks);
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
                }
            }
        });
    }
    private void addModelSelectListener() {
        view.modelSelect.addItemListener((ItemEvent e) -> model.setCurrentReflectionModel((PhongModel)e.getItem()));
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