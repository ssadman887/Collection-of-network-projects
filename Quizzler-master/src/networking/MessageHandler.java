package networking;


public interface MessageHandler {

	public void handleMessage(String msg, String username);

	public void log(String msg);

}