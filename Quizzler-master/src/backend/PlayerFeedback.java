package backend;

import java.io.Serializable;

public class PlayerFeedback implements Serializable {

	private static final long serialVersionUID = -3445887382336801372L;
	
	private String precedingPlayer;
	private int scoreDelta;
	private int position;
	private boolean wasCorrect;
	private Question question;
	

	public PlayerFeedback(String player, int delta, boolean wasCorrect, int position, Question question) {
		precedingPlayer = player;
		scoreDelta = delta;
		this.wasCorrect = wasCorrect;
		this.position = position;
		this.question = question;
	}
	
	public Question getQuestion() {
		return question;
	}
	
	public int getPosition() {
		return position;
	}
	
	public boolean answerWasCorrect() {
		return wasCorrect;
	}
	
	public String getPrecedingPlayer() {
		return precedingPlayer;
	}
	
	public int getScoreDelta() {
		return scoreDelta;
	}

}