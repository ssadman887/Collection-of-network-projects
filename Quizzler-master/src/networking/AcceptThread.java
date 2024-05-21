package networking;

import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;

import frontend.ServerView;


public class AcceptThread extends Thread{
    
    public boolean running = true;
    
    private ServerSocket sock;
    private ServerView server;
    
    public AcceptThread(ServerSocket sock, ServerView server){
        this.sock = sock;
        this.server = server;
    }
    
    public void run(){
        while (running){
            try {
            		// accept new client
                Socket cSock = sock.accept();
                server.addClientHandler(new ClientHandler(cSock, server));
            } catch (SocketException e){
                if (e.getMessage().equals("Socket closed")){
                    running = false;
                    break;
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    
}