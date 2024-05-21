package frontend;

import backend.View;
import backend.WindowHandler;


public class Main {

	private WindowHandler wh;

	private MainMenu mainMenu;

	private ServerView serverView;
	private ClientView clientView;
	private QuizEditor quizEditor;
	private AboutWindow aboutWindow;

	public Main() {
		wh = new WindowHandler();

		mainMenu = new MainMenu(this);
		aboutWindow = new AboutWindow();

		serverView = new ServerView();
		serverView.addWindowListener(wh);

		clientView = new ClientView(this);

		quizEditor = new QuizEditor();

		mainMenu.setVisible(true);

		// ensure that server and client are closed when the
		// program exits
		Runtime.getRuntime().addShutdownHook(new Thread() {
			public void run() {
				serverView.closeServer();
				clientView.closeClient();
			}
		});
	}
  

	public void showView(View v) {
		switch (v) {
			case CLIENT_MODE:
				clientView.setVisible(true);
				break;
			case MAIN_MENU:
				mainMenu.setVisible(true);
				break;
			case QUIZ_EDITOR:
				quizEditor.setVisible(true);
				break;
			case SERVER_MODE:
				serverView.startServer(1616, mainMenu.getQuiz());
				serverView.setVisible(true);
				break;
			case ABOUT_WINDOW:
				aboutWindow.setVisible(true);
				break;
			default:
				break;
		}
	}

	public boolean serverIsRunning() {
		return serverView.stillRunning();
	}

	public static void main(String[] args) {
		new Main();
	}

}