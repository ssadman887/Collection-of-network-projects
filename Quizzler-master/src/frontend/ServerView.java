package frontend;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileWriter;
import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.URL;
import java.net.UnknownHostException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.FileHandler;
import java.util.logging.Handler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import javax.swing.*;

//import org.apache.commons.csv.CSVFormat;
//import org.apache.commons.csv.CSVPrinter;

import backend.GameState;
import backend.LeaderboardModel;
import backend.PlayerFeedback;
import backend.Question;
import backend.Quiz;
import backend.Updatable;
import backend.Updater;
import networking.AcceptThread;
import networking.ClientHandler;
import networking.MessageHandler;
import networking.NetworkMessages;


public class ServerView extends JFrame implements MessageHandler, ActionListener, Updatable {

	private static final long serialVersionUID = -6532875835478176408L;

	// networking
	private int portNum;
	private ServerSocket serverSocket;

	private ArrayList<ClientHandler> clientArray;
	private List<String> dataHeaders;
	private Map<String, List<String>> clientData;
	private Map<String, Boolean> wasCorrect;
	private int answersReceived = 0;

	private AcceptThread acceptThread;
	private Thread gameThread;
	private boolean isRunning = false;
	private GameState currentState = GameState.WAITING_FOR_PLAYERS;

	// quiz data
	private LeaderboardModel leaderboardModel;
	private JTable leaderboard;
	private QuestionAnalysis qa;

	private Quiz quiz;
	private Question currentQuestion;
	private int timeRemaining;
	private int receivableScore;
	private int answerCount[] = { 0, 0, 0, 0 };
	private int questionCount;

	// game settings
	private JCheckBox enableMusic;
	private JCheckBox enableAShuffle;
	private JCheckBox enableQShuffle;

	// UI elements
	private JTabbedPane tab;
	private JScrollPane scrollPane;

	private JLabel lblQuizName;

	private JLabel lblCurrentQ;

	private JLabel lblA;
	private JLabel lblB;
	private JLabel lblC;
	private JLabel lblD;
	private JLabel[] answers;

	private JLabel lblTime;
	private JButton btnNext;

	private JLabel lblEvent;
	private JPanel southPanel;

	private JButton btnKickUser;

	// music
	private Clip music;
	private static final String qClips[] = { "Fastest.wav", "Faster.wav", "Fast.wav", "Middle.wav", "Slow.wav",
			"Slower.wav", "Slowest.wav" };
	private String lastClip = "";

	// logging
	private Logger logger = Logger.getLogger("ServerLog");
	private String logDate;

