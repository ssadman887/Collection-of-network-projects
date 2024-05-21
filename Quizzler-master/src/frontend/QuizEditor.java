package frontend;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import javax.imageio.ImageIO;
import javax.swing.*;

import backend.Question;
import backend.QuestionListModel;
import backend.Quiz;


public class QuizEditor extends JFrame implements ActionListener {

	private static final long serialVersionUID = 1125527090979758382L;

	private JTextField nameField;

	private JButton btnLoad;
	private JButton btnSave;

	private JTable questionList;
	private QuestionListModel qlistModel;

	private JTextField questionField;
	private JTextField ansA;
	private JTextField ansB;
	private JTextField ansC;
	private JTextField ansD;

	private JCheckBox aOK;
	private JCheckBox bOK;
	private JCheckBox cOK;
	private JCheckBox dOK;

	private JButton btnAddQuestion;
	private JButton btnRemoveQuestion;

	private File loadedImage;
	private JButton btnLoadImage;
	private JButton btnClearImage;
	private JPanel imagePanel;

	private JFileChooser jfc = new JFileChooser();

	private Quiz quiz;
	private boolean modified = false;
	private JTextField timeField;
	private JButton btnEditQuestion;
	private JTextField pointsField;

	private JPanel contentPane;

	public QuizEditor() {
		setTitle("Quizzler Quiz Editor");
		setBounds(500, 120, 1150, 800);
		getContentPane().setLayout(new GridLayout(0, 1, 0, 0));
		setBackground(Color.white);

		this.contentPane = (JPanel) getContentPane();

		JPanel panel_9 = new JPanel();
		getContentPane().add(panel_9);
		panel_9.setLayout(new GridLayout(0, 1, 0, 0));

		JPanel panel_11 = new JPanel();
		panel_9.add(panel_11);
		panel_11.setLayout(new GridLayout(0, 1, 0, 5));

		JPanel panel = new JPanel();
		panel_11.add(panel);
		panel.setLayout(new GridLayout(1, 0, 5, 0));

		JLabel lblQuizName = new JLabel("Quiz Name");
		lblQuizName.setBounds(100, 100, 150, 25);
		lblQuizName.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel.add(lblQuizName);

		nameField = new JTextField();
		nameField.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel.add(nameField);
		nameField.setColumns(10);

		btnSave = new JButton("Save");
		btnSave.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		btnSave.setBackground(new Color(250, 250, 210));
		btnSave.addActionListener(this);
		panel.add(btnSave);

		btnLoad = new JButton("Load");
		btnLoad.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		btnLoad.setBackground(new Color(250, 250, 210));
		btnLoad.addActionListener(this);
		panel.add(btnLoad);

		JPanel panel_10 = new JPanel();
		panel_11.add(panel_10);
		panel_10.setLayout(new BorderLayout(0, 0));

		JLabel lblQuestion = new JLabel("Question");
		lblQuestion.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_10.add(lblQuestion, BorderLayout.WEST);

		questionField = new JTextField();
		questionField.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_10.add(questionField);
		questionField.setColumns(10);

		JPanel panel_12 = new JPanel();
		panel_11.add(panel_12);
		panel_12.setLayout(new BorderLayout(0, 0));

		JLabel lblTime = new JLabel("Time			");
		lblTime.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_12.add(lblTime, BorderLayout.WEST);

		timeField = new JTextField();
		timeField.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_12.add(timeField, BorderLayout.CENTER);
		timeField.setColumns(10);

		JPanel panel_13 = new JPanel();
		panel_11.add(panel_13);
		panel_13.setLayout(new BorderLayout(0, 0));

		JLabel lblPoints = new JLabel("Max Points");
		lblPoints.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_13.add(lblPoints, BorderLayout.WEST);

		pointsField = new JTextField();
		pointsField.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_13.add(pointsField, BorderLayout.CENTER);
		pointsField.setColumns(10);

		JPanel superpanel_img = new JPanel();
		superpanel_img.setLayout(new GridLayout(1, 0, 0, 0));
		panel_9.add(superpanel_img);

		JPanel panel_img = new JPanel();
		superpanel_img.add(panel_img);
		panel_img.setLayout(new GridLayout(0, 1, 0, 5));

		btnLoadImage = new JButton("Add Image");
		btnLoadImage.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		btnLoadImage.setBackground(new Color(250, 250, 210));
		panel_img.add(btnLoadImage);
		btnLoadImage.addActionListener(this);

		btnClearImage = new JButton("Remove Image");
		btnClearImage.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		btnClearImage.setBackground(new Color(250, 250, 210));
		panel_img.add(btnClearImage);
		btnClearImage.addActionListener(this);

		imagePanel = new JPanel();
		imagePanel.setLayout(new GridLayout(1, 0, 0, 0));
		superpanel_img.add(imagePanel);

		JPanel panel_1 = new JPanel();
		panel_9.add(panel_1);
		panel_1.setLayout(new GridLayout(1, 0, 0, 0));

		JPanel panel_6 = new JPanel();
		panel_1.add(panel_6);
		panel_6.setLayout(new BorderLayout(0, 0));

		JPanel panel_2 = new JPanel();
		panel_6.add(panel_2, BorderLayout.WEST);
		panel_2.setLayout(new GridLayout(0, 1, 0, 0));

		JLabel lblA = new JLabel("A. ");
		lblA.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_2.add(lblA);

		JLabel lblB = new JLabel("B. ");
		lblB.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_2.add(lblB);

		JPanel panel_3 = new JPanel();
		panel_6.add(panel_3);
		panel_3.setLayout(new GridLayout(0, 1, 0, 0));

		ansA = new JTextField();
		ansA.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_3.add(ansA);
		ansA.setColumns(10);

		JPanel panel_ab = new JPanel();
		panel_ab.setLayout(new GridLayout(0, 1, 0, 0));

		aOK = new JCheckBox();
		panel_ab.add(aOK);
		bOK = new JCheckBox();
		panel_ab.add(bOK);

		panel_6.add(panel_ab, BorderLayout.EAST);

		ansB = new JTextField();
		ansB.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_3.add(ansB);
		ansB.setColumns(10);

		JPanel panel_7 = new JPanel();
		panel_1.add(panel_7);
		panel_7.setLayout(new BorderLayout(0, 0));

		JPanel panel_4 = new JPanel();
		panel_7.add(panel_4, BorderLayout.WEST);
		panel_4.setLayout(new GridLayout(0, 1, 0, 0));

		JLabel lblC = new JLabel("C. ");
		lblC.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_4.add(lblC);

		JLabel lblD = new JLabel("D. ");
		lblD.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_4.add(lblD);

		JPanel panel_5 = new JPanel();
		panel_7.add(panel_5);
		panel_5.setLayout(new GridLayout(0, 1, 0, 0));

		ansC = new JTextField();
		ansC.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_5.add(ansC);
		ansC.setColumns(10);

		ansD = new JTextField();
		ansD.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		panel_5.add(ansD);
		ansD.setColumns(10);

		JPanel panel_cd = new JPanel();
		panel_cd.setLayout(new GridLayout(0, 1, 0, 0));

		cOK = new JCheckBox();
		panel_cd.add(cOK);
		dOK = new JCheckBox();
		panel_cd.add(dOK);

		panel_7.add(panel_cd, BorderLayout.EAST);

		JPanel panel_8 = new JPanel();
		panel_1.add(panel_8);
		panel_8.setLayout(new GridLayout(0, 1, 0, 10));

		btnAddQuestion = new JButton("Add Question");
		btnAddQuestion.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		btnAddQuestion.setBackground(new Color(250, 250, 210));
		btnAddQuestion.addActionListener(this);
		panel_8.add(btnAddQuestion);

		btnRemoveQuestion = new JButton("Delete Selected Question");
		btnRemoveQuestion.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		btnRemoveQuestion.setBackground(new Color(250, 250, 210));
		btnRemoveQuestion.addActionListener(this);
		panel_8.add(btnRemoveQuestion);

		btnEditQuestion = new JButton("Edit Selected Question");
		btnEditQuestion.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		btnEditQuestion.setBackground(new Color(250, 250, 210));
		btnEditQuestion.addActionListener(this);
		panel_8.add(btnEditQuestion);

		qlistModel = new QuestionListModel();

		JScrollPane scrollPane = new JScrollPane();
		getContentPane().add(scrollPane);
		questionList = new JTable(qlistModel);
		scrollPane.setViewportView(questionList);
		scrollPane.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));

	}

	@Override
	public void actionPerformed(ActionEvent e) {
		if (e.getSource() == btnLoad) {
			// ask user to select a file and load the quiz
			if (jfc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
				try {
					quiz = Quiz.read(jfc.getSelectedFile().getAbsolutePath());
					nameField.setText(quiz.quizName);
					for (Question q : quiz.getQuestionList()) {
						qlistModel.addQuestion(q);
					}
					modified = false;
				} catch (ClassNotFoundException | IOException e1) {
					JOptionPane.showMessageDialog(null, "Failed to load quiz");
				}
			}
		} else if (e.getSource() == btnSave) {
			// ask user for a save location and save the file
			if (jfc.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
				if (modified) {
					quiz = new Quiz(nameField.getText(), qlistModel.getObjects());
					modified = false;
				}
				try {
					quiz.save(jfc.getSelectedFile().getAbsolutePath());
				} catch (IOException e1) {
					JOptionPane.showMessageDialog(null, "Failed to save quiz");
				}
			}
		} else if (e.getSource() == btnAddQuestion) {
			// obtain question data from UI
			modified = true;
			ArrayList<String> answers = new ArrayList<String>(4);
			answers.add(ansA.getText());
			answers.add(ansB.getText());
			answers.add(ansC.getText());
			answers.add(ansD.getText());
			int answerCount = 0;
			// question must contain at least two non-empty answers to be valid
			boolean isValid = false;
			for (String ans : answers) {
				if (!ans.equals("")) {
					answerCount++;
					if (answerCount >= 2) {
						isValid = true;
						break;
					}
				}
			}
			if (!isValid) {
				JOptionPane.showMessageDialog(null, "Questions need at least 2 answers", "Invalid question",
						JOptionPane.ERROR_MESSAGE);
				return;
			}
			// only non-empty answers can be correct for the question to be valid
			// additionally, at least one answer must be correct
			isValid = false;
			boolean accepted[] = new boolean[] { aOK.isSelected(), bOK.isSelected(), cOK.isSelected(),
					dOK.isSelected() };
			for (int i = 0; i < 4; i++) {
				if (accepted[i]) {
					if (answers.get(i).equals("")) {
						isValid = false;
						break;
					} else {
						isValid = true;
					}
				}
			}
			if (!isValid) {
				JOptionPane.showMessageDialog(null, "Question either has no correct answers or accepts an empty answer",
						"Invalid question", JOptionPane.ERROR_MESSAGE);
				return;
			}
			try {
				Question question = new Question(questionField.getText(), Integer.parseInt(timeField.getText()),
						Integer.parseInt(pointsField.getText()), answers, accepted);

				// load image into question data and clear UI so next question can be entered
				if (loadedImage != null) {
					ByteArrayOutputStream baos = new ByteArrayOutputStream();
					ImageIO.write(ImageIO.read(loadedImage), "jpg", baos);
					question.setMultimediaDataForKey(Question.keyHasImage, true);
					question.setMultimediaDataForKey(Question.keyImageData, baos.toByteArray());
				}
				
				qlistModel.addQuestion(question);
				questionField.setText("");
				timeField.setText("");
				pointsField.setText("");
				ansA.setText("");
				ansB.setText("");
				ansC.setText("");
				ansD.setText("");
				aOK.setSelected(false);
				bOK.setSelected(false);
				cOK.setSelected(false);
				dOK.setSelected(false);
				loadImage(null);
			} catch (NumberFormatException | IOException e1) {
				e1.printStackTrace();
			}
		} else if (e.getSource() == btnRemoveQuestion) {
			removeSelectedQuestion();
		} else if (e.getSource() == btnEditQuestion) {
			// load question data into UI and remove from question list
			int row = questionList.getSelectedRow();
			if (row >= 0) {
				Question q = qlistModel.getObjects().get(row);
				ArrayList<String> answers = q.getAnswers();
				questionField.setText(q.getQ());
				ansA.setText(answers.get(0));
				ansB.setText(answers.get(1));
				ansC.setText(answers.get(2));
				ansD.setText(answers.get(3));
				timeField.setText(Integer.toString(q.getTimeLimit()));
				pointsField.setText(Integer.toString(q.getPoints()));
				aOK.setSelected(q.acceptAnswer(0));
				bOK.setSelected(q.acceptAnswer(1));
				cOK.setSelected(q.acceptAnswer(2));
				dOK.setSelected(q.acceptAnswer(3));
				removeSelectedQuestion();
			}
		} else if (e.getSource() == btnClearImage) {
			// remove image from question
			loadedImage = null;
			loadImage(null);
		} else if (e.getSource() == btnLoadImage) {
			// load an image from file
			if (jfc.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
				loadedImage = jfc.getSelectedFile();
				loadImage(loadedImage);
			}
		}
	}
	

	private void loadImage(File file) {
		imagePanel.removeAll();
		if (file != null) {
			try {
				JLabel lbl = new JLabel(new ImageIcon(new ImageIcon(ImageIO.read(file)).getImage()
						.getScaledInstance(imagePanel.getWidth(), imagePanel.getHeight(), Image.SCALE_DEFAULT)));
				imagePanel.add(lbl);
				validate();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		imagePanel.repaint();
	}

	private void removeSelectedQuestion() {
		int row = questionList.getSelectedRow();
		if (row >= 0) {
			modified = true;
			qlistModel.removeQuestion(row);
		}
	}

}