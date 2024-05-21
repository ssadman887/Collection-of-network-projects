package frontend;

import java.awt.*;

import javax.swing.*;

public class AboutWindow extends JFrame {
	private JPanel contentPane;

	private static final long serialVersionUID = -5929273713052488865L;
	
	public AboutWindow() {
		setTitle("About Quizler v1.0");
		setBounds(600, 120, 800, 600);
		getContentPane().setLayout(new GridLayout(0, 1, 0, 0));
		JScrollPane scroll = new JScrollPane();
		JTextArea text = new JTextArea();

		text.setText("                                   	This is a simple Quiz Application.");

		text.setFont(new Font("Segoe UI Semilight", Font.PLAIN, 15));
		text.setEditable(false);
		scroll.setViewportView(text);
		getContentPane().add(scroll);


	}

}