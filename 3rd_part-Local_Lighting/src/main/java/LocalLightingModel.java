public class LocalLightingModel {

    private ReflectionModel [] reflectionModels;
    private ReflectionModel currentReflectionModel;
    public String[] CHANNEL_LABELS = {"Kanał R", "Kanał G", "Kanał B"};
    public LocalLightingModel() {
        reflectionModels = new ReflectionModel[] {
            new PhongModel(),
            new PhongBlinnModel()
        };
        currentReflectionModel = reflectionModels[0];
    }   
    public ReflectionModel getCurrentReflectionModel(){
        return currentReflectionModel;
    }

    public ReflectionModel [] getReflectionModels(){
        return reflectionModels;
    }

    public void setCurrentReflectionModel(ReflectionModel model) {
        currentReflectionModel = model;
    }
}