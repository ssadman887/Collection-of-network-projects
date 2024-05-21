package backend;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


public class Question implements Serializable {

	private static final long serialVersionUID = 876478610869525268L;
	
	public transient static final String keyHasImage = "hasImageData";
	public transient static final String keyImageData = "imageData";
	
	private int points;
	private int timeLimit;
	private String question;
	private ArrayList<String> answers;
	private boolean[] acceptableAnswers;
	
	private Map<String, Object> multimediaData;
	

	public Question(String question, int time, int points, ArrayList<String> ans, boolean[] okAns) throws IOException {
		this.question = question;
		this.points = points;
		timeLimit = time;
		answers = ans;
		acceptableAnswers = okAns;
		multimediaData = new HashMap<String, Object>();
	}
	
	public Object getMultimediaDataForKey(String key, Object def) {
		return multimediaData.getOrDefault(key, def);
	}
	
	public void setMultimediaDataForKey(String key, Object obj) {
		multimediaData.put(key, obj);
	}
	

	public Question getSendableCopy() {
		try {
			Question q = new Question(question, timeLimit, points, answers, new boolean[] {});
			for (Map.Entry<String, Object> entry : multimediaData.entrySet()) {
				q.setMultimediaDataForKey(entry.getKey(), entry.getValue());
			}
			return q;
		} catch (IOException e) {
			return null;
		}
	}
	

	public void shuffleAnswers() {
		for (int i = 3; i > 0; i--) {
			int idx = Quiz.rgen.nextInt(i + 1);
			if (idx != i) {
				// swap acceptable answers
				acceptableAnswers[i] ^= acceptableAnswers[idx];
				acceptableAnswers[idx] ^= acceptableAnswers[i];
				acceptableAnswers[i] ^= acceptableAnswers[idx];
				
				// swap text
				String tmp = answers.get(i);
				answers.set(i, answers.get(idx));
				answers.set(idx, tmp);
			}
		}
	}
	

	public boolean acceptAnswer(int ans) {
		return acceptableAnswers[ans];
	}
	
	public String getCorrectAnswers() {
		String ans = "";
		int i = 0;
		int correct = 0;
		for (boolean ok : acceptableAnswers) {
			if (ok) {
				if (correct > 0) {
					ans = ans.concat("/");
				}
				correct++;
				ans = ans.concat(answers.get(i));
			}
			i++;
		}
		return ans;
	}
	
	public String getQ() {
		return question;
	}
	
	public ArrayList<String> getAnswers() {
		return answers;
	}
	
	public int getPoints() {
		return points;
	}
	
	public int getTimeLimit() {
		return timeLimit;
	}
	
	public String toString() {
		String str = question + " (";
		for (int i = 0; i < 4; i++) {
			str = str.concat(answers.get(i) + (i < 3 ? "," : ") "));
		}
		str = str.concat(timeLimit + "s, " + points + " pts");
		return str;
	}

}