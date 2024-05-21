package backend;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Random;

public class Quiz implements Serializable {
	
	private static final long serialVersionUID = -348125175644252486L;
	
	public final String quizName;
	
	private transient int currentQuestion = 0;
	private ArrayList<Question> questionList;

	protected static Random rgen = new Random();
	
	public Quiz(String name, ArrayList<Question> questions) {
		quizName = name;
		questionList = questions;
	}
	
	public ArrayList<Question> getQuestionList() {
		return questionList;
	}
	

	public void shuffleQuestions() {
		for (int i = questionList.size() - 1; i > 0; i--) {
			int idx = Quiz.rgen.nextInt(i + 1);
			if (idx != i) {
				// swap questions
				Question tmp = questionList.get(i);
				questionList.set(i, questionList.get(idx));
				questionList.set(idx, tmp);
			}
		}
	}
	

	public Question nextQuestion() {
		if (currentQuestion == questionList.size()) {
			return null;
		}
		return questionList.get(currentQuestion++);
	}
	

	public static Quiz read(String filename) throws IOException, ClassNotFoundException {
		FileInputStream fis = new FileInputStream(filename);
		ObjectInputStream ois = new ObjectInputStream(fis);
		Quiz q = (Quiz)ois.readObject();
		ois.close();
		fis.close();
		return q;
	}
	

	public void save(String filename) throws IOException {
		FileOutputStream fos = new FileOutputStream(filename);
		ObjectOutputStream oos = new ObjectOutputStream(fos);
		oos.writeObject(this);
		oos.close();
		fos.close();
	}

}