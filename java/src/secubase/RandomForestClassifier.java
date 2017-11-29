package secubase;

import java.io.File;

import weka.classifiers.Evaluation;
import weka.classifiers.misc.InputMappedClassifier;
import weka.classifiers.trees.RandomForest;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.CSVSaver;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.NumericToNominal;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.attribute.Reorder;
import weka.filters.unsupervised.attribute.StringToNominal;

public class RandomForestClassifier {

	public void classificationCSV(RandomForest classification, String input, String output, int classIndex_minus)
			throws Exception {

		String path = System.getProperty("user.dir");
		String Out_path = path + '\\' + output;
		DataSource source = new DataSource(input);

		Instances olddata = source.getDataSet();
		if (olddata.classIndex() == -1)
			olddata.setClassIndex(olddata.numAttributes() - classIndex_minus);

		NumericToNominal convert = new NumericToNominal();
		String[] optionc = new String[2];
		optionc[0] = "-R";
		optionc[1] = "1, last"; // range of variables to make numeric

		convert.setOptions(optionc);
		convert.setInputFormat(olddata);

		Instances data = Filter.useFilter(olddata, convert);

		StringToNominal convert2 = new StringToNominal();
		optionc = new String[2];
		optionc[0] = "-R";
		optionc[1] = "2, 3, 4"; // range of variables to make numeric

		convert2.setOptions(optionc);
		convert2.setInputFormat(data);

		Remove remove = new Remove();
		String[] options0 = weka.core.Utils.splitOptions("-R 4");
		remove.setOptions(options0);
		remove.setInputFormat(data);

		Instances data2 = Filter.useFilter(data, convert2);

		data2.setClassIndex(data2.numAttributes() - classIndex_minus);

		InputMappedClassifier toUse = new InputMappedClassifier();
		toUse.setSuppressMappingReport(true); 
		String[] mappedOptions = weka.core.Utils.splitOptions("-I -trim");
		toUse.setClassifier(classification);
		toUse.setOptions(mappedOptions);
		
		toUse.buildClassifier(data2);

		try {

			for (int i = 1; i < data2.numInstances(); i++) {
				Instance ins = data2.instance(i);
				Instance newIns = toUse.constructMappedInstance(ins);
				
				double classify = classification.classifyInstance(newIns);
				ins.setClassValue(classify);

			}
		} catch (java.lang.ArrayIndexOutOfBoundsException e) {
			e.printStackTrace();
		}

		CSVSaver saver = new CSVSaver();
		saver.setInstances(data2);
		saver.setFile(new File(Out_path));
		saver.writeBatch();

	}

	public RandomForest unsupermeasure(String input, int classIndex_minus) throws Exception {

		String path = System.getProperty("user.dir");

		DataSource source = new DataSource(input);
		Instances olddata = source.getDataSet();
		if (olddata.classIndex() == -1)
			olddata.setClassIndex(olddata.numAttributes() - classIndex_minus);

		NumericToNominal convert = new NumericToNominal();
		String[] optionc = new String[2];
		optionc[0] = "-R";
		optionc[1] = "1, last"; // range of variables to make numeric

		convert.setOptions(optionc);
		convert.setInputFormat(olddata);

		Instances data = Filter.useFilter(olddata, convert);

		StringToNominal convert2 = new StringToNominal();
		optionc = new String[2];
		optionc[0] = "-R";
		optionc[1] = "2, 3, 4"; // range of variables to make numeric

		convert2.setOptions(optionc);
		convert2.setInputFormat(data);

		Remove remove = new Remove();
		String[] options0 = weka.core.Utils.splitOptions("-R 4");
		remove.setOptions(options0);
		remove.setInputFormat(data);

		Instances data2 = Filter.useFilter(data, convert2);

		data2.setClassIndex(data2.numAttributes() - classIndex_minus);
		RandomForest classifier = new RandomForest();
		classifier.buildClassifier(data2);

		Evaluation eval = new Evaluation(data2);
		eval.evaluateModel(classifier, data2);

		String cutString = eval.toClassDetailsString();
		double[][] matrix = eval.confusionMatrix();
		for (int i = 0; i < matrix.length; i++) {
			for (int j = 0; j < matrix[0].length; j++) {
				System.out.print(matrix[i][j] + "\t");
			}
			System.out.println();
		}
		System.out.println(cutString);
		return classifier;
	}

	public void unsupercluster(String input, String output) throws Exception {

		RandomForest forest = unsupermeasure(input, 1);
		classificationCSV(forest, "C:\\Users\\SB_MrBoo\\PycharmProjects\\Python_3_5_64\\last_test.csv", "test1.csv",
				1);

		RandomForest forest2 = unsupermeasure(input, 2);
		classificationCSV(forest2, "C:\\Users\\SB_MrBoo\\PycharmProjects\\Python_3_5_64\\last_test.csv", "test3.csv",
				2);

	}

	public void run() {
		try {
			unsupercluster("C:\\Users\\SB_MrBoo\\PycharmProjects\\Python_3_5_64\\last_train.csv", "test.csv");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}