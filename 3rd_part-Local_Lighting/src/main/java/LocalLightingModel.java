public class LocalLightingModel {

    private PhongModel [] reflectionModels;
    private PhongModel currentReflectionModel;
    public String[] CHANNEL_LABELS = {"Kanał R", "Kanał G", "Kanał B"};
    public LocalLightingModel() {
        reflectionModels = new PhongModel[] {
            new PhongModel(),
            new PhongBlinnModel()
        };
        currentReflectionModel = reflectionModels[0];
    }   
    public PhongModel getCurrentReflectionModel(){
        return currentReflectionModel;
    }

    public PhongModel [] getReflectionModels(){
        return reflectionModels;
    }

    public void setCurrentReflectionModel(PhongModel model) {
        currentReflectionModel = model;
    }
}