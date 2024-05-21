package networking;

import java.io.EOFException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.net.SocketException;

public class MsgThread extends Thread {

	public boolean running = true;

	private ObjectInputStream oin;
	private MessageHandler receiver;
	private String username;


	public MsgThread(ObjectInputStream oin, String username, MessageHandler receiver) {
		this.oin = oin;
		this.username = username;
		this.receiver = receiver;
	}

	public void run() {
		String inLine = "";
		while (running) {
			try {
				// read the message
				inLine = (String) oin.readObject();
				// disconnect if required, otherwise let MessageHandler handle it
				if (inLine.equals(NetworkMessages.disconnect)) {
					receiver.log(username + " disconnected");
					running = false;
				} else {
					receiver.handleMessage(inLine, username);
				}
			} catch (SocketException | EOFException e) {
				running = false;
			} catch (IOException e) {
				receiver.log("IOException from " + username);
			} catch (ClassNotFoundException | ClassCastException e) {
				receiver.log("Protocol error from " + username);
			}
		}
	}

}