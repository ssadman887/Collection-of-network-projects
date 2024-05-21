package networking;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;

import frontend.ServerView;


public class ClientHandler {
	private Socket sock;
	
	public ObjectOutputStream oout;
	public ObjectInputStream oin;
	public MsgThread msgThread;
	public String username;
	
	private String ipAddress;


	public ClientHandler(Socket clientSocket, ServerView server) {
		try {
			sock = clientSocket;
			ipAddress = clientSocket.getInetAddress().toString();
			oout = new ObjectOutputStream(clientSocket.getOutputStream());
			oin = new ObjectInputStream(clientSocket.getInputStream());
			username = (String) oin.readObject();
			msgThread = new MsgThread(oin, username, server);
			msgThread.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public String getIP() {
		return ipAddress;
	}


	public void send(Object obj) {
		try {
			oout.reset();
			oout.writeObject(obj);
			oout.flush();
		} catch (IOException e) {
		}
	}

	public void stopRunning() {
		msgThread.running = false;
		try {
			sock.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}