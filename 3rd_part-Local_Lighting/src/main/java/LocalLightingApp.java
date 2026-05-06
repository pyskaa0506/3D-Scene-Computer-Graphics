public class LocalLightingApp{

	
	public static void main(String args[]){

		LocalLightingModel model = new LocalLightingModel();
		LocalLightingView lv = new LocalLightingView(model);
		InterfaceController controller  = new InterfaceController(model, lv);
		
	}
}
