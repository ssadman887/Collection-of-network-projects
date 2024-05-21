package backend;

public class Updater implements Runnable {
	
	private Updatable updatable;
	private double delay;

	public Updater(Updatable comp, double delay) {
		this.updatable = comp;
		this.delay = delay;
	}
	
	public void run() {
		long lastUpdate = System.nanoTime();
		double delta = 0;
		while (updatable.stillRunning()) {
			long now = System.nanoTime();
			delta = (now - lastUpdate) / 1000000000;
			if (delta >= delay - 0.1) {
				updatable.update();
				lastUpdate = now;
			}
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
}