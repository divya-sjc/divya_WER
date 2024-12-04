package TataDigitalOmniTest;
import io.appium.java_client.AppiumDriver;
import com.opencsv.CSVWriter; 
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URL;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.opencsv.CSVParser;
import com.opencsv.CSVParserBuilder;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.UnsupportedAudioFileException;

import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.interactions.Pause;
import org.openqa.selenium.interactions.PointerInput;
import org.openqa.selenium.interactions.Sequence;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

//All fashion products go to tata cliq
//Disambiguation inside sub app, searches internally only
//supports navigation and lab in 1mg
//csv format output
public class TD_automation {
	
static AppiumDriver driver;
static String ui_hints[] = new String[12];
static WebDriverWait wait;
static List<String[]> data = new ArrayList<String[]>(); 
	
	public static void setup() {
		try {
			DesiredCapabilities cap = new DesiredCapabilities();
			cap.setCapability("deviceName", "Android Emulator");
			cap.setCapability("isHeadless", true);
			cap.setCapability("udid", "emulator-5554");
			cap.setCapability("platformName", "Android");
			cap.setCapability("platformVersion", "13");
			cap.setCapability("appium:app", "/Users/divyac/Documents/AppiumProject/TataDigitalOmniTest/src/test/resources/APK/TD_Prod_10th-April.apk");
//			cap.setCapability("appium:app", "/Users/divyac/Documents/AppiumProject/TataDigitalOmniTest/src/test/resources/APK/STAGING - c5436eb104a2493485bf6e2b543c0237 - 21st March.apk");
			cap.setCapability("automationName", "UiAutomator2");
			cap.setCapability("appium:noReset", false); 
			URL url = new URL("http://127.0.0.1:4723");
			driver = new AppiumDriver(url, cap);
			Thread.sleep(3000);
			}catch(Exception e)
		{
			System.out.println("Cause is: "+e.getCause());
			System.out.println("Message is: "+e.getMessage());
		}
	}
	
	public static void teardown() {
		driver.quit();
		try {
			Thread.sleep(1500);
		}catch(Exception e) {
			
		}
	}
	
	
	public static void playAudio(String audioFilePath) throws IOException, UnsupportedAudioFileException, LineUnavailableException {
	    File audioFile = new File(audioFilePath);

	    AudioInputStream audioStream = AudioSystem.getAudioInputStream(audioFile);
	    AudioFormat format = audioStream.getFormat();

	    DataLine.Info info = new DataLine.Info(SourceDataLine.class, format);
	    SourceDataLine audioLine = (SourceDataLine) AudioSystem.getLine(info);
	    audioLine.open(format);
	    audioLine.start();
	    //System.out.println("Audio Started");

	    int bufferSize = 4096;
	    byte[] buffer = new byte[bufferSize];
	    int bytesRead;

	    while ((bytesRead = audioStream.read(buffer, 0, buffer.length)) != -1) {
	        audioLine.write(buffer, 0, bytesRead);
	    }

	    audioLine.drain();
	    audioLine.close();
	    audioStream.close();
	}
	
	
	public static void callplayaudio(String d) throws InterruptedException {
		final String audioFilePath2 = d;
		Thread audioThread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    playAudio(audioFilePath2);
                } catch (IOException | UnsupportedAudioFileException | LineUnavailableException e) {
                    e.printStackTrace();
                }
            }
        });
        audioThread.start();
	}
	
	
	public static String getnlpresponse() throws InterruptedException {
		long startTime = System.currentTimeMillis();
		while((System.currentTimeMillis() - startTime) / 1000 < 25) {
		try{
			WebElement resp_heading = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text"));
			String resp = resp_heading.getText();
			if((!resp.contains("Just a moment")) &&  (!resp.contains("I’m on it. Give me a moment")) &&  (!resp.contains("Give me a clue")) &&  (!resp.contains("Processing")) && (!resp.contains("Fetching"))  && (!resp.contains("Almost there")) && (!resp.contains("Got it"))&& (!resp.contains("clarification")) && (!resp.contains("Searching")) && (!resp.contains("Anything else?")) && (!resp.contains("Initiating")) && (!resp.contains("Seeking"))) {
				System.out.println("Response= "+resp);
				return resp;
			}
	        }catch(Exception e) {
	        	continue;
	        }
		}
		return "";
	}
	
	
	public static int mute_umnute() throws InterruptedException {
		long startTime = System.currentTimeMillis();
		while((System.currentTimeMillis() - startTime) / 1000 < 25) {
		try{
			WebElement speaker = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_header_v2_action_mute_button_container"));
			speaker.click();
			return 1;
	        }catch(Exception e) {
	        	continue;
	        }
		}
		return 0;
	}
	
	
	public static int feedback() throws InterruptedException {
		long startTime = System.currentTimeMillis();
		while((System.currentTimeMillis() - startTime) / 1000 < 25) {
		try{
			WebElement resp_heading = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text"));
			String resp = resp_heading.getText();
			if(!resp.contains("sorry")) {
				try{
					WebElement thumbsup = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_settings_v2_thumb_up_button_container"));
					thumbsup.click();
					return 1;
				}catch(Exception e) {
					continue;
				}
			}
			else {
				try{
					WebElement thumbsdown = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_settings_v2_thumb_down_button_container"));
					thumbsdown.click();
					return 1;
				}catch(Exception e) {
					continue;
				}
			}
	        }catch(Exception e) {
	        	continue;
	        }
		}
		return 0;
	}
	
	
	public static String[] allhints() throws Exception{
		String hints[]= {"","","", ""};
		scroll_right();
		String app = guess_app();
		try {
        	WebElement hint1 = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.TextView")));
    		System.out.println("Hint1="+ hint1.getText());
    		hints[0]=hint1.getText();
    		try {
			WebElement hint2 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView")));
			System.out.println("Hint2="+hint2.getText());
			hints[1]=hint2.getText();
					try {
						WebElement hint3 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView")));
						System.out.println("Hint3a="+hint3.getText());
						hints[2] = hint3.getText();
						try {
							if(app.equalsIgnoreCase("bigbasket"))scroll1();else scroll();
							WebElement hint4 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[4]/android.widget.TextView")));
								System.out.println("Hint4a="+hint4.getText());
								hints[3] = hint4.getText();
						}catch(Exception e) {
							if(app.equalsIgnoreCase("bigbasket"))scroll1();else scroll();
//							System.out.println("First attempt to search hint 4 failed");
							try {
							WebElement hint4 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView")));
							System.out.println("Hint4b="+hint4.getText());
							hints[3] = hint4.getText();
							}catch(Exception e1) {
//								System.out.println("Second attempt to search hint 4 failed");
							}
						}
					}catch(Exception e0) {
						if(app.equalsIgnoreCase("bigbasket"))scroll1();else scroll();
//						System.out.println("First attempt to search hint 3 failed");
							try {
								WebElement hint3 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView")));
								System.out.println("Hint3a="+hint3.getText());
								hints[2] = hint3.getText();
								try {
									WebElement hint4 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[4]/android.widget.TextView")));
										System.out.println("Hint4a="+hint4.getText());
										hints[3] = hint4.getText();
								}catch(Exception e11) {
//									System.out.println("Third attempt to search hint 4 failed");
									WebElement hint4 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView")));
									System.out.println("Hint4a="+hint4.getText());
									hints[3] = hint4.getText();
								}
								}catch(Exception e) {
									if(app.equalsIgnoreCase("bigbasket"))scroll1();else scroll();
									WebElement hint3 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView")));
									System.out.println("Hint3a="+hint3.getText());
									hints[2] = hint3.getText();
									try {
										WebElement hint4 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView")));
											System.out.println("Hint4a="+hint4.getText());
											hints[3] = hint4.getText();
									}catch(Exception e10) {
								}
								}
					}
			}catch(Exception e1){
			}
		}catch(Exception e2){
    	}
		return hints;
	}
	
	public static int check_clarification_asked(String d) throws Exception{
		String searchterm =""; int a=0; String Hint3="", plp="", nulls="";
		try {
        	WebElement hint1 = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_hints_item_text")));
    		String Hint1 = hint1.getText();
    		try {
			WebElement hint2 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView")));
			String Hint2 = hint2.getText();
			try {
				WebElement hint3 =  new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView")));
				Hint3 = hint3.getText();
			}catch(Exception e) {}
			if((Hint1.equalsIgnoreCase("FAQs")) || (Hint1.equalsIgnoreCase("Chat with us"))){
				if((Hint2.equalsIgnoreCase("FAQs")) || (Hint2.equalsIgnoreCase("Chat with us"))){
					System.out.println("****************** Unsupported ******************");
					System.out.println("Chip 1 ="+Hint1);
					System.out.println("Chip 2 ="+Hint2);
					String app = guess_app();
					System.out.println("App Name: "+app);
					plp=check_plp();
					nulls = product_shown();
					data.add(new String[] { d,"Unsupported ", app, Hint1, Hint2, "", "", searchterm, plp+" "+nulls});
					System.out.println("**************************************************************************************");
					//Clicking on first hint
					hint1.click();
					app = guess_app();
					System.out.println("App Name: "+app);
					data.add(new String[] { Hint1+" clicked", "", app, Hint1, Hint2, Hint3, "", "", ""});
					//Clicking on second hint
					hint2.click();
					app = guess_app();
					System.out.println("App Name: "+app);
					data.add(new String[] { Hint2+" clicked", "", app, Hint1, Hint2, Hint3, "", "", ""});
					return 2;
			}
			}
			if((Hint1.toLowerCase().equals("grocery")) || (Hint1.toLowerCase().equals("electronics")) || (Hint1.toLowerCase().equals("beauty")) || (Hint1.toLowerCase().equals("fashion")) || (Hint1.toLowerCase().contains("health")) || (Hint1.toLowerCase().contains("lab")) || (Hint1.contains("Tata neu")) || (Hint1.toLowerCase().equals("pharmacy")) || (Hint1.toLowerCase().contains("wellness")) || (Hint1.toLowerCase().equals("household")) || (Hint1.toLowerCase().equals("sport")) || (Hint1.toLowerCase().equals("furniture")) || (Hint1.toLowerCase().equals("fitness"))){
				if((Hint2.toLowerCase().equals("grocery")) || (Hint2.toLowerCase().equals("electronics")) || (Hint2.toLowerCase().equals("beauty")) || (Hint2.toLowerCase().equals("fashion")) || (Hint2.toLowerCase().contains("health")) || (Hint2.toLowerCase().contains("lab")) || (Hint2.contains("Tata neu")) || (Hint2.toLowerCase().equals("pharmacy")) || (Hint2.toLowerCase().contains("wellness")) || (Hint2.toLowerCase().equals("household")) || (Hint2.toLowerCase().equals("sport")) || (Hint2.toLowerCase().equals("furniture")) || (Hint2.toLowerCase().equals("fitness"))){
					System.out.println("****************** Disambiguates ******************");
					System.out.println("Category 1 ="+Hint1);
					System.out.println("Category 2 ="+Hint2);
					String resp = getnlpresponse();
					String app = guess_app();
					System.out.println("App Name: "+app);
					plp=check_plp();
					nulls = product_shown();
					data.add(new String[] { d,"Disambiguates "+resp, app, Hint1, Hint2, Hint3, "", searchterm, plp+" "+nulls});
					System.out.println("**************************************************************************************");
					first_hint_click();
					return 1;
			}
			}
			}catch(Exception e){
    		if((Hint1.contains("Tata neu"))|| (Hint1.toLowerCase().equals("grocery")) || (Hint1.toLowerCase().equals("electronics")) || (Hint1.toLowerCase().equals("beauty")) || (Hint1.toLowerCase().equals("fashion")) || (Hint1.toLowerCase().contains("health")) || (Hint1.toLowerCase().contains("lab")) || (Hint1.contains("Tata neu")) || (Hint1.toLowerCase().equals("pharmacy")) || (Hint1.toLowerCase().contains("wellness")) || (Hint1.toLowerCase().equals("household")) || (Hint1.toLowerCase().equals("sport")) || (Hint1.toLowerCase().equals("furniture")) || (Hint1.toLowerCase().equals("fitness"))) {
    			String app = guess_app();
    			System.out.println("App Name: "+app);
    			String resp = getnlpresponse();
    			plp=check_plp();
    			nulls = product_shown();
    			System.out.println("Disambiguation has only one category chip that is chosen");	
    			System.out.println("Category 1 ="+Hint1);
    			data.add(new String[] {d, resp, app, Hint1, "","", "", searchterm, plp+" "+nulls});
			}
    		return 1;
			}
		}catch(Exception e){
				//Not clarification
    		}
		return 0;
	}
		
	
	public static void scroll() {
		for(int i=0;i<3;i++) {
		int startX = 1040;
		int startY = 2600;
        int endX = (int) (startX * 0.02);
        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence scroll = new Sequence(finger, 0);
        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        scroll.addAction(finger.createPointerMove(Duration.ofMillis(25), PointerInput.Origin.viewport(), endX, startY));
        scroll.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
        driver.perform(Arrays.asList(scroll));
		}
	}
	
	public static void scroll_right() {
		String app = guess_app();
		if(app.equalsIgnoreCase("bigbasket")) {
		for(int i=0;i<3;i++) {
		int startX = 1040;
		int startY = 2450;
        int endX = (int) (startX * 2);
        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence scroll = new Sequence(finger, 0);
        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        scroll.addAction(finger.createPointerMove(Duration.ofMillis(25), PointerInput.Origin.viewport(), endX, startY));
        scroll.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
        driver.perform(Arrays.asList(scroll));
		}
		}
		else {
			for(int i=0;i<3;i++) {
				int startX = 1040;
				int startY = 2600;
		        int endX = (int) (startX * 2);
			 PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
		        Sequence scroll = new Sequence(finger, 0);
		        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
		        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
		        scroll.addAction(finger.createPointerMove(Duration.ofMillis(25), PointerInput.Origin.viewport(), endX, startY));
		        scroll.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
		        driver.perform(Arrays.asList(scroll));
		}
		}
	}
	
	
	public static void recipe_scroll_right() {
		String app = guess_app();
		if(app.equalsIgnoreCase("bigbasket")) {
		for(int i=0;i<3;i++) {
		int startX = 333;
		int startY = 2222;
        int endX = (int) (startX * 2);
        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence scroll = new Sequence(finger, 0);
        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        scroll.addAction(new Pause(finger, Duration.ofMillis(200)));
        scroll.addAction(finger.createPointerMove(Duration.ofMillis(25), PointerInput.Origin.viewport(), endX, startY));
        scroll.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
        driver.perform(Arrays.asList(scroll));
		}
		}
		else {
				int startX = 333;
				int startY = 2500;
		        int endX = (int) (startX * 2);
			 PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
		        Sequence scroll = new Sequence(finger, 0);
		        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
		        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
		        scroll.addAction(new Pause(finger, Duration.ofMillis(200)));
		        scroll.addAction(finger.createPointerMove(Duration.ofMillis(25), PointerInput.Origin.viewport(), endX, startY));
		        scroll.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
		        driver.perform(Arrays.asList(scroll));
		}
	}
	
	
	public static void recipe_scroll_left() {
		String app = guess_app();
		if(app.equalsIgnoreCase("bigbasket")) {
		int startX = 1111;
		int startY = 2222;
        int endX = (int) (startX * 0.5);
        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence scroll = new Sequence(finger, 0);
        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        scroll.addAction(new Pause(finger, Duration.ofMillis(200)));
        scroll.addAction(finger.createPointerMove(Duration.ofMillis(25), PointerInput.Origin.viewport(), endX, startY));
        scroll.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
        driver.perform(Arrays.asList(scroll));
		}
		else {
				int startX = 1100;
				int startY = 2522;
		        int endX = (int) (startX * 0.5);
			 PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
		        Sequence scroll = new Sequence(finger, 0);
		        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
		        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
		        scroll.addAction(new Pause(finger, Duration.ofMillis(200)));
		        scroll.addAction(finger.createPointerMove(Duration.ofMillis(25), PointerInput.Origin.viewport(), endX, startY));
		        scroll.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
		        driver.perform(Arrays.asList(scroll));
		}
	}
	
	public static void scroll1() {
		for(int i=0;i<3;i++) {
		int startX = 1040;
		int startY = 2450;
        int endX = (int) (startX * 0.02);
        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence scroll = new Sequence(finger, 0);
        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        scroll.addAction(finger.createPointerMove(Duration.ofMillis(25), PointerInput.Origin.viewport(), endX, startY));
        scroll.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
        driver.perform(Arrays.asList(scroll));
		}
	}
	
	public static void click_coord(int startX, int startY) {
		 PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
	        Sequence scroll = new Sequence(finger, 0);
	        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
	        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
	        driver.perform(Arrays.asList(scroll));
	}
	
	public static void click_position(int startX, int startY) {
		 PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
	        Sequence scroll = new Sequence(finger, 0);
	        scroll.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), startX, startY));
	        scroll.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
	        scroll.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
	        driver.perform(Arrays.asList(scroll));
	}
	
	public static void ui_while() {
		try {
			setup();	
			System.out.println("**************************************************************************************");	
			try {
			WebElement assist = new WebDriverWait(driver, Duration.ofSeconds(120)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[4]")));
			assist.click();
			System.out.println("Application started...");	
			}catch(Exception e1) {
				System.out.println("Assist trigger is not visible");
			}
		}catch(Exception e2) {
			System.out.println("Application could not started");
		}
	}
			
	public static void sub_app_search_and_hint_clicked(String d) {
		String searchterm = "", plp="", nulls="";
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
		try {
			WebElement editing = new WebDriverWait(driver, Duration.ofSeconds(20)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
			editing.click();
			editing.clear();
			Thread.sleep(700);
			editing.sendKeys(d);
			System.out.println("Utterance= "+d);
			Thread.sleep(500);
			click_position(1313, 2820);
			int a = check_clarification_asked(d);
			if(a!=2) {
			try {
			WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
			String resp = getnlpresponse();
			String app = guess_app();
			System.out.println("App Name: "+app);
			String[] hints = allhints();
			if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
				searchterm = search_bar_utterance(app);
				System.out.println("Value passed to the search bar = "+searchterm);
				plp=check_plp();
				nulls = product_shown();
			}
			if (a!=1){
				data.add(new String[] {d, resp, app, hints[0], hints[1], hints[2], hints[3], searchterm, plp+" "+nulls});
			}
			}catch(Exception e6) {
				System.out.println("Response takes longer than expected");
				data.add(new String[] {d, "Response takes longer than expected", "Unknown", "", "", "", "", "", ""});
			}
			}
		}catch(Exception e7) {
			System.out.println("Edit button or send button could not be clicked");
			data.add(new String[] {d, "Edit button or send button could not be clicked", "Unknown", "", "", "", "", "", ""});
		}
		}
		}catch(Exception e) {
			teardown();
			ui_while();
		}
	}
	
	public static void first_hint_click() {
		String searchterm = "", plp="", nulls="";
		scroll_right();
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
		try {
			WebElement clickable_hint1 =  new WebDriverWait(driver, Duration.ofSeconds(20)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.TextView")));
			String hint2 = clickable_hint1.getText();
			System.out.println("Hint1= "+hint2);
			clickable_hint1.click();
			int a = check_clarification_asked(hint2);
			if(a!=2) {
			System.out.println("First clickable hint is clicked");
			String resp = getnlpresponse();
			String app = guess_app();
			System.out.println("App Name: "+app);
			String[] hints = allhints();
			if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
				searchterm = search_bar_utterance(app);
				System.out.println("Value passed to the search bar = "+searchterm);
				plp=check_plp();
				nulls = product_shown();
			}
			
			if (a!=1) {
				data.add(new String[] {hint2, resp, app, hints[0], hints[1], hints[2], hints[3], searchterm, plp+" "+nulls});
			}
			}
			}catch(Exception e1) {
				System.out.println("First clickable hint could not be clicked");
				data.add(new String[] {"", "First clickable hint could not be clicked", "", "", "", "", "", "", ""});
			}
		}
		}catch(Exception e2) {
			teardown();
			ui_while();
		}
		}
	
	public static String search_bar_utterance(String app) {
		WebElement response1=null;
		try {
		Thread.sleep(300);
		}catch(Exception e) {
		}
		if(app.equals("bigbasket") || app.equals("")) {
		long startTime1 = System.currentTimeMillis();
		while((System.currentTimeMillis() - startTime1) / 1000 < 15) {
		try{
			//bb
			response1 = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View[3]/android.view.View/android.widget.EditText"));
			if(response1.getText().equals("New Delhi")) {
				continue;
			}
			break;
			}catch(Exception e0) {
				continue;
			}
		}
		}
		
		//croma
		if(app.equals("croma") || app.equals("")) {
			long startTime1 = System.currentTimeMillis();
			while((System.currentTimeMillis() - startTime1) / 1000 < 15) {
			try{
				response1 = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.widget.TextView"));
				if(response1.getText().equals("New Delhi")) {
					continue;
				}
				break;
				}catch(Exception e0) {
					continue;
				}
			}
			}
				
		//Tata 1mg
				if(app.equals("Tata 1mg") || app.equals("")) {
					long startTime1 = System.currentTimeMillis();
					while((System.currentTimeMillis() - startTime1) / 1000 < 15) {
					try{
						response1 = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[3]/android.view.View/android.widget.TextView"));
						if(response1.getText().equals("New Delhi")) {
							continue;
						}
						break;
						}catch(Exception e0) {
							continue;
						}
					}
					}	
		
				//Tata cliq
				if(app.equals("Tata Cliq") || app.equals("")) {
					long startTime1 = System.currentTimeMillis();
					while((System.currentTimeMillis() - startTime1) / 1000 < 15) {
					try{
						response1 = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]"));
						if(response1.getText().equals("New Delhi")) {
							continue;
						}
						break;
						}catch(Exception e0) {
							continue;
						}
					}
					}		
				
				//westside
				if(app.equals("Westside")) {
					long startTime1 = System.currentTimeMillis();
					while((System.currentTimeMillis() - startTime1) / 1000 < 15) {
					try{
						response1 = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[3]/android.widget.TextView"));
						if(response1.getText().equals("New Delhi")) {
							continue;
						}
						break;
						}catch(Exception e0) {
							continue;
						}
					}
					}	
				
					
		if(response1==null)
			return "";
		else {
		String utterance = response1.getText();
		return utterance;
		}
		}
	
	
	public static void sec_hint_clicked(String d) {
		String response1="", plp="", nulls="";
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
				System.out.println("Second hint is clicked");
				scroll_right();
		try {
        	WebElement hint1 = new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_hints_item_text")));
        	String hint1_txt = hint1.getText();
    		try {
    			WebElement clickable_hint1 =  new WebDriverWait(driver, Duration.ofSeconds(20)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView")));
    			String hint2 = clickable_hint1.getText();
    			clickable_hint1.click();
    			int a = check_clarification_asked(hint2);
    			if(a!=2) {
    			String app = guess_app();
    			System.out.println("App Name: "+app);
    			String resp = getnlpresponse();
    			if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
    					response1 = search_bar_utterance(app);
    					System.out.println("Value passed to the search bar = "+response1);
    					plp=check_plp();
    	    			nulls = product_shown();
    			}
    			String[] hints = allhints();
    			if((hint2.equalsIgnoreCase(response1)) || (response1.contains(hint2)) || (!response1.equalsIgnoreCase(""))) {
    				System.out.println("Clickable hints work well");
    			}
    			
    			if (a!=1){
    				data.add(new String[] { hint2,resp, app, hints[0], hints[1], hints[2], hints[3], response1, plp+" "+nulls});
    			}
    			}
    		}catch(Exception e4) {
    			hint1.click();
    			System.out.println("First clickable hint is clicked");
    			int a = check_clarification_asked(hint1_txt);
    			if(a!=2) {
    			String app = guess_app();
    			System.out.println("App Name: "+app);
    			String resp = getnlpresponse();
    			if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
    					response1 = search_bar_utterance(app);
    					System.out.println("Value passed to the search bar = "+response1);
    					plp=check_plp();
    	    			nulls = product_shown();
    			}
    			String[] hints = allhints();
    			if((hint1_txt.equalsIgnoreCase(response1)) || (response1.contains(hint1_txt)) || (!response1.equalsIgnoreCase(""))) {
    				System.out.println("Clickable hints work well");
    			}
    			
    			if (a!=1){
    				data.add(new String[] {hint1_txt,resp, app, hints[0], hints[1], hints[2],hints[3], response1,plp+" "+nulls});
    			}
    			}
			}
			
			}catch(Exception e4) {
				System.out.println("No clickable hints are seen");
				data.add(new String[] {"No hint", "No clickable hints are seen", "", "", "", "", "", "", ""});
			}
		}
		}catch(Exception e) {
			teardown();
			ui_while();
		}
	}
	
	
	
	
	public static void select_app_search_in_it(String app, String d) {
		ui_while();
		String plp="", nulls="";
		if(app.equalsIgnoreCase("Electronics"))
			try {
				WebElement editing = new WebDriverWait(driver, Duration.ofSeconds(20)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
				editing.click();
				editing.clear();
				Thread.sleep(700);
				editing.sendKeys("iphone 14 pro");
				System.out.println("Utterance= iphone 14 pro");
				Thread.sleep(500);
				click_position(1313, 2820);
				Thread.sleep(2000);
			}catch(Exception e0) {
				System.out.println("Electronic app could not be selected");		
				data.add(new String[] {"", "electronic could not be clicked", "", "", "", "", "", "", ""});
			}
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
		try {
			WebElement editing = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
			editing.click();
			editing.clear();
			Thread.sleep(700);
			editing.sendKeys(d);
			System.out.println("Utterance= "+d);
			Thread.sleep(500);
			click_position(1313, 2820);
			int a = check_clarification_asked(d);
			if(a!=2) {
			WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
			String app2 = guess_app();
			System.out.println("App Name: "+app2);
			String resp = getnlpresponse();
			String[] hints = allhints();
			plp=check_plp();
			nulls = product_shown();
			if (a!=1){
				data.add(new String[] {d, resp, app2, hints[0], hints[1], hints[2], hints[3], "", plp+" "+nulls});
			}
			}
		}catch(Exception e7) {
			System.out.println("Edit button could not be clicked");
			data.add(new String[] {"edit", "Edit button could not be clicked", "", "","","","","", ""});
		}
		}
		}catch(Exception e2) {
			teardown();
			select_app_search_in_it(app, d);
		}
	}
	
	public static void sub_app_search_another_sub_app(String d) {
		guess_app();
		String app2 = "", searchterm="", plp="", nulls="";
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
		try {
			WebElement editing = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
			editing.click();
			editing.clear();
			Thread.sleep(700);
			editing.sendKeys(d);
			System.out.println("Utterance= "+d);
			Thread.sleep(500);
			click_position(1313, 2820);
			int r = check_clarification_asked(d);
			if(r!=2) {
			WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
			String resp = getnlpresponse();
			String[] hints = allhints();
			app2 = guess_app();
			System.out.println("App Name: "+app2);
			if((!app2.equalsIgnoreCase("Home Page"))||(!app2.equalsIgnoreCase("navigated")))	{
				searchterm = search_bar_utterance(app2);
				System.out.println("Value passed to the search bar = "+searchterm);
				plp=check_plp();
				nulls = product_shown();
			}
				if(d.equalsIgnoreCase("Tablet for students")) {
					data.add(new String[] { d, resp, "Croma", hints[0],hints[1], hints[2], hints[3], searchterm, plp+" "+nulls});
						System.out.println("**************************************************************************************");
						System.out.println("TestCase1:e: Searching in the sub app");
						sec_hint_clicked("Tablet for students");
				}
					else {
						if (r!=1){
							data.add(new String[] {d,resp, app2, hints[0], hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
						}
					}
			}
		}catch(Exception e7) {
			System.out.println("Edit button could not be clicked");
			data.add(new String[] {"edit", "Edit button could not be clicked", "", "", "", "", "", "", ""});
		}
		}
		}catch(Exception e) {
			teardown();
			ui_while();
//			sub_app_search_another_sub_app(d);
		}
	}
	
	
	public static void home_page_redirected_sub_app(String d) {
			String searchterm = "", plp="", nulls="";
			try {
				WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
				if(surface.isDisplayed()) {
			try {
				WebElement text_box_con = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
				text_box_con.click();
				Thread.sleep(700);
				text_box_con.sendKeys(d);
				Thread.sleep(500);
				System.out.println("Utterance= "+d);
				click_position(1313, 2820);
				int a = check_clarification_asked(d);
				if(a!=2) {
				String resp = getnlpresponse();
				String app = guess_app();
				System.out.println("App Name = "+app);
				String[] hints = allhints();
				if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
					searchterm = search_bar_utterance(app);
					System.out.println("Value passed to the search bar = "+searchterm);
					plp=check_plp();
					nulls = product_shown();
			}
				if(d.equalsIgnoreCase("ceiling fan"))
					app="croma";
				if (a!=1){
					data.add(new String[]  {d, resp,app, hints[0],hints[1], hints[2], hints[3],searchterm, plp, nulls});
				}
				}
			}catch(Exception e1) {
				System.out.println("Text box could not be edited");
				data.add(new String[] { "","Text box could not be edited","", "","", "", "", "", "",""});
			}
			}
			}catch(Exception e){
				teardown();
				ui_while();
				System.out.println("repeat again");
				home_page_redirected_sub_app(d);
			}
	}
	
	
	
	public static void disamb_from_home(String d, String hint) {
		String searchterm ="", plp="", nulls="";
		int result = 0;
		String app = guess_app();
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
		try {
			WebElement text_box = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
			text_box.click();
			Thread.sleep(700);
			text_box.sendKeys(d);
			Thread.sleep(500);
			click_position(1313, 2820);
			System.out.println("Utterance= "+d);
			String resp = getnlpresponse();
			try {
			WebElement app1 = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.TextView")));
			String app_name1 = app1.getText();
			System.out.println("Category 1= "+app_name1);
			try {
			WebElement app2 = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView")));
			String app_name2 = app2.getText();
			System.out.println("Category 2= "+app_name2);
			data.add(new String[] {d,"Disambiguation "+resp, app, app_name1, app_name2, "", searchterm, ""});
			if(hint.equalsIgnoreCase(app_name2)) {
				app2.click();
				System.out.println(app_name2+" is clicked");
				app = guess_app();
				resp = getnlpresponse();
				String[] hints = allhints();
				if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
					searchterm = search_bar_utterance(app);
					System.out.println("Value passed to the search bar = "+searchterm);
					plp=check_plp();
					nulls = product_shown();
				}
				if((hints[0].equalsIgnoreCase("electronics")) || (hints[0].contains("fitness"))|| (hints[0].contains("health"))||(hints[0].contains("lab")) ||(hints[0].contains("healthcare")) ||(hints[0].contains("pharmacy")) || (hints[0].contains("fashion"))||(hints[0].contains("beauty")) ||(hints[0].contains("sports")) || (hints[0].contains("grocery"))||(hints[0].contains("household")) ||(hints[0].equals("baby")) ||(hints[0].contains("stationary"))) {
						System.out.println("Disambiguation loop");
						data.add(new String[] {app_name2,"Disambiguation loop "+resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
					}
					else {
						System.out.println("Disambiguation works");
						data.add(new String[] {app_name2, resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
					}
			}
			}catch(Exception e) {
				data.add(new String[] {"", "No Disambiguation", "", "", "", "", "", "", ""});
			}
			if(hint.equalsIgnoreCase(app_name1)) {
				app1.click();
				System.out.println(app_name1+" is clicked");
				app = guess_app();
				resp = getnlpresponse();
				String[] hints = allhints();
				if((!app.equalsIgnoreCase("Home Page"))	||(!app.equalsIgnoreCase("navigated"))){
					searchterm = search_bar_utterance(app);
					System.out.println("Value passed to the search bar = "+searchterm);
					plp=check_plp();
					nulls = product_shown();
			}
				if((hints[0].equalsIgnoreCase("electronics")) ||(hints[0].contains("fitness")) || (hints[0].contains("health"))||(hints[0].contains("lab")) ||(hints[0].contains("healthcare")) ||(hints[0].contains("pharmacy")) || (hints[0].contains("fashion"))||(hints[0].contains("beauty")) ||(hints[0].contains("sports")) || (hints[0].contains("grocery"))||(hints[0].contains("household")) ||(hints[0].equals("baby")) ||(hints[0].contains("stationary"))) {
					System.out.println("Disambiguation loop");
					data.add(new String[] {app_name1, "Disambiguation loop "+resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
				}
				else {
					System.out.println("Disambiguation works");
					data.add(new String[] {app_name1, resp, app, hints[0], hints[1], hints[2], hints[3], searchterm, plp+" "+nulls});
				}
			}
				System.out.println("**************************************************************************************");
				System.out.println("TestCase8:b: Disambiguation in the sub app");
				sub_app_search_and_hint_clicked("Orange");
			}catch(Exception e) {
				System.out.println("Not Disambiguating");
				data.add(new String[] {"", "No disambiguation", "", "", "", "", "", "", ""});
			}
			
		}catch(Exception e1) {
			System.out.println("Text box could not be edited");
			data.add(new String[] {"input", "Input box could not be clicked", "", "", "", "", "", "", ""});
		}
		}
		}catch(Exception e) {
			teardown();
			ui_while();
			disamb_from_home(d, hint);
		}
}
	
	
	public static String guess_app() {
		String heading_text="";
		Long startTime1 = System.currentTimeMillis();
		while((System.currentTimeMillis() - startTime1) / 1000 < 30) {
			try {
				//croma
				WebElement app_name = driver.findElement(By.xpath("//android.view.View[@content-desc=\"Logo\"]/android.widget.Image"));
//				System.out.println("inside Croma");
					heading_text = "Croma";
					break;
			}catch(Exception e0) {
				try {
					//tata cliq
					WebElement app_name = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]/android.widget.TextView"));
//					System.out.println("inside TC");
					heading_text=app_name.getText();
					if(heading_text.equalsIgnoreCase("")) {
						heading_text = "Tata Cliq";
						break;
					}
					}catch(Exception e3) {
						try {
							//bigbasket
							WebElement app_name = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View/android.widget.TextView"));
//							System.out.println("inside bb");
							if(app_name.getText().equalsIgnoreCase("bigbasket")) {
								heading_text="bigbasket";
								break;
							}
							else {
								try {
									//home page
									app_name = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View"));
//									System.out.println("inside HP");
										heading_text = "Home Page";
									break;
								}catch(Exception e5) {
									continue;
								}
							}
							}catch(Exception e4) {
								try {
										//home page
										WebElement app_name = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View"));
//										System.out.println("inside HP");
											heading_text = "Home Page";
											break;
									}catch(Exception e5) {
									continue;
								}
							}
						}
			}
		}
					
		if(heading_text.equals("")) {
		startTime1 = System.currentTimeMillis();
		while((System.currentTimeMillis() - startTime1) / 1000 < 10) {
		try {
			WebElement app_name = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.widget.TextView[2]"));
//			System.out.println("inside bp");

			if((app_name.getText().contains("file:"))) {
				heading_text = "navigated";
				break;
			}
			else {
				try {
					//home page
					app_name = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View"));
//					System.out.println("inside HP");
						heading_text = "Home Page";
						break;
				}catch(Exception e5) {
						try {
							//tata 1mg
							app_name = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View[2]/android.widget.Image"));
//							System.out.println("inside 1mg");
							heading_text = "Tata 1mg";
							break;
						}catch(Exception e4) {
							continue;
						}
				}
					}
		}catch(Exception e6) {
			try {
				//home page
				WebElement app_name = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View"));
//				System.out.println("inside HP");
					heading_text = "Home Page";
					break;
			}catch(Exception e5) {
			try {
						//tata 1mg
						WebElement app_name = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View[2]/android.widget.Image"));
//						System.out.println("inside 1mg");
						heading_text = "Tata 1mg";
						break;
					}catch(Exception e4) {
						continue;
					}	
			}
		}
		}
		}
			
		if(heading_text.equals("400001"))
			heading_text = "Home Page";
		if((heading_text.equals("Sort By")) || (heading_text.equals("SORT BY")))
			heading_text = "Westside";
		if((heading_text.equals("Men")) || (heading_text.equals("Quick View")) || (heading_text.equals("Search for")) || (heading_text.equals("Products")))
			heading_text = "Tata Cliq";
//		System.out.println("App Name: "+heading_text);
		return heading_text;
		}
	
	
	
	public static void page_redirected(String d) {
		String plp="";
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
		try {
			WebElement text_box = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
			text_box.click();
			Thread.sleep(700);
			text_box.sendKeys(d);
			System.out.println("Utterance: "+d);			
			Thread.sleep(500);
			click_position(1313, 2820);
			String resp = getnlpresponse();
			int a = check_clarification_asked(d);
			if(a!=2) {
			String app=guess_app();
			System.out.println("App Name: "+app);
			String[] hints = allhints();
			if (a!=1){
				data.add(new String[]  {d, resp,app, hints[0],hints[1],hints[2], hints[3],"", ""});
			}
			}
			}catch(Exception e) {
				System.out.println("Apps Did not navigate");
				data.add(new String[] {d, "Apps Did not navigate", "", "", "", "", "", "", ""});
			}
			
		}
		}catch(Exception e) {

		}
	}
	
	
	public static String check_plp() throws InterruptedException {
		System.out.println("Checking plp");
		WebElement plp = null;
		String resp = "";
			try {
				WebElement bb_close = driver.findElement(By.id("banner_use_app_btn"));
				bb_close.click();
			}catch(Exception e) {
				e.fillInStackTrace();
			}
			String app = guess_app();
			if(!app.equalsIgnoreCase("Home Page")) {
		long startTime1 = System.currentTimeMillis();
		while((System.currentTimeMillis() - startTime1) / 1000 < 10) {
		try{
			//bb
			plp = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[3]/android.widget.TextView"));
			resp = plp.getText();
			System.out.println("Items= "+resp);
			return resp;
		}catch(Exception e) {
	       try {
	    	   //1 mg
			plp = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[3]/android.view.View/android.widget.TextView"));
	        	if(plp.getText().contains("Showing")) {
	        		resp = "Items= 1+";
	    			System.out.println("Items= 1+");
	    			return resp;
	        	}
	        	else {
	         	   try {
		    		   //croma
		   			plp = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.widget.ListView/android.view.View[1]/android.view.View"));
		   			if(plp.getText().contains("Results") || plp.getText().contains("Showing")) {
		   				resp = plp.getText();
			   			resp = resp.substring(resp.indexOf("(") + 1);
			   			resp = resp.substring(0, resp.indexOf(")"));
		   	    			System.out.println("Items= "+resp);
		   	    			return resp;
		   	        	}
		    	   }catch(Exception e2) {
		    		   try {
		    			   //tata cliq
		   	   			plp = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.widget.TextView[2]"));
		   	   	        		resp = plp.getText();
		   	   	    			System.out.println("Items= "+resp);
		   	   	    		return resp;
		   	    	   }catch(Exception e3) {
		   	    		   continue;
		   	    	   }
	        	}
	        	}
	       }catch(Exception e1) {
	    	   try {
	    		   //croma
	   			plp = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.widget.TextView"));
	   	        	if(plp.getText().contains("Results")) {
	   	        		resp = plp.getText();
			   			resp = resp.substring(resp.indexOf("(") + 1);
			   			resp = resp.substring(0, resp.indexOf(")"));
		   	    			System.out.println("Items= "+resp);
		   	    			return resp;
	   	        	}
	    	   }catch(Exception e2) {
	    		   try {
	    			   //tata cliq
	   	   			plp = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.widget.TextView[2]"));
	   	   	        		resp = plp.getText();
	   	   	    			System.out.println("Items= "+resp);
	   	   	    		return resp;
	   	    	   }catch(Exception e3) {
	   	    		   continue;
	   	    	   }
	    	   }
	    	   }
	       }
		}
	}
	return "";
	}
	
	public static String product_shown() {
		WebElement nullsearch = null;
		String nulls="";
		try {
			//bb
			nullsearch = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[1]"));
			if(nullsearch.getText().contains("sorry")) {
			nulls="Bigbasket shows null search";
			return nulls;
			}
			else {
				try {
					//croma
					nullsearch = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.widget.ListView/android.view.View[1]/android.view.View"));
					if(!nullsearch.isDisplayed())
						nulls="Croma shows null search";
					return nulls;
				}catch(Exception e1) {
					try {
						//tata cliq
						nullsearch = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.TextView"));
						if(nullsearch.getText().contains("No results found")) {
						nulls= nullsearch.getText()+" in Tata cliq";
						return nulls;
						}
					}catch(Exception e2) {
						try {
							// 1mg
							nullsearch = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[3]/android.view.View/android.widget.TextView[1]"));
							nulls=nullsearch.getText()+" in 1 MG";
							return nulls;
						}catch(Exception e3) {}
					}
				}
			}
		}catch(Exception e) {
			try {
				//croma
				nullsearch = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.widget.ListView/android.view.View[1]/android.view.View"));
				if(!nullsearch.isDisplayed())
				nulls="Croma shows null search";
				return nulls;
			}catch(Exception e1) {
				try {
					//tata cliq
					nullsearch = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.TextView"));
					if(nullsearch.getText().contains("No results found")) {
					nulls= nullsearch.getText()+" in Tata cliq";
					return nulls;
					}
				}catch(Exception e2) {
					try {
						// 1mg
						nullsearch = driver.findElement(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[3]/android.view.View/android.widget.TextView[1]"));
						nulls=nullsearch.getText()+" in 1 MG";
						return nulls;
					}catch(Exception e3) {}
				}
			}
	}
		return nulls;
	}
	
	public static void hanshake_test() {
		try {
			String PLP="";
		System.out.println("**************************************************************************************");
		setup();
		System.out.println("Application started...");	
		System.out.println("***************************** Handshake Surface *******************************************");
		Thread.sleep(3000);
			//Pause and play testing
			int p1=0, p2=0;
			try {
				Thread.sleep(3000);
				WebElement pause = new WebDriverWait(driver, Duration.ofSeconds(120))
				.until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[3]")));
				pause.click();
				try {
					WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
					if(surface.isDisplayed()) {
						System.out.println("Pause started working even before the trigger is clicked");
					}
				}catch(Exception e0) {
					System.out.println("Pause button doesn't work before the trigger is clicked");
					p1 =1;
				}
			}catch(Exception e1) {
				System.out.println("Pause button is not visible");
			}
			
			try {
				WebElement play = new WebDriverWait(driver, Duration.ofSeconds(8))
						.until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[2]")));
						play.click();
						try {
							WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
							if(surface.isDisplayed()) {
								System.out.println("Play started working even before the trigger is clicked");
							}
						}catch(Exception e0) {
							System.out.println("Play button doesn't work before the trigger is clicked");
							p2 =1;
						}
					}catch(Exception e1) {
						System.out.println("Play button is not visible");
					}	
		
		if(p1==1 && p2==1) {
			data.add(new String[] {"Testing play and pause before trigger ", "Doesn't work", "", "", "", "", "", "", ""});
		}
		else {
			data.add(new String[] {"Testing play and pause before trigger ", "work", "", "", "", "", "", "", ""});
		}
			try {	
			WebElement inline_trigger = new WebDriverWait(driver, Duration.ofSeconds(120))
			.until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[4]")));
			inline_trigger.click();
			String[] greeting_state = {"", "", "", "", ""};
			try {
				WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
				if(surface.isDisplayed()) {
					try {
						WebElement Star_icon = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_icon")));
						System.out.println("Surface star icon - visible");
						greeting_state[0] = "star icon";
					}catch(Exception e) {
						System.out.println("Surface star icon - Not visible");
					}
					try {
						WebElement greet_title = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_title_text")));
						System.out.println("Hi, I am AI search - visible");
						greeting_state[1] = "Hi, I am AI search";
					}catch(Exception e) {
						System.out.println("Hi, I am AI search - Not visible");
					}
					try {
						WebElement greet_heading = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
						System.out.println("Greeting "+greet_heading.getText());
						greeting_state[2] = greet_heading.getText();
					}catch(Exception e) {
						System.out.println("Greeting Not visible");
					}
					try {
						WebElement input_box = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
						System.out.println(input_box.getText());
						greeting_state[3] = input_box.getText();
					}catch(Exception e) {
						System.out.println("Input box not visible");
					}
					try {
						WebElement sec_mic = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
						System.out.println("Secondary mic is visible");
						greeting_state[4] = "Secondary mic";
					}catch(Exception e) {
						System.out.println("Secondary mic is Not visible");
					}
				}
						String app = guess_app();
						System.out.println("App Name: "+app);
						String[] hints = allhints();
				data.add(new String[] {"Greeting state - items ", greeting_state[0]+", "+greeting_state[1]+", "+greeting_state[2]+", "+greeting_state[3]+", "+greeting_state[4], app, hints[0], hints[1], hints[2], hints[3], "", PLP});
			}catch(Exception e) {
				System.out.println("Surface is not open");
				data.add(new String[] {"", "Surface wasnt open", "", "", "", "", "", "", ""});
			}
		}catch(Exception e1) {
			System.out.println("Trigger could not be clicked");
			data.add(new String[] {"", "Trigger could not be clicked", "", "", "", "", "", "", ""});
		}
		}catch(Exception e1) {
			System.out.println("Application could not be started");
			data.add(new String[] {"", "Appication could not be started", "", "", "", "", "", "", ""});
		}
		
		//Play button should not work after manually closing the surface
		horizontal_close();
		int q1=1, q2=1;
		try {
			WebElement pause = new WebDriverWait(driver, Duration.ofSeconds(120))
			.until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[3]")));
			pause.click();
			try {
				WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
				if(surface.isDisplayed()) {
					System.out.println("Pause started working when the surface was manually closed");
					q1=0;
				}
			}catch(Exception e0) {
				System.out.println("Pause button doesn't work when surface is manually closed");
			}
		}catch(Exception e1) {
			System.out.println("Pause button is not visible");
		}
		try {
			WebElement play = new WebDriverWait(driver, Duration.ofSeconds(8))
					.until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[2]")));
					play.click();
					try {
						WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
						if(surface.isDisplayed()) {
							System.out.println("Play started working when the surface was manually closed");
							q2=0;
						}
					}catch(Exception e0) {
						System.out.println("Play button doesn't work work when surface is manually closed");
					}
				}catch(Exception e1) {
					System.out.println("Play button is not visible");
				}	
		if(q1==1 && q2==1) {
			data.add(new String[] {"Testing play and pause after manually closing the surface ", "Doesn't work", "", "", "", "", "", "", ""});
		}
		else {
			data.add(new String[] {"Testing play and pause after manually closing the surface ", "work", "", "", "", "", "", "", ""});
		}
		
		try {	
			Thread.sleep(2000);
			WebElement inline_trigger = new WebDriverWait(driver, Duration.ofSeconds(120))
			.until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[4]")));
			inline_trigger.click();
		}catch(Exception e) {
			System.out.println("Inline trigger could not be clicked");
		}
		
	}
	
	public static void text_box_test() {
		System.out.println("***************************** Testing Text Input  *******************************************");
		String resp = "", searchterm="", plp="", nulls="";
		try {
				WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
				if(surface.isDisplayed()) {
				try {
					WebElement edit_text = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
					edit_text.click();
					Thread.sleep(1000);
					edit_text.sendKeys("Orange");
					System.out.println("Utterance= Orange");	
					Thread.sleep(500);
					click_position(1313, 2820);
					int a = check_clarification_asked("Orange");
					if(a==2) {
						data.add(new String[] {"Input box and send Button", "Works ", "", "","", "", "","", ""});
					}
					if(a!=2) {
						int x = mute_umnute();
						try {
							WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
							resp = getnlpresponse();
						}catch(Exception e) {
							System.out.println("Response takes longer");
							data.add(new String[] {"", "Response takes longer", "", "", "", "", "", "", ""});
						}
					int y = feedback();
					String app = guess_app();
					System.out.println("App Name: "+app);
					String[] hints = allhints();
					if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
						searchterm = search_bar_utterance(app);
						System.out.println("Value passed to the search bar = "+searchterm);
						plp=check_plp();
						nulls = product_shown();
					}
					if((searchterm.equalsIgnoreCase("Oranges")) || (searchterm.equalsIgnoreCase("Orange")) ){
						data.add(new String[] {"Input box and send Button", "Works", "", "","", "", "","", ""});
					}
					else {
						data.add(new String[] {"Input box and send Button", "Doesn't Works", "", "","", "", "","", ""});
					}
					if((x == 1)&&(y==1)) {
						System.out.println("Mute and feedback works");
						data.add(new String[] {"Mute and feedback", "Works ", "", "","", "", "","", ""});
					}
					else {
						System.out.println("Mute and feedback works");
						data.add(new String[] {"Mute and feedback", "Doesn't Works ", "", "","", "", "","", ""});
					}
									if (a!=1){
										data.add(new String[] {"Orange", resp,	app, hints[0],hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
									}
					}
								}catch(Exception e) {
									System.out.println("Edit button could not be clicked");
									data.add(new String[] {"input", "Input box could not be clicked", "", "", "", "", "", "", ""});
								}
				}
			}catch(Exception e) {
				System.out.println("Surface is not open");
				teardown();
				ui_while();
				text_box_test();
			}
	}
	
	public static void suspended_state_test() {
		System.out.println("***************************** Suspended State  *******************************************");	
		//suspended state
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
			try {
				WebElement sec_mic = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
				sec_mic.click();
				try {
					WebElement grant_dialog = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.android.permissioncontroller:id/grant_dialog")));
					if(grant_dialog.isDisplayed()) {
						try {
							WebElement allow_perm = new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.android.permissioncontroller:id/permission_allow_foreground_only_button")));
							allow_perm.click();
				String[] Suspended_state = {"", "", "", ""};
				try {
					WebElement star_icon = new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_icon")));
					System.out.println("Star icon visible");
					Suspended_state[0] = "Star icon";
					}catch(Exception e0) {
					}
				try {
					WebElement greet_heading = new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
					System.out.println("Greeting "+greet_heading.getText());
					Suspended_state[1] = greet_heading.getText();
				}catch(Exception e0) {
				}
				try {
					WebElement input_box = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
					System.out.println("Input_box "+input_box.getText());
					Suspended_state[2] = input_box.getText();
				}catch(Exception e) {
				}
				try {
					sec_mic = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
					System.out.println("Secondary mic is visible");
					Suspended_state[3] = "Secondary mic";
				}catch(Exception e) {
				}
				String app = guess_app();
				System.out.println("App Name: "+app);
				String[] hints = allhints();
				data.add(new String[] {"Suspended state - items ", Suspended_state[0]+", "+Suspended_state[1]+", "+Suspended_state[2]+", "+Suspended_state[3], app, hints[0], hints[1], hints[2], hints[3], "", ""});
					
						}catch(Exception e1) {
							System.out.println("Allow permission could not be clicked");
							data.add(new String[] {"", "Allow mic permission could not be clicked", "", "", "", "", "", "", ""});
						}
					}
				}catch(Exception e3) {
					System.out.println("Grant dialog box is not visible");
					data.add(new String[] {"", "Grant dialog box did not appear", "", "", "", "", "", "", ""});
				}
			}catch(Exception e3) {
				System.out.println("Secondary mic is not visible");
				data.add(new String[] {"", "Secondary mic could not be clicked", "", "", "", "", "", "", ""});
			}
			}
			}catch(Exception e3) {
				System.out.println("Surface is not visible");
				teardown();
				ui_while();
				suspended_state_test();
			}	
	}
	
	public static void listening_state_test() {
		System.out.println("***************************** Listening state  *******************************************");
		try {
			WebElement sec_mic = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
			sec_mic.click();
						//listening state elements
						String[] listening_state= {"", "", "", "", ""};
						long startTime1 = System.currentTimeMillis();
						while((System.currentTimeMillis() - startTime1) / 1000 < 30) {
						try {
							WebElement waves = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_footer_v2_wave"));
							try {
							WebElement star_icon = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_icon"));
							System.out.println("Star icon visible");
							listening_state[0] = "Star icon";
							break;
							}catch(Exception e0) {
								continue;
							}
						}catch(Exception e0) {
							try {
								sec_mic = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
								sec_mic.click();
							}catch(Exception e) {
							}
						}
						}
						startTime1 = System.currentTimeMillis();
						while((System.currentTimeMillis() - startTime1) / 1000 < 30) {
						try {
							WebElement waves = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_footer_v2_wave"));
						try {
							WebElement greet_heading = new WebDriverWait(driver, Duration.ofSeconds(1)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
							System.out.println("Greeting "+greet_heading.getText());
							listening_state[1] = greet_heading.getText();
							break;
						}catch(Exception e0) {
							continue;
						}
					}catch(Exception e0) {
						try {
							sec_mic = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
							sec_mic.click();
						}catch(Exception e) {
						}
					}
					}
						startTime1 = System.currentTimeMillis();
						while((System.currentTimeMillis() - startTime1) / 1000 < 30) {
						try {
							WebElement waves = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_footer_v2_wave"));
						try {
							WebElement blinking_cursor = new WebDriverWait(driver, Duration.ofSeconds(1)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_v2_text_view_blinking_cursor")));
							WebElement speak_box = new WebDriverWait(driver, Duration.ofSeconds(1)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_v2_text_view")));
							listening_state[2] = "Blinking_cursor, "+speak_box.getText();
							System.out.println("Speak box "+listening_state[2]);
							break;
						}catch(Exception e0) {
							continue;
						}
					}catch(Exception e0) {
						try {
							sec_mic = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
							sec_mic.click();
						}catch(Exception e) {
						}
					}
					}
						startTime1 = System.currentTimeMillis();
						while((System.currentTimeMillis() - startTime1) / 1000 < 30) {
						try {
							WebElement waves = driver.findElement(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_footer_v2_wave"));
							System.out.println("Waves are visible");
							listening_state[4] = "Waves";
							break;
						}catch(Exception e0) {
							continue;
						}
					}
						String app = guess_app();
						System.out.println("App Name: "+app);
						scroll_right();
						String[] hints = allhints();
						data.add(new String[] {"Listening state - items ", listening_state[0]+", "+listening_state[1]+", "+listening_state[2]+", "+"waves"+", ", app, hints[0], hints[1], hints[2], hints[3], "", ""});
								
					
					}catch(Exception e3) {
						System.out.println("Secondary mic is not visible");
						data.add(new String[] {"", "Secondary mic could not be clicked", "", "", "", "", "", "", ""});
					}	
	}
	
	public static void audio_input_test() {
		String searchterm="", plp="", nulls="";
	System.out.println("***************************** Testing Audio Input  *******************************************");				
							
	try {
		WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
		if(surface.isDisplayed()) {
			try {
				WebElement sec_mic = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
				sec_mic.click();
			
				//Audio Testing
				try {
					WebElement waves = new WebDriverWait(driver, Duration.ofSeconds(3)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_footer_v2_wave")));
					callplayaudio("../TataDigitalOmniTest/src/test/resources/audio/showmemacfoundation.wav");
				}catch(Exception e) {
					System.out.println("Not in listening state or audio could not be played");
					try {
						surface = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
						if(surface.isDisplayed()) {
							try {
								sec_mic = new WebDriverWait(driver, Duration.ofSeconds(3)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
								sec_mic.click();
								callplayaudio("../TataDigitalOmniTest/src/test/resources/audio/showmemacfoundation.wav");
							}catch(Exception e0) {
								data.add(new String[] {"", "Mic could not be clicked", "", "", "", "", "", "", ""});
							}
						}
					}catch(Exception e1) {
						System.out.println("Surface was not visible");
						data.add(new String[] {"", "surface is not seen", "", "", "", "", "", "", ""});
					}
				}
				//response of audio
				int a = check_clarification_asked("Mac Foundation");
				if(a==2) {
					data.add(new String[] {"Audio_Testing - Mac foundation", "Works ", "", "","", "", "","", ""});
				}
				if(a!=2) {
				int x = mute_umnute();
				try {
				WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
				if(response.isDisplayed()) {
				String resp = getnlpresponse();
				int y = feedback();
				String app = guess_app();
				System.out.println("App Name: "+app);
				String[] hints = allhints();
				if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
					searchterm = search_bar_utterance(app);
					System.out.println("Value passed to the search bar = "+searchterm);
					plp=check_plp();
					nulls = product_shown();
				}
				if (a!=1){
					data.add(new String[] {"Audio_Testing - Mac foundation", resp,	app, hints[0],hints[1], hints[2], hints[3],searchterm, plp+"' "+nulls});
				}
				}		
				}catch(Exception e2) {
					System.out.println("Response not visible");
					data.add(new String[] {"", "Response not visible", "", "", "", "", "", "", ""});
				}		
				}
			}catch(Exception e3) {
				System.out.println("Secondary mic is not visible");
				data.add(new String[] {"", "secondary mic could not be clicked", "", "", "", "", "", "", ""});
			}
		}
	}catch(Exception e3) {
		System.out.println("Surface is not visible");
		teardown();
		ui_while();
		audio_input_test();
	}
	}
	
	public static void pause_play_test() {
		String searchterm="", plp="", nulls="";
		//Pause button
			System.out.println("***************************** Testing pause and play  *******************************************");
			try {
				String app = guess_app();
				System.out.println("App Name: "+app);
				WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
				if(surface.isDisplayed()) {
					try {
					WebElement pause = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[3]")));
					pause.click();
					System.out.println("Pause button is clicked");
					try {
					surface = new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
					if(surface.isDisplayed()) {
						System.out.println("Pause button does not works");
						data.add(new String[] {"Testing - Pause button", "Doesn't work ", app, "","", "", "","", ""});
					}
					}catch(Exception e8) {
						System.out.println("Pause button works. Surface is closed");
						data.add(new String[] {"Testing - Pause button", "works ", app, "","", "", "","", ""});
					}
					}catch(Exception e9) {
						System.out.println("Pause button not visible");
						data.add(new String[] {"", "Pause button could not be clicked", "", "", "", "", "", "", ""});
					}
				}
			}catch(Exception e10) {
				System.out.println("Surface not visible");
				teardown();
				ui_while();
				pause_play_test();
			}
			
			//Play button
				try {
					WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
					if(surface.isDisplayed()) {
						try {
						WebElement pause = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[3]")));
						pause.click();
						}catch(Exception e9) {
							System.out.println("Pause button not visible");
							data.add(new String[] {"", "pause could not be clicked", "", "", "", "", "", "", ""});
						}
					}
				}catch(Exception e10) {
					try {
					WebElement play = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[2]")));
					play.click();
					try {
						WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
						if(surface.isDisplayed()) {
							String resp = getnlpresponse();
							String app = guess_app();
							System.out.println("App Name: "+app);
							String[] hints = allhints();
							if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
								searchterm = search_bar_utterance(app);
								System.out.println("Value passed to the search bar = "+searchterm);
								plp=check_plp();
								nulls = product_shown();
							}
							data.add(new String[] {"Testing - Play button", "Works "+resp, app, hints[0],hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
						}
					}catch(Exception e9) {
						System.out.println("Surface not visible");
						data.add(new String[] {"Testing - Play button", "Doesn;t work", "", "","", "", "","", ""});
					}
					}catch(Exception e9) {
						System.out.println("Play button not visible");
						data.add(new String[] {"", "Play button could not be clicked", "", "", "", "", "", "", ""});
					}
				}
	}
	
	public static void background_back_btn_test() {
		// Testing background and back button when surface is open
				System.out.println("***************************** Testing background and back button  *******************************************");		
		try {
			WebElement close_ads = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.TextView[3]")));
			close_ads.click();
		}catch(Exception e) {
		}
		String app = guess_app();
		if(app.equalsIgnoreCase("Tata Cliq")) {
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
		try {
			WebElement product1 = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View[3]/android.view.View/android.view.View[1]/android.view.View[1]")));
			product1.click();
			System.out.println("First product from plp is clicked");
			try {
				WebElement brand = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View/android.view.View/android.widget.TextView")));
				if(brand.isDisplayed()) {
					driver.navigate().back();
					try {
						product1 = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View[3]/android.view.View/android.view.View[1]/android.view.View[1]")));
						if(product1.isDisplayed() && surface.isDisplayed()) {
							System.out.println("Interacting with the background and the Back button works");
							data.add(new String[] {"Testing - background interaction and back button", "works", "", "","", "", "","", ""});
						}
					}catch(Exception e10) {
						try {
							WebElement back = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.widget.Button")));
							back.click();
							try {
								product1 = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View[3]/android.view.View/android.view.View[1]/android.view.View[1]")));
							if(product1.isDisplayed() && surface.isDisplayed()) {
								System.out.println("Interacting with the background and the Back button works");
								data.add(new String[] {"Testing - background interaction and back button", "works", "", "","", "", "","", ""});
							}
							}catch(Exception e) {
								System.out.println("Could not navigate back");
								data.add(new String[] {"Testing - background interaction and back button", "Doesn't work", "", "","", "", "","", ""});
							}
						}catch(Exception e11) {
							System.out.println("Back button doesn't work");
							data.add(new String[] {"Testing - background interaction and back button", "Doesn't work", "", "","", "", "","", ""});
						}
					}
				}
			}catch(Exception e10) {
				System.out.println("Brand page could not be opened");
				data.add(new String[] {"Testing - background interaction and back button", "Doesn't work", "", "","", "", "","", ""});
			}
		}catch(Exception e10) {
			System.out.println("First product on plp could not clicked");
			data.add(new String[] {"Testing - background interaction and back button", "Doesn't work", "", "","", "", "","", ""});
		}
			}
		}catch(Exception e10) {
			System.out.println("Surface remains open");
			data.add(new String[] {"Testing - background interaction and back button", "Doesn't work", "", "","", "", "","", ""});
		}	
		}
	}
		
	public static void long_audio_test() {

System.out.println("***************************** Testing Long Audio Input  *******************************************");				

try {
	WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
	if(surface.isDisplayed()) {
		try {
			WebElement sec_mic = new WebDriverWait(driver, Duration.ofSeconds(8)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
			sec_mic.click();
		
			//Audio Testing
			try {
				WebElement waves = new WebDriverWait(driver, Duration.ofSeconds(3)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_footer_v2_wave")));
				callplayaudio("../TataDigitalOmniTest/src/test/resources/audio/longsentence.wav");
				try {
					WebElement input = new WebDriverWait(driver, Duration.ofSeconds(120)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_v2_fade_view_top")));
					System.out.println("scrolls up and fades");
					data.add(new String[] {"Testing - Long audio scroll up and faded text", "works", "", "","", "", "","", ""});
				}catch(Exception e10) {
					System.out.println("Input box could not be accessed");		
					data.add(new String[] {"input", "Input box could not be clicked", "", "", "", "", "", "", ""});
					}
			}catch(Exception e) {
				System.out.println("Not in listening state or audio could not be played");
				try {
					surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
					if(surface.isDisplayed()) {
						try {
							sec_mic = new WebDriverWait(driver, Duration.ofSeconds(3)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_mic")));
							sec_mic.click();
							callplayaudio("../TataDigitalOmniTest/src/test/resources/audio/longsentence.wav");
							try {
								WebElement input = new WebDriverWait(driver, Duration.ofSeconds(120)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_v2_fade_view_top")));
								System.out.println("scrolls up and fades");
								data.add(new String[] {"Testing - Long audio scroll up and faded text", "works", "", "","", "", "","", ""});
							}catch(Exception e10) {
								System.out.println("Input box could not be accessed");
								data.add(new String[] {"input", "Input box could not be clicked", "", "", "", "", "", "", ""});
								}
						}catch(Exception e0) {
							data.add(new String[] {"", "secondary mic could not be clicked", "", "", "", "", "", "", ""});
						}
					}
				}catch(Exception e0) {
					System.out.println("Surface was not visible");
					data.add(new String[] {"", "surface is not visible", "", "", "", "", "", "", ""});
				}
			}
		}catch(Exception e1) {
			System.out.println("Secondary mic was not visible");
			data.add(new String[] {"", "secondary mic could not be clicked", "", "", "", "", "", "", ""});
		}}
	}catch(Exception e2) {
		System.out.println("Surface was not visible");
		teardown();
		ui_while();
		long_audio_test();
	}
	}
	
	
	public static void ui_setting_ux(){
		String searchterm ="";
		try {
			hanshake_test();
			text_box_test();
			suspended_state_test();
			listening_state_test();
			audio_input_test();
			pause_play_test();
			background_back_btn_test();
			long_audio_test();
			teardown();
	System.out.println("**************************************************************************************");
		
		}catch(Exception e6) {
			System.out.println("Application could not be started");
		}
	}
	
	public static void llmsearch(String d) {
		String searchterm ="", plp="", nulls="";
		System.out.println("**************************************************************************************");
			try {
				WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
				if(surface.isDisplayed()) {	
					try {
						WebElement edit_text = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
						edit_text.click();
						Thread.sleep(700);
						edit_text.sendKeys(d);
						System.out.println("Utterance="+d);
						Thread.sleep(500);
						click_position(1313, 2820);
						int a = check_clarification_asked(d);
						if(a!=2) {
						WebElement response = new WebDriverWait(driver, Duration.ofSeconds(20)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
						String resp = getnlpresponse();
						String app = guess_app();
						System.out.println("App Name: "+app);
						String[] hints = allhints();
						if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
							searchterm = search_bar_utterance(app);
							System.out.println("Value passed to the search bar = "+searchterm);
							plp=check_plp();
							nulls = product_shown();
						}
						if (a!=1){
							data.add(new String[] {d, resp,app, hints[0],hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
						} 
						System.out.println("**************************************************************************************");
						System.out.println("Second clickable hint is clicked");
						sec_hint_clicked(d);
						}
					}catch(Exception e4) {
						System.out.println("Error while editing");
						data.add(new String[] {"edit", "Edit box could not be clicked", "", "", "", "", "", "", ""});
					}
				}
			}catch(Exception e0) {
				System.out.println("Surface is not open");
				teardown();
				ui_while();
				llmsearch(d);
			}
	}
	
	
	public static void horizontal_close() {
		//Horizontal close bar
				try {
				WebElement horizontal_close =new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_header_v2_horizontal_close_button")));
				try {
					WebElement droppable = driver.findElement(By.id("android:id/navigationBarBackground"));
					new Actions(driver).dragAndDrop(horizontal_close, droppable).perform();
					}catch(Exception e2) {
						System.out.println("Horizontal drop position not available");
					}
				}catch(Exception e1) {
					System.out.println("Horizontal close bar does not appears");
				}
	}
	
	
	public static void start_app() {
		try {
			WebElement grant_dialog = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.elementToBeClickable(By.id("com.android.permissioncontroller:id/grant_dialog")));
			if(grant_dialog.isDisplayed()) {
				try {
					WebElement dont_allow1 = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.id("com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button")));
					dont_allow1.click();
				}catch(Exception e) {
					System.out.println("Don't allow could not be clicked");
				}
			}
			}catch(Exception e0) {
				System.out.println("Grant dialog box is not visible");
			}
}
	
	public static void small_talk(String d) {
		ui_while();
		String plp="", nulls="";
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(20)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()){
			try {
				WebElement text_box = new WebDriverWait(driver, Duration.ofSeconds(20)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
				text_box.click();
				Thread.sleep(700);
				text_box.sendKeys(d);
				System.out.println("Utterance= "+d);
				Thread.sleep(500);
				click_position(1313, 2820);
				int a = check_clarification_asked(d);
				if(a!=2) {
				try {
				WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
				if(response.isDisplayed()) {
				String resp = getnlpresponse();
				String app = guess_app();
				System.out.println("App Name: "+app);
				String[] hints = allhints();
				plp=check_plp();
				nulls = product_shown();
				data.add(new String[] { d, resp, app, hints[0], hints[1], hints[2], hints[3],"", plp+" "+nulls});
				}
				}catch(Exception e) {
					System.out.println("Response not visible");
					data.add(new String[] {"response", "Response could not be clicked", "", "", "", "", "", "", ""});
				}
				}
			}catch(Exception e) {
				System.out.println("Text box could not be clicked");
				data.add(new String[] {"input", "Input box could not be clicked", "", "", "", "", "", "", ""});
			}
				}
			}catch(Exception e1) {
				teardown();
				small_talk(d);
			}
		teardown();
	}
	
	public static void ui_surface() {
		System.out.println("************************ Testing SmallTalk - Greeting ****************************");
		small_talk("Good morning");
		System.out.println("************************ Testing SmallTalk - Farewell ****************************");
		small_talk("Thank you");
		System.out.println("********************** Testing SmallTalk - Inside subapp **************************");	
		select_app_search_in_it("Electronics", "How can you help me");
		teardown();
	}
	
	
	public static void click_homepage_hints(String d, int x) {
		String searchterm ="", plp="", nulls="";
		System.out.println("Testing Clickable hint "+x);
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(25)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
		try {
			WebElement clickable_hint1 =new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.xpath(d)));
			String hint1 = clickable_hint1.getText();
			System.out.println("Hint "+x+" = "+hint1);
			clickable_hint1.click();
			int a = check_clarification_asked(hint1);
			if(a!=2) {
			try {
			WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
			if(response.isDisplayed()) {
			String resp = getnlpresponse();
			String app = guess_app();
			System.out.println("App Name: "+app);
			String[] hints = allhints();
			if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
				searchterm = search_bar_utterance(app);
				System.out.println("Value passed to the search bar = "+searchterm);
				plp=check_plp();
				nulls = product_shown();
			}
			if (a!=1){
				data.add(new String[] {hint1,resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
			}
			}
			}catch(Exception e0) {
				System.out.println("Response is not visible");
				data.add(new String[] {"", "Respnse is not visible", "", "", "", "", "", "", ""});
			}
			}
			System.out.println("**************************************************************************************");
			sec_hint_clicked(hint1);
			teardown();
		}catch(Exception e) {
			System.out.println("Hints don't work or it takes longer time to respond");
			data.add(new String[] {"", "Hint takes longer to respond", "", "", "", "", "", "", ""});
		}
			}
			}catch(Exception e2) {
				System.out.println("Surface is not open");
				try {
					WebElement assist = new WebDriverWait(driver, Duration.ofSeconds(120)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[4]")));
					assist.click();
					click_homepage_hints(d, x);
					}catch(Exception e1) {
						teardown();
						ui_while();
						click_homepage_hints(d, x);
					}
			}
		System.out.println("**************************************************************************************");
		
	}
		

	public static void click_homepage_hints() {
		String searchterm ="", plp="", nulls="";
		//fourth hint
				try {
					WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(120)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
					if(surface.isDisplayed()) {
				System.out.println("Testing Global hint 4");
				try {
					WebElement clickable_hint3 = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView")));
					String hint3 = clickable_hint3.getText();
					System.out.println("Hint3 = "+hint3);
					scroll();
				try {
					WebElement clickable_hint4 = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[4]/android.widget.TextView")));
					String hint4 = clickable_hint4.getText();
					System.out.println("Hint4 = "+hint4);
					if(!hint3.equals(hint4)) {
						clickable_hint4.click();
					}
					else {
						scroll();
						try {
							clickable_hint4 = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[4]/android.widget.TextView")));
							hint4 = clickable_hint4.getText();
							System.out.println("Hint4 = "+hint4);
						clickable_hint3.click();
						}catch(Exception e2) {
							data.add(new String[] {"", "Hint 4 is not visible", "", "", "", "", "", "", ""});
						}
					}
					int a = check_clarification_asked(hint4);
					if(a!=2) {
					try {
					WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
					if(response.isDisplayed()) {
					String resp = getnlpresponse();
					String app = guess_app();
					System.out.println("App Name: "+app);
					String[] hints = allhints();
					if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
						searchterm = search_bar_utterance(app);
						System.out.println("Value passed to the search bar = "+searchterm);
						plp=check_plp();
						nulls = product_shown();
					}
					if (a!=1){
						data.add(new String[] {hint4, resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
					}
					}
					}catch(Exception e0) {
						System.out.println("Response not seen");
						data.add(new String[] {"", "Response is not visible", "", "", "", "", "", "", ""});
					}
					}
					System.out.println("**************************************************************************************");
					sec_hint_clicked(hint4);
					teardown();
				}catch(Exception e) {
					try {
						WebElement clickable_hint4 = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView")));
						String hint4 = clickable_hint4.getText();
						System.out.println("Hint4 = "+hint4);
						clickable_hint4.click();
						int a = check_clarification_asked(hint4);
						if(a!=2) {
						try {
						WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
						if(response.isDisplayed()) {
						String resp = getnlpresponse();
						String app = guess_app();
						System.out.println("App Name: "+app);
						String[] hints = allhints();
						if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
							searchterm = search_bar_utterance(app);
							System.out.println("Value passed to the search bar = "+searchterm);
							plp=check_plp();
							nulls = product_shown();
						}
						if (a!=1){
							data.add(new String[] {hint4, resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
						}
						}
						}catch(Exception e0) {
							System.out.println("Response not seen");
							data.add(new String[] {"", "Response takes longer", "", "", "", "", "", "", ""});
						}
						}
						System.out.println("**************************************************************************************");
						sec_hint_clicked(hint4);
						teardown();
					}catch(Exception e1) {
						System.out.println("Hint 4 could not be found");
						data.add(new String[] {"", "Hint4 is not visible", "", "", "", "", "", "", ""});
					}
					
				}
				}catch(Exception e) {
					try {
						WebElement clickable_hint3 = new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView")));
						String hint3 = clickable_hint3.getText();
						System.out.println("Hint2 = "+hint3);
						clickable_hint3.click();
						int a = check_clarification_asked(hint3);
						if(a!=2) {
						try {
						WebElement response = new WebDriverWait(driver, Duration.ofSeconds(15)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_primary_v2_text")));
						if(response.isDisplayed()) {
						String resp = getnlpresponse();
						String app = guess_app();
						System.out.println("App Name: "+app);
						String[] hints = allhints();
						if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
							searchterm = search_bar_utterance(app);
							System.out.println("Value passed to the search bar = "+searchterm);
							plp=check_plp();
							nulls = product_shown();
						}
						if (a!=1){
							data.add(new String[] {hint3, resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp+" "+nulls});
						}
						}
						}catch(Exception e0) {
							System.out.println("Response not seen");
						}
						}
						System.out.println("**************************************************************************************");
						sec_hint_clicked(hint3);
					}catch(Exception e1) {
						System.out.println("Hints don't work or it takes longer time to respond");
						data.add(new String[] {"", "Hint doesn't work", "", "", "", "", "", "", ""});
					}
				}
				}
				}catch(Exception e2) {
					System.out.println("Surface is not open");
					try {
						WebElement assist = new WebDriverWait(driver, Duration.ofSeconds(120)).until(ExpectedConditions.elementToBeClickable(By.xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.Button[4]")));
						assist.click();
						click_homepage_hints();
						}catch(Exception e1) {
							teardown();
							ui_while();
							click_homepage_hints();
						}
				}	
				teardown();
	}
	
	public static void select_electronics() {
		try {
			WebElement surface = new WebDriverWait(driver, Duration.ofSeconds(120)).until(ExpectedConditions.presenceOfElementLocated(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_surface_v2_inner_card_container")));
			if(surface.isDisplayed()) {
		try {
			WebElement editing = new WebDriverWait(driver, Duration.ofSeconds(20)).until(ExpectedConditions.elementToBeClickable(By.id("com.example.flutter_omni_tata_neu:id/slang_lib_secondary_edit_text_v2_view")));
			editing.click();
			editing.clear();
			Thread.sleep(700);
			editing.sendKeys("iphone 14 pro");
			System.out.println("Utterance= iphone 14 pro");
			Thread.sleep(500);
			click_position(1313, 2820);
			Thread.sleep(2500);
		}catch(Exception e0) {
			System.out.println("Electronic app could not be selected");			}
			}
		}catch(Exception e) {
			teardown();
			ui_while();
			select_electronics();
		}
	}
	
	public static void TestCase0() {
		System.out.println("**************************** Testing Global hints *********************************");
		//first hint is clicked
		ui_while();
		try {
			Thread.sleep(1000);
		String[] hints=allhints();
		if(hints[0].equalsIgnoreCase("Ingredients for pesto pasta")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.TextView", 1);
		}
		else if(hints[1].equalsIgnoreCase("Ingredients for pesto pasta")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView", 2);
		}
		else if(hints[2].equalsIgnoreCase("Ingredients for pesto pasta")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView", 3);
		}
		else if(hints[3].equalsIgnoreCase("Ingredients for pesto pasta"))
		click_homepage_hints();
		}catch(Exception e) {System.out.println("First hint could not be clicked");}
		
		//second hint is clicked
		ui_while();
		try {
		String[] hints=allhints();
		if(hints[0].equalsIgnoreCase("Summer essentials")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.TextView", 1);
		}
		else if(hints[1].equalsIgnoreCase("Summer essentials")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView", 2);
		}
		else if(hints[2].equalsIgnoreCase("Summer essentials")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView", 3);
		}
		else if(hints[3].equalsIgnoreCase("Summer essentials"))
		click_homepage_hints();
		}catch(Exception e) {System.out.println("Second hint could not be clicked");}
		
		//third hint is clicked
		ui_while();
		try {
		String[] hints=allhints();
		if(hints[0].equalsIgnoreCase("Gaming setup")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.TextView", 1);
		}
		else if(hints[1].equalsIgnoreCase("Gaming setup")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView", 2);
		}
		else if(hints[2].equalsIgnoreCase("Gaming setup")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView", 3);
		}
		else if(hints[3].equalsIgnoreCase("Gaming setup"))
		click_homepage_hints();
		}catch(Exception e) {System.out.println("Third hint could not be clicked");}
		
		//fourth hint is clicked
		ui_while();
		try {
		String[] hints=allhints();
		if(hints[0].equalsIgnoreCase("First aid medicines")) {
			scroll_right();
			click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.TextView", 1);
		}
		else if(hints[1].equalsIgnoreCase("First aid medicines")) {
			scroll_right();
			click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.TextView", 2);
		}
		else if(hints[2].equalsIgnoreCase("First aid medicines")) {
			scroll_right();
		click_homepage_hints("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[3]/android.widget.TextView", 3);
		}
		else if(hints[3].equalsIgnoreCase("First aid medicines"))
		click_homepage_hints();
		}catch(Exception e) {System.out.println("Fourth hint could not be clicked");}
		
		System.out.println("**************************** Testing Domain FAQ *********************************");
		ui_while();
		llmsearch("What do you recommend for lunch");
		llmsearch("What are the benefits of ginger");
		llmsearch("What is the difference between top load and front load washing machine");
		llmsearch("can I have Dolo 650 in empty stomach");
		llmsearch("What fabric is best to be worn in summer");
		llmsearch("I am planning to make chapati. show me pans to make chapatis");
		llmsearch("What are some tennis rackets for intermediate players");
		System.out.println("**************************************************************************************");
				teardown();
	}
	
	public static void TestCase1() {
		ui_while();
		System.out.println("*************************** Test cases *********************************");
		System.out.println("TestCase1:a: From home page, re-directed to correct sub app");	
		home_page_redirected_sub_app("Oil");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase1:b: Searching in the sub app");
		sub_app_search_and_hint_clicked("colgate");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase1:c: Clicking the second hint inside the sub app");
		sec_hint_clicked("colgate");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase1:d: From sub app, re-directed to another sub app");
		sub_app_search_another_sub_app("4k ultra HD TV");
		teardown();
	}
	
	
	public static void TestCase2() {
		ui_while();
		System.out.println("TestCase2:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("ceiling fan");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase2:b: Searching in the sub app");
		sub_app_search_and_hint_clicked("SONY Playstation 5 Gaming Console");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase2:c: Clicking the second hint inside the sub app");
		sec_hint_clicked("SONY Playstation 5 Gaming Console");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase2:d: From sub app, re-directed to another sub app");
		sub_app_search_another_sub_app("paracetamol");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase2:e: From sub app, Disambiguating");
		sub_app_search_and_hint_clicked("black urad dal");
		teardown();
}
	
	public static void TestCase3() {
		ui_while();
		System.out.println("TestCase3:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("cough syrup");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase3:b: Searching in the sub app");
		sub_app_search_and_hint_clicked("Antifungal Dusting Powder for Sweat Rash, Itching, Skin Irritation, Chafing & Redness");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase3:c: Clicking the second hint inside the sub app");
		sec_hint_clicked("Antifungal Dusting Powder for Sweat Rash, Itching, Skin Irritation, Chafing & Redness");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase3:d: From sub app, re-directed to another sub app");
		sub_app_search_another_sub_app("Red Skirt with dupatta");
		teardown();
}
	
	public static void TestCase4() {
		ui_while();
		System.out.println("TestCase4:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("Dining Table with ladder chairs");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase4:b: Searching in the sub app");
		sub_app_search_and_hint_clicked("Suggest a refrigerator for 5 member family");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase4:c: Clicking the second hint inside the sub app");
		sec_hint_clicked("Suggest a refrigerator for 5 member family");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase4:d: From sub app, Failure utterance");
		sub_app_search_another_sub_app("Blah blah blah");
		teardown();
}
	
	public static void TestCase5() {
		ui_while();
		System.out.println("TestCase5:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("WES Casuals Black & Brown Checked Slim Fit Shirt");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase5:b: Searching in the sub app");
		sub_app_search_and_hint_clicked("Black kurta");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase5:c: Clicking the second hint inside the sub app");
		sec_hint_clicked("Black kurta");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase5:d: From sub app, re-directed to another sub app");
		sub_app_search_another_sub_app("aashirvaad atta");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase5:e: From sub app, Disambiguating");
		sub_app_search_and_hint_clicked("I am going for a party tonight, but my hair is curled. Show me a hair straightner to iron my hair");
		teardown();
}
	
	public static void TestCaselab() {
		ui_while();
		System.out.println("TestCase6:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("Blood test for liver functioning");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase6:b: Searching in the sub app");
		sub_app_search_and_hint_clicked("I am suffering from slip disc, i want to do a spine x-ray");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase6:c: Clicking the second hint inside the sub app");
		sec_hint_clicked("I am suffering from slip disc, i want to do a spine x-ray");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase6:d: From sub app, re-directed to another sub app");
		sub_app_search_another_sub_app("Thyronorm 75 mcg");
		teardown();
}
	
	public static void TestCase7() {
		ui_while();
		System.out.println("***************************** Unsupported ********************************************");
		System.out.println("TestCase7:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("How far is the Earth from the moon");
		System.out.println("**************************************************************************************");
		select_electronics();
		System.out.println("TestCase7:b: Searching unsupported in the sub app");
		sub_app_search_and_hint_clicked("Can human live in mars planet");
		teardown();
}
	
	
	
	public static void TestCase8() {
		ui_while();
		System.out.println("***************************** Disambiguation *******************************************");
		System.out.println("TestCase 8:a: From home page, re-directed to correct sub app");
		disamb_from_home("Apple", "electronics");
		teardown();
		ui_while();
		System.out.println("***************************** Disambiguation *******************************************");
		disamb_from_home("Apple", "grocery");
		teardown();
	}
	
	
	public static void TestCase9() {
		ui_while();
		System.out.println("***************************** Filter Search *******************************************");
		System.out.println("TestCase 9:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("Men's shirt from Adidas");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase 9:b: Searching in the sub app");
		sub_app_search_and_hint_clicked("how about for my wife");
		System.out.println("**************************************************************************************");
		teardown();
}
	
	
	public static void TestCase10() {
		ui_while();
		System.out.println("***************************** Filter Search *******************************************");
		System.out.println("TestCase10:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("Do you have shampoo products");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase10:b: Searching in the sub app");
		sub_app_search_and_hint_clicked("but i have dry hair");
		System.out.println("**************************************************************************************");
		teardown();
}
	
	public static void TestCase11() {
		String searchterm = "", plp="";
		ui_while();
		System.out.println("***************************** Recipe Search *******************************************");
		System.out.println("TestCase11:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("How to cook egg burji");
		System.out.println("*************************** Next Step *****************************************");
		scroll_right();
		recipe_scroll_left();
		try {
		int a = check_clarification_asked("How to cook egg burji");
		if(a!=2) {
		String resp = getnlpresponse();
		String app = guess_app();
		String[] hints = allhints();
		if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
			searchterm = search_bar_utterance(app);
			System.out.println("Value passed to the search bar = "+searchterm);
		}
		plp=check_plp();
		data.add(new String[] {"Swipe next step", resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp});
		}
		}catch(Exception e) {}
		System.out.println("************************** Previous Step ***************************************");
		recipe_scroll_right();
		try {
			int a = check_clarification_asked("How to cook egg burji");
			if(a!=2) {
			String resp = getnlpresponse();
			String app = guess_app();
			String[] hints = allhints();
			if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
				searchterm = search_bar_utterance(app);
				System.out.println("Value passed to the search bar = "+searchterm);
			}
			plp=check_plp();
			data.add(new String[] {"Swipe previous step", resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp});
			}
			}catch(Exception e) {}
		System.out.println("**************************************************************************************");
		try {
			scroll_right();
			first_hint_click();
		}catch(Exception e) {
		}
		try {
			Thread.sleep(1000);
		}catch(Exception e) {}
		sub_app_search_and_hint_clicked("Give me the recipe for chicken dum biriyani");
		System.out.println("**************************************************************************************");
		recipe_scroll_left();
		try {
			int a = check_clarification_asked("How to cook egg burji");
			if(a!=2) {
			String resp = getnlpresponse();
			String app = guess_app();
			String[] hints = allhints();
			if((!app.equalsIgnoreCase("Home Page"))||(!app.equalsIgnoreCase("navigated")))	{
				searchterm = search_bar_utterance(app);
				System.out.println("Value passed to the search bar = "+searchterm);
			}
			plp=check_plp();
			data.add(new String[] {"Swipe next step", resp, app, hints[0], hints[1], hints[2], hints[3],searchterm, plp});
			}
			}catch(Exception e) {}
		try {
			scroll_right();
			first_hint_click();
    	}catch(Exception e) {}
		System.out.println("**************************************************************************************");
		teardown();
}
		
	public static void TestCase12() {
		ui_while();
		System.out.println("***************************** Gift Search *******************************************");
		System.out.println("TestCase12:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("What can i gift my 14 year old son who just finished his high school");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase12:b: Searching in the sub app");
		select_electronics();
		sub_app_search_and_hint_clicked("Suggest something to gift my newphew for his birthday on pokemon theme");
		System.out.println("**************************************************************************************");
		teardown();
}
	
	public static void TestCase13() {
		ui_while();
		System.out.println("***************************** List Search *******************************************");
		System.out.println("TestCase13:a: From home page, re-directed to correct sub app");
		home_page_redirected_sub_app("Tomato, onion, cucumber");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase13:b: Searching in the sub app");
		sub_app_search_and_hint_clicked("Floral satin saree, high heels, pearl jewllery set");
		System.out.println("**************************************************************************************");
		teardown();
}
	
	public static void TestCasenavi() {
		ui_while();
		System.out.println("***************************** Navigation *******************************************");
		System.out.println("TestCase14:a: From home page, re-directed to correct sub app");
		page_redirected("i want to invest 5000 rupees in digital gold");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase14:b: Searching in the sub app");
		page_redirected("I want to pay by electricity bill");
		System.out.println("**************************************************************************************");
		System.out.println("TestCase14:c: Searching in the sub app");
		page_redirected("I want to apply for tata neu credit card");
		System.out.println("**************************************************************************************");
		teardown();
}
	
	
	 public static int readCSV(String file1Path, String file2Path) {
		 int flag =1;
		 String[] act_utterance = {"Testing play and pause before trigger",	"Greeting state - items",	"Testing play and pause after manually closing the surface",	"Input box and send Button",	"Mute and feedback",	"Orange",	"Suspended state - items",	"Listening state - items",	"Testing - Pause button",	"Testing - Play button",	"Testing - background interaction and back button",	"Testing - Long audio scroll up and faded text",	"Good morning",	"Thank you",	"How can you help me",	"Ingredients for pesto pasta",	"pine nuts",	"Summer essentials",	"flip-flops",	"Gaming setup",	"gaming mouse",	"First aid medicines",	"adhesive tape",	"What do you recommend for lunch",	"chicken curry",	"edit",	"What is the difference between top load and front load washing machine",	"Which type of washing machine is more energy efficient?",	"can I have Dolo 650 in empty stomach",	"Crocin",	"What fabric is best to be worn in summer",	"No hint",	"I am planning to make chapati. show me pans to make chapatis",	"aluminum tawa",	"What are some tennis rackets for intermediate players",	"Oil",	"colgate",	"4k ultra HD TV",	"ceiling fan",	"SONY Playstation 5 Gaming Console",	"Nintendo Switch Gaming Console",	"paracetamol",	"black urad dal",	"cough syrup",	"Antifungal Dusting Powder for Sweat Rash, Itching, Skin Irritation, Chafing & Redness",	"antifungal cream",	"Red Skirt with dupatta",	"Dining Table with ladder chairs",	"Suggest a refrigerator for 5 member family",	"energy-efficient refrigerator",	"Blah blah blah",	"WES Casuals Black & Brown Checked Slim Fit Shirt",	"Black kurta",	"red kurta",	"aashirvaad atta",	"I am going for a party tonight, but my hair is curled. Show me a hair straightner to iron my hair",	"Blood test for liver functioning",	"I am suffering from slip disc, i want to do a spine x-ray",	"CT scan for spine",	"Thyronorm 75 mcg",	"How far is the Earth from the moon",	"Can human live in mars planet",	"Apple",	"electronics",	"Orange",	"grocery",	"fashion",	"Orange",	"Men's shirt from Adidas",	"how about for my wife",	"Do you have shampoo products",	"but i have dry hair",	"How to cook egg burji",	"Swipe next step",	"Swipe previous step",	"eggs",	"Give me the recipe for chicken dum biriyani",	"Swipe next step",	"",	"What can i gift my 14 year old son who just finished his high school",	"Suggest something to gift my newphew for his birthday on pokemon theme",	"Tomato, onion, cucumber",	"Floral satin saree, high heels, pearl jewllery set",	"i want to invest 5000 rupees in digital gold",	"I want to pay by electricity bill",	"I want to apply for tata neu credit card"};
		 String[] act_resp = {"Doesn't work",	"star icon, Hi, I am AI search, Give me a clue & I’ll find it for you - groceries, gadgets, latest styles or meds, Try typing \"What is the…\", Secondary mic",	"Doesn't work",	"Works",	"Works",	"Here are the search results for oranges",	"Star icon, Give me a clue & I’ll find it for you - groceries, gadgets, latest styles or meds, Try typing \"What is the…\", Secondary mic",	"Star icon, Give me a clue & I’ll find it for you - groceries, gadgets, latest styles or meds, Blinking_cursor, what is working for some reason if doesn't that I am telling, waves,",	"works",	"Mac Foundation",	"works",	"works",	"Good morning!",	"You're welcome!",	"I'm",	"pesto pasta.",	"pesto pasta.",	"essential summer products",	"summer products",	"gaming setup",	"gaming setup",	"first aid medicines",	"first aid medicines",	"",	"lunch",	"Edit box could not be clicked",	"Top load washing machines",	"washing machine",	"dolo",	"dolo",	"summer",	"No clickable hints are seen",	"chapati pans",	"chapati pans",	"tennis",	"oil",	"colgate",	"",	"ceiling fans",	"Gaming Console",	"Gaming Console",	"paracetamol",	"black urad dal",	"cough syrup",	"antifungal dusting powder",	"antifungal dusting powder",	"red skirt",	"dining table",	"refrigerators",	"refrigerators",	"puzzler",	"shirt",	"black kurta",	"black kurta",	"Aashirvaad Atta",	"hair straighteners",	"blood test",	"spine x-ray",	"spine x-ray",	"Thyronorm",	"puzzler",	"puzzler",	"Disambiguation Please select one of the categories",	"",	"orange",	"",	"",	"orange",	"shirt",	"shirt",	"shampoo",	"dry hair",	"egg burji",	"Sauté the onions until they turn golden brown.",	"egg burji",	"egg burji",	"chicken dum biriyani",	"chicken dum biriyani",	"First clickable hint could not be clicked",	"gift",	"gift",	"Here is your shopping list...",	"Here is your shopping list...",	"Sure, taking you to the digital gold investment page...",	"Sure, taking you to the bill payment page...",	"Sure, taking you to the credit card application page..."};
		 String[] act_app = {"",	"",	"",	"",	"",	"bigbasket",	"bigbasket",	"bigbasket",	"Tata Cliq",	"Tata Cliq",	"",	"",	"Home Page",	"Home Page",	"Croma",	"bigbasket",	"bigbasket",	"Tata Cliq",	"Tata Cliq",	"Croma",	"Croma",	"Tata 1mg",	"Tata 1mg",	"Home Page",	"bigbasket",	"",	"",	"",	"Tata 1mg",	"Tata 1mg",	"Tata 1mg",	"",	"",	"bigbasket",	"Tata Cliq",	"bigbasket",	"bigbasket",	"croma",	"croma",	"croma",	"Croma",	"Tata 1mg",	"bigbasket",	"Tata 1mg",	"Tata 1mg",	"Tata 1mg",	"Tata Cliq",	"Tata Cliq",	"croma",	"Croma",	"Croma",	"Tata Cliq",	"Tata Cliq",	"Tata Cliq",	"bigbasket",	"Tata Cliq",	"Tata 1mg",	"Tata 1mg",	"Tata 1mg",	"Tata 1mg",	"",	"",	"",	"Croma",	"bigbasket",	"bigbasket",	"Tata Cliq",	"bigbasket",	"Tata Cliq",	"Tata Cliq",	"Tata 1mg",	"Tata 1mg",	"bigbasket",	"bigbasket",	"bigbasket",	"bigbasket",	"bigbasket",	"bigbasket",	"",	"Tata Cliq",	"Tata Cliq",	"bigbasket",	"Tata Cliq",	"",	"",	""};
		 String[] act_hint1 = {"",	"Summer essentials",	"",	"",	"",	"orange",	"Gaming setup",	"",	"",	"Mac Foundation",	"",	"",	"Ingredients for pesto pasta",	"Ingredients for pesto pasta",	"",	"pasta",	"pasta",	"sunglasses",	"sunglasses",	"144 hz monitor",	"144 hz monitor",	"bandages",	"bandages",	"dal",	"vegetables",	"",	"Which type of washing machine is more energy efficient?",	"Ingredients for pesto pasta",	"Dolo 650",	"Dolo 650",	"",	"",	"chapati pans",	"non-stick tawa",	"",	"oil",	"electronics",	"",	"ceiling fan",	"SONY Playstation 5 Gaming Console",	"SONY Playstation 5 Gaming Console",	"paracetamol",	"black urad dal",	"honey-based cough syrup",	"antifungal dusting powder",	"antifungal dusting powder",	"red skirt",	"dining table",	"double door refrigerator",	"double door refrigerator",	"FAQs",	"",	"black kurta",	"blue kurta",	"Aashirvaad Atta",	"hair straightener",	"",	"",	"",	"Thyronorm 75 mcg",	"FAQs",	"FAQs",	"electronics",	"Apple products",	"oranges",	"apples",	"",	"",	"",	"",	"conditioner",	"shampoo for dry hair",	"eggs",	"eggs",	"eggs",	"eggs",	"",	"",	"",	"smartwatch",	"Pokemon merchandise",	"tomato",	"floral satin saree",	"Ingredients for pesto pasta",	"Ingredients for pesto pasta",	"Ingredients for pesto pasta"};
		 String[] act_hint2 = {"",	"Gaming setup",	"",	"",	"",	"apple",	"Summer essentials",	"",	"",	"liquid foundation",	"",	"",	"Summer essentials",	"Summer essentials",	"",	"pesto sauce",	"pesto sauce",	"sunscreen",	"sunscreen",	"mechanical keyboard",	"mechanical keyboard",	"antiseptic cream",	"antiseptic cream",	"vegetables",	"chicken curry",	"",	"",	"First aid medicines",	"paracetamol",	"paracetamol",	"",	"",	"cast iron tawa",	"aluminum tawa",	"",	"",	"grocery",	"",	"table fan",	"Microsoft Xbox Series X Gaming Console",	"Microsoft Xbox Series X Gaming Console",	"ibuprofen",	"organic black urad dal",	"herbal cough syrup",	"antifungal cream",	"antifungal cream",	"flared red skirt",	"dining table with bench",	"frost-free refrigerator",	"frost-free refrigerator",	"Chat with us",	"",	"white kurta",	"red kurta",	"whole wheat flour",	"curling iron",	"",	"",	"",	"Eltroxin 75 mcg",	"Chat with us",	"Chat with us",	"grocery",	"iphone",	"mandarin oranges",	"red apples",	"",	"",	"",	"",	"hair oil",	"conditioner",	"onions",	"onions",	"onions",	"onions",	"",	"",	"",	"wireless earbuds",	"Pokemon t-shirts",	"onion",	"high heels",	"Summer essentials",	"Summer essentials",	"Summer essentials"};
		 String[] act_hint3 = {"",	"First aid medicines",	"",	"",	"",	"banana",	"First aid medicines",	"",	"",	"powder foundation",	"",	"",	"Gaming setup",	"Gaming setup",	"",	"pine nuts",	"pine nuts",	"beach hats",	"beach hats",	"gaming mouse",	"gaming mouse",	"cotton swabs",	"cotton swabs",	"chicken curry",	"salad",	"",	"",	"Summer essentials",	"Crocin",	"Crocin",	"",	"",	"non-stick tawa",	"roti tawa",	"",	"",	"grocery",	"",	"tower fan",	"SONY Playstation 4 Gaming Console",	"SONY Playstation 4 Gaming Console",	"aspirin",	"split black urad dal",	"dry cough syrup",	"calamine lotion",	"calamine lotion",	"pleated red skirt",	"extendable dining table",	"side-by-side refrigerator",	"side-by-side refrigerator",	"",	"",	"blue kurta",	"green kurta",	"multigrain flour",	"hair curlers",	"",	"",	"",	"Thyrox 75 mcg",	"",	"",	"",	"macbook",	"blood oranges",	"green apples",	"",	"",	"",	"",	"hair mask",	"hair oil",	"tomatoes",	"tomatoes",	"tomatoes",	"tomatoes",	"",	"",	"",	"backpack",	"Pokemon action figures",	"cucumber",	"pearl jewelry set",	"Gaming setup",	"Gaming setup",	"Gaming setup"};
		 String[] act_hint4 = {"",	"Ingredients for pesto pasta",	"",	"",	"",	"mango",	"Ingredients for pesto pasta",	"",	"",	"stick foundation",	"",	"",	"First aid medicines",	"First aid medicines",	"",	"garlic",	"garlic",	"summer dresses",	"summer dresses",	"gaming pc",	"gaming pc",	"first aid kits",	"first aid kits",	"roti",	"roti",	"",	"",	"Gaming setup",	"Saridon",	"Combiflam",	"",	"",	"flat griddle",	"flat griddle",	"",	"",	"",	"",	"pedestal fan",	"SONY Playstation 4 Gaming Console",	"SONY Playstation 4 Gaming Console",	"cough syrup",	"black lentils",	"cough syrup",	"calamine lotion",	"tea tree oil",	"asymmetric red skirt",	"4-seater dining table",	"refrigerator",	"refrigerator",	"",	"",	"yellow kurta",	"yellow kurta",	"rice flour",	"hair styling cream",	"",	"",	"",	"Thyronorm 100 mcg",	"",	"",	"",	"ipad",	"navel oranges",	"organic apples",	"",	"",	"",	"",	"dry shampoo",	"dry shampoo",	"garam masala",	"garam masala",	"garam masala",	"garam masala",	"",	"",	"",	"fitness tracker",	"Pokemon trading cards",	"cucumber",	"pearl jewelry set",	"First aid medicines",	"First aid medicines",	"First aid medicines"};
		 String[] act_searchterm = {"",	"",	"",	"",	"",	"orange",	"",	"",	"",	"Mac Foundation",	"",	"",	"",	"",	"",	"pasta",	"pine nuts",	"Sunglasses",	"Flip Flops",	"",	"",	"Showing results for bandages",	"Showing results for adhesive tape",	"",	"chicken curry",	"",	"",	"",	"Showing results for Dolo 650",	"Showing results for Crocin",	"Showing results for Crocin",	"",	"",	"",	"tennis",	"",	"",	"",	"",	"Results for \"SONY Playstation 5 Gaming Console\"(19)",	"",	"Showing results for paracetamol",	"",	"Showing results for honey-based cough syrup",	"Showing results for antifungal dusting powder",	"Showing results for antifungal cream",	"Red Skirt",	"Dining Table",	"Results for \"double door refrigerator\"(202)",	"",	"",	"",	"Black Kurta",	"Red Kurta",	"Aashirvaad Atta",	"",	"",	"",	"",	"Showing results for Thyronorm 75 mcg",	"",	"",	"",	"",	"",	"",	"",	"apples",	"",	"",	"Showing results for conditioner",	"Showing results for shampoo for dry hair",	"eggs",	"eggs",	"eggs",	"eggs",	"eggs",	"eggs",	"",	"Smartwatch",	"Pokemon Merchandise",	"tomato",	"Floral Satin Saree",	"",	"",	""};
		 int act_sc[] = {52,	52,	52,	52,	52,	39,	52,	24,	52,	30,	52,	52,	52,	52,	19,	39,	10,	29,	10,	29,	10,	29,	10,	12,	10,	52,	16,	7,	19,	10,	21,	52,	21,	8,	27,	27,	18,	27,	34,	27,	8,	27,	34,	27,	34,	8,	27,	27,	27,	8,	19,	27,	27,	8,	27,	19,	52,	52,	52,	27,	47,	47,	32,	18,	27,	18,	18,	18,	27,	18,	19,	19,	27,	18,	18,	18,	27,	18,	52,	19,	27,	27,	52,	43,	43,	43};
		 try {
		 BufferedReader reader1 = new BufferedReader(new FileReader(file1Path));
	     BufferedReader reader2 = new BufferedReader(new FileReader(file2Path));
	            String line1, line2; int count=0; 
	            while ((line2 = reader2.readLine()) != null) {	            	
	            	// Configure OpenCSV parser
	                CSVParser csvParser = new CSVParserBuilder().withSeparator(',').withIgnoreQuotations(false).build();

	                // Parse CSV row into a string array
	                String[] rowArray2 = csvParser.parseLine(line2);
	                int score=0;
	                
	                for(int j=0;j<act_utterance.length;j++) {
	     	           if(rowArray2[0].equals(act_utterance[j])) {
	     	        		// Convert lists to sets
	     	        		Set<String> finalHintsSet = new HashSet<>(Arrays.asList(act_hint1[j].toLowerCase(), act_hint2[j].toLowerCase(), act_hint3[j].toLowerCase(), act_hint4[j].toLowerCase()));
	     	        	   
	     	        		 if(rowArray2[0].toLowerCase().contains(act_utterance[j].toLowerCase())) 
	     	                	score += 10;
	     	        		if(rowArray2[1].toLowerCase().contains(act_resp[j].toLowerCase())) 
	     	                	score += 9;
	     	        		if(rowArray2[2].toLowerCase().contains(act_app[j].toLowerCase())) 
	     	                	score += 8;
	     	        		if(finalHintsSet.contains(rowArray2[3].toLowerCase())) 
	     	                	score += 7;
	     	        		if(finalHintsSet.contains(rowArray2[4].toLowerCase())) 
	     	                	score += 6;
	     	        		if(finalHintsSet.contains(rowArray2[5].toLowerCase())) 
	     	                	score += 5;
	     	        		if(finalHintsSet.contains(rowArray2[6].toLowerCase())) 
	     	                	score += 4;
	     	        		if(rowArray2[7].toLowerCase().contains(act_searchterm[j].toLowerCase())) 
	     	                	score += 3;
	     	        	  }
	     	           }
	                
	             
	            for(int j=0;j<act_utterance.length;j++) {
	            	if(rowArray2[0].equals(act_utterance[j])) {
	            		if(score<act_sc[j]) {
	            			flag=0;
	            			System.out.println("Row number = "+(count+1)+" failed");
	            			System.out.println("Actual Value = "+(Arrays.toString(rowArray2))+"Actual Score="+score);
	        	            System.out.println("Expected Value ="+act_utterance[j]+","+act_resp[j]+","+act_app[j]+","+act_hint1[j]+","+act_hint2[j]+","+act_hint3[j]+","+act_hint4[j]+","+act_searchterm[j]+"Expected score="+act_sc[j]);
	            		}
	            	}
	             }
	            count++;
	           }
	        } catch (IOException e) {
	            e.printStackTrace();
	        }
		 
		 
	        return flag;
	    }
		
	public static void main(String[] args) {
		
		 LocalDate currentDate = LocalDate.now();
	     String formattedDate = currentDate.format(DateTimeFormatter.ofPattern("dd_MM_yyyy"));
	     String d = "../TataDigitalOmniTest/Output_TD/Stage_2XX" + formattedDate + ".csv";

		try {
			File file = new File(d); 
			FileWriter outputfile = new FileWriter(file); 
			CSVWriter writer = new CSVWriter(outputfile); 
	    
	   
		ui_setting_ux(); 
		 writer.writeAll(data); 
		 data.clear();
			
		//Surface Testing
		ui_surface();
			writer.writeAll(data); 
			data.clear();
		
		//clickable hints from home page
		TestCase0();
			writer.writeAll(data); 
			data.clear();
			
		//Test cases
		TestCase1();
			writer.writeAll(data); 
			data.clear();
		TestCase2();
			writer.writeAll(data); 
			data.clear();
		TestCase3();
			writer.writeAll(data); 
			data.clear();
		TestCase4();
			writer.writeAll(data); 
			data.clear();
		TestCase5();
			writer.writeAll(data); 
			data.clear();
		
		//Lab
		TestCaselab();
			writer.writeAll(data); 
			data.clear();
		
		//Unsupported
		TestCase7();
			writer.writeAll(data); 
			data.clear();
		
		//disambiguation
		TestCase8();
			writer.writeAll(data); 
			data.clear();
		
		//Filter data
		TestCase9();
			writer.writeAll(data); 
			data.clear();
		TestCase10();
			writer.writeAll(data); 
			data.clear();
		
		//Receipe search
		TestCase11();
			writer.writeAll(data); 
			data.clear();
				
		//Gift search
		TestCase12();
			writer.writeAll(data); 
			data.clear();
		
		//List search
		TestCase13();
			writer.writeAll(data); 
			data.clear();
		
		//Navigation
		TestCasenavi();
		 	writer.writeAll(data); 
		 	data.clear();
		  
	        // closing writer connection 
	        writer.close(); 
			}catch(Exception e) {
				System.out.println("File could not be created"+e.getMessage());}
		
		System.out.println("**************************************************************************************");
		
		
		//File compare
		 String file1Path = "../TataDigitalOmniTest/src/test/resources/TD_Compare/Prod_V125.csv";
	     String file2Path = d;

	     int flag = readCSV(file1Path, file2Path);
	     if(flag==1)
   	    	 System.out.println("Pass");	
	     
	     
//	     //Testing from the TD utterace file
//	     String d1 = "../TataDigitalOmniTest/Output_TD/Stage_" + formattedDate + "1.csv";
//	     String csvFilePath = "/Users/divyac/Documents/AppiumProject/TataDigitalOmniTest/src/test/resources/Files required/TD utterances Combined.csv";
////	     String csvFilePath = "/Users/divyac/Documents/AppiumProject/TataDigitalOmniTest/src/test/resources/Files required/TD utterances1.csv";
//	     try (CSVReader csvReader = new CSVReaderBuilder(new FileReader(csvFilePath)).build()){
//	    	try {
//	    		File file = new File(d1); 
//	    		FileWriter outputfile = new FileWriter(file); 
//	    		CSVWriter writer = new CSVWriter(outputfile); 
//	    		data.add(new String[] {"Utterance", "Response", "App", "Hints1", "Hints2", "Hint3", "Hint4", "Search Term", "PLP Count", "Product shown"}); 
//	    		ui_while();
//	    		Thread.sleep(2500);
//	    		String[] line;
//	    		int count=0;    
//	    		writer.writeAll(data); 
//	    		while ((line = csvReader.readNext()) != null){
//	    			for (String value : line) {
//	    				System.out.println("**************************************************************************************");
//	    				count++;
//	    				System.out.println("No:"+count);
//	    				home_page_redirected_sub_app(value);
//	    				writer.writeAll(data);
//	    				if(count%5==0 && count!=0) {
//	    					data.clear();
//	    					teardown();
//	    					ui_while();
//	    				}
//	    			}
//	    		}
//	     		disamb_from_home("Apple", "electronics");
//	    		writer.writeAll(data);
//	    	}catch(Exception e) {System.out.println("Output file could not be cicked");}
//	     }catch(Exception e1) {System.out.println("Input file could not be cicked");}
	     teardown();
	}
}

 
