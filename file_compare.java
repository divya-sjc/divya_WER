package TataDigitalOmniTest;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.opencsv.CSVParser;
import com.opencsv.CSVParserBuilder;

public class file_compare {
	    // Method to read CSV file and return data as a list of arrays of strings
	 public static int[] readCSV(String file1Path, String file2Path) {
		 List<String[]> lines = new ArrayList<>();
		 int[] finalscore = new int[100];
		 try {
		 BufferedReader reader1 = new BufferedReader(new FileReader(file1Path));
	     BufferedReader reader2 = new BufferedReader(new FileReader(file2Path));
	            String line1, line2; int count=0;
	            while ((line1 = reader1.readLine()) != null && (line2 = reader2.readLine()) != null) {	            	
	            	// Configure OpenCSV parser
	                CSVParser csvParser = new CSVParserBuilder().withSeparator(',').withIgnoreQuotations(false).build();

	                // Parse CSV row into a string array
	                String[] rowArray1 = csvParser.parseLine(line1);
	                String[] rowArray2 = csvParser.parseLine(line2);
	                int score=0;
	                for(int i=0;i<rowArray1.length;i++) {
	                if(rowArray1[i].equalsIgnoreCase(rowArray2[i]))
	                	score += (rowArray1.length - i);
	                }
//	                System.out.println("Line "+count+"="+score);
	                finalscore[count]=score;
	                count++;
	            }
	        } catch (IOException e) {
	            e.printStackTrace();
	        }

	        return finalscore;
	    }
	}