	public ServerView() {
		setTitle("Quizzler: Hosting Game");
		setBounds(1000, 200, 700, 500);

		JPanel panel_1 = new JPanel();
		getContentPane().add(panel_1, BorderLayout.NORTH);
		panel_1.setLayout(new GridLayout(0, 1, 0, 0));
		panel_1.setBackground(Color.white);

		lblQuizName = new JLabel("New label");
		lblQuizName.setHorizontalAlignment(SwingConstants.CENTER);
		panel_1.add(lblQuizName);

		lblCurrentQ = new JLabel("No Question Yet");
		lblCurrentQ.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 30));
		lblCurrentQ.setHorizontalAlignment(SwingConstants.CENTER);
		panel_1.add(lblCurrentQ);

		JPanel panel_2 = new JPanel();
		panel_1.add(panel_2);
		panel_2.setLayout(new GridLayout(2, 2, 0, 0));
		panel_2.setBackground(Color.white);

		lblA = new JLabel("A.");
		lblA.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 16));
		lblA.setHorizontalAlignment(SwingConstants.CENTER);
		panel_2.add(lblA);

		lblB = new JLabel("B.");
		lblB.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 16));
		lblB.setHorizontalAlignment(SwingConstants.CENTER);
		panel_2.add(lblB);

		lblC = new JLabel("C.");
		lblC.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 16));
		lblC.setHorizontalAlignment(SwingConstants.CENTER);
		panel_2.add(lblC);

		lblD = new JLabel("D.");
		lblD.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 16));
		lblD.setHorizontalAlignment(SwingConstants.CENTER);
		panel_2.add(lblD);

		answers = new JLabel[] { lblA, lblB, lblC, lblD };

		tab = new JTabbedPane();
		getContentPane().add(tab, BorderLayout.CENTER);
		getContentPane().setBackground(Color.white);
		tab.setBackground(Color.white);

		scrollPane = new JScrollPane();
		scrollPane.setBackground(Color.white);
		tab.addTab("Leaderboard", scrollPane);

		leaderboardModel = new LeaderboardModel();
		leaderboard = new JTable(leaderboardModel);
		leaderboard.setBackground(Color.white);
		leaderboard.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		scrollPane.setViewportView(leaderboard);

		qa = new QuestionAnalysis();
		tab.addTab("Stats", qa);
		tab.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));


		JPanel settings = new JPanel();
		tab.addTab("Game Settings", settings);
		settings.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));


		settings.setLayout(new GridLayout(0, 1, 0, 0));
		settings.setBackground(Color.white);

		enableMusic = new JCheckBox("Enable music");
		enableMusic.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));

		enableMusic.setSelected(false);				// to enable or disable...
		enableMusic.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				if (((JCheckBox) e.getSource()).isSelected()) {
					loadSound();
				} else {
					music.close();
				}
			}
		});
		settings.add(enableMusic);

		enableAShuffle = new JCheckBox("Shuffle answers (takes effect next question)");
		enableAShuffle.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));

		//settings.add(enableAShuffle);

		enableQShuffle = new JCheckBox("Shuffle questions (cannot be changed after game start)");
		enableQShuffle.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));

		//settings.add(enableQShuffle);

		JPanel panel = new JPanel();
		getContentPane().add(panel, BorderLayout.EAST);
		panel.setLayout(new GridLayout(0, 1, 0, 0));
		panel.setBackground(Color.white);

		lblTime = new JLabel("60");
		lblTime.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 50));
		lblTime.setHorizontalAlignment(SwingConstants.CENTER);
		panel.add(lblTime);

		btnNext = new JButton("Begin!");
		btnNext.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		btnNext.setBackground(new Color(250, 250, 210));
		panel.add(btnNext);
		btnNext.addActionListener(this);



		southPanel = new JPanel();
		getContentPane().add(southPanel, BorderLayout.SOUTH);
		southPanel.setLayout(new GridLayout(1, 0, 0, 0));

		lblEvent = new JLabel("The Quiz is starting soon...");	// Nothing eventful yet
		lblEvent.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 17));
		southPanel.add(lblEvent);

		btnKickUser = new JButton("Kick User");
		btnKickUser.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		btnKickUser.setBackground(new Color(250, 250, 210));

		btnKickUser.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				kickSelectedUser();
			}
		});

		try {
			music = AudioSystem.getClip();
		} catch (LineUnavailableException e) {
			e.printStackTrace();
		}

		logger.setUseParentHandlers(false);
	}


	private void loadSound() {
		if (lastClip.length() > 0) {
			loadResourceSound(lastClip);
		}
	}


	private void loadResourceSound(String sound) {
		loadSound(ServerView.class.getResource("/sound/" + sound));
		lastClip = sound;
	}


	private void loadSound(URL sound) {
		if (enableMusic.isSelected()) {
			try {
				music.open(AudioSystem.getAudioInputStream(sound));
				music.start();
				music.loop(Clip.LOOP_CONTINUOUSLY);
			} catch (LineUnavailableException | IOException | UnsupportedAudioFileException e) {
				e.printStackTrace();
			}
		}
	}


	public void startServer(int givenPort, Quiz givenQuiz) {
		if (isRunning) {
			return;
		}
		isRunning = true;

		quiz = givenQuiz;
		lblQuizName.setText(quiz.quizName);
		lblQuizName.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 20));

		try {
			lblCurrentQ.setText("IP: " + InetAddress.getLocalHost().getHostAddress());
			lblCurrentQ.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 30));

		} catch (UnknownHostException e) {
			lblCurrentQ.setText("Failed to get IP address");
			lblCurrentQ.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));

		}

		lblA.setText("Option - A");
		lblA.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));

		lblB.setText("Option - B");
		lblB.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));

		lblC.setText("Option - C");
		lblC.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));

		lblD.setText("Option - D");
		lblD.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));


		btnNext.setText("Begin!");

		loadResourceSound("Theme.wav");	// to disable music....

		enableQShuffle.setEnabled(true);
		southPanel.add(btnKickUser);

		// start logging
		try {
			DateFormat df = new SimpleDateFormat("yyyy-MM-dd HH.mm.ss");
			logDate = df.format(new Date());
			FileHandler fh = new FileHandler(logDate + ".log");
			fh.setFormatter(new SimpleFormatter());
			logger.addHandler(fh);
		} catch (SecurityException | IOException e) {
			e.printStackTrace();
		}

		logger.info("Started server with quiz: " + quiz.quizName);

		clientArray = new ArrayList<ClientHandler>();
		portNum = givenPort;
		// Listens for socket
		try {
			serverSocket = new ServerSocket(portNum);
		} catch (IOException e1) {
			logger.severe("Failed to create socket");
			return;
		}
		acceptThread = new AcceptThread(serverSocket, this);
		acceptThread.start();
	}

	public void closeServer() {
		if (clientArray == null) {
			return;
		}
		isRunning = false;
		currentState = GameState.WAITING_FOR_PLAYERS;
		for (ClientHandler ch : clientArray) {
			ch.send(NetworkMessages.userKicked);
			ch.send("Server shutting down");
			ch.stopRunning();
		}
		clientArray.clear();
		clientArray = null;
		music.close();
		leaderboardModel.clear();
		try {
			serverSocket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		logger.info("Closed server");
		for (Handler h : logger.getHandlers()) {
			h.close();
			logger.removeHandler(h);
		}
		if (questionCount > 0) {
			//			try {
//				CSVPrinter csvprinter = new CSVPrinter(new FileWriter(logDate + ".csv"), CSVFormat.DEFAULT);
//				csvprinter.printRecord(dataHeaders);
//				for (Map.Entry<String, List<String>> entry : clientData.entrySet()) {
//					csvprinter.print(entry.getKey());
//					csvprinter.printRecord(entry.getValue());
//					csvprinter.println();
//				}
//				csvprinter.close();
//			} catch (IOException e) {
//				e.printStackTrace();
//			}
		}
	}

	private void backToMain() {
		setVisible(false);
	}


	private void kickSelectedUser() {
		int selectedUser = leaderboard.getSelectedRow();
		if (selectedUser >= 0) {
			String username = (String) leaderboardModel.getValueAt(selectedUser, 0);
			leaderboardModel.removePlayer(selectedUser);
			int i = 0;
			for (; i < clientArray.size(); i++) {
				if (clientArray.get(i).username.equals(username)) {
					break;
				}
			}
			ClientHandler ch = clientArray.get(i);
			logger.info("Kicked user " + username + " from IP " + ch.getIP());
			ch.send(NetworkMessages.userKicked);
			ch.send("Kicked by server owner");
			ch.stopRunning();
			clientArray.remove(i);
		}
	}


	public void addClientHandler(ClientHandler clientHandler) {
		for (ClientHandler ch : clientArray) {
			if (ch.getIP().equals(clientHandler.getIP())) {
				logger.warning("User from IP " + ch.getIP() + " tried to connect twice as " + ch.username + " and "
						+ clientHandler.username);
				clientHandler.send(NetworkMessages.userKicked);
				clientHandler.send("Only one connection per machine");
				clientHandler.stopRunning();
				return;
			}
		}
		logger.info(clientHandler.username + " from IP " + clientHandler.getIP() + " joined the game");
		leaderboardModel.addPlayer(clientHandler.username, 0);
		clientArray.add(clientHandler);
		sendToClient(clientHandler.username, NetworkMessages.userAccepted);
	}


	private void broadcastToClients(Object obj) {
		for (ClientHandler ch : clientArray) {
			ch.send(obj);
		}
	}


	private void sendToClient(String username, String text) {
		for (ClientHandler ch : clientArray) {
			if (ch.username.equals(username)) {
				ch.send(text);
				return;
			}
		}
	}

	@Override
	public void handleMessage(String msg, String username) {
		if (currentState == GameState.WAITING_FOR_ANSWERS) {
			try {
				int chosen = Integer.parseInt(msg);
				String feedback = "X ";
				answerCount[chosen]++;
				if (currentQuestion.acceptAnswer(chosen)) {
					wasCorrect.put(username, true);
					feedback = "/ ";
					leaderboardModel.changeScore(username, receivableScore);
					receivableScore *= 0.9;
				}
				clientData.get(username).add(feedback + currentQuestion.getAnswers().get(chosen));
				logger.info(username + " chose answer " + msg);
			} catch (NumberFormatException e) {
				logger.warning("Invalid answer provided by " + username);
			}
			answersReceived++;
			if (answersReceived >= clientArray.size()) {
				timeRemaining = 0;
			}
		}
	}


	private void startGame() {
		acceptThread.running = false;
		gameThread = new Thread(new Updater(this, 1));
		gameThread.start();

		southPanel.remove(btnKickUser);
		lblEvent.setText("The Quiz is running...");
		leaderboardModel.initializeDeltas();
		wasCorrect = new HashMap<String, Boolean>();

		dataHeaders = new ArrayList<String>();
		dataHeaders.add("Name");
		clientData = new HashMap<String, List<String>>();

		if(clientArray.size() == 0) {
			JOptionPane.showMessageDialog(this, "No such participation. Please wait to others join.",
					"Ensure Participation!", JOptionPane.ERROR_MESSAGE);
		}

			for (ClientHandler ch : clientArray) {
			clientData.put(ch.username, new ArrayList<String>());
		}

		if (enableQShuffle.isSelected()) {
			quiz.shuffleQuestions();
		}
		enableQShuffle.setEnabled(false);

		logger.info("Started game");
		questionCount = 0;

		getNextQuestion();
	}

	public void update() {
		if (currentState == GameState.WAITING_FOR_ANSWERS) {
			timeRemaining--;
			if (timeRemaining <= 0) {
				actionPerformed(null);
			}
			if(timeRemaining == -1) timeRemaining = 0;
			lblTime.setText(Integer.toString(timeRemaining));
		}
	}

	public boolean stillRunning() {
		return isRunning;
	}

	private boolean getNextQuestion() {
		currentQuestion = quiz.nextQuestion();
		questionCount++;
		for (int i = 0; i < 4; i++) {
			answerCount[i] = 0;
		}
		wasCorrect.clear();
		if (currentQuestion == null) {
			logger.info("No more questions remaining");
			broadcastToClients(NetworkMessages.gameOver);
			currentState = GameState.GAME_OVER;
			return false;
		}
		broadcastToClients(NetworkMessages.nextQ);
		if (enableAShuffle.isSelected()) {
			currentQuestion.shuffleAnswers();
		}
		broadcastToClients(currentQuestion.getSendableCopy());
		dataHeaders.add(currentQuestion.getQ() + " (" + currentQuestion.getCorrectAnswers() + ")");
		logger.info("Moving to next question: " + currentQuestion.getQ());

		lblCurrentQ.setText(currentQuestion.getQ());
		int index = 0;
		for (String ans : currentQuestion.getAnswers()) {
			answers[index].setText(ans);
			index++;
		}
		answersReceived = 0;
		timeRemaining = currentQuestion.getTimeLimit();
		receivableScore = currentQuestion.getPoints();
		lblTime.setText(Integer.toString(timeRemaining));
		currentState = GameState.WAITING_FOR_ANSWERS;

		music.close();
		if (timeRemaining < 30) {
			loadResourceSound(qClips[timeRemaining / 5]);
		} else {
			loadResourceSound(qClips[6]);
		}
		return true;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		switch (currentState) {
		case WAITING_FOR_ANSWERS:
			logger.info("Skipping remaining time for question");
			tab.setSelectedComponent(qa);
			currentState = GameState.WAITING_FOR_NEXT_Q;
			music.close();
			broadcastToClients(NetworkMessages.timeup);
			leaderboardModel.updateData();
			Map<String, PlayerFeedback> feedback = leaderboardModel.getFeedback(wasCorrect, currentQuestion);
			for (ClientHandler ch : clientArray) {
				ch.send(feedback.get(ch.username));
				List<String> answers = clientData.get(ch.username);
				if (answers.size() < questionCount) {
					answers.add("X");
				}
			}
			qa.loadData(currentQuestion, answerCount);
			btnNext.setText("Next");
			break;
		case WAITING_FOR_PLAYERS:
			startGame();
			currentState = GameState.WAITING_FOR_ANSWERS;
			btnNext.setText("Skip");
			break;
		case GAME_OVER:
			logger.info("Ending game");
			closeServer();
			backToMain();
			break;
		case WAITING_FOR_NEXT_Q:
			tab.setSelectedComponent(scrollPane);
			if (getNextQuestion()) {
				btnNext.setText("Skip");
			} else {
				btnNext.setText("Exit");
			}
			break;
		default:
			break;
		}
	}

	public void log(String msg) {
		logger.info(msg);
	}

}