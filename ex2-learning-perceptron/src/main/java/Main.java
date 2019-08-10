import java.util.Random;
import java.awt.Color;
import javax.swing.JFrame;
import de.erichseifert.gral.data.DataTable;
import de.erichseifert.gral.plots.XYPlot;
import de.erichseifert.gral.plots.lines.DefaultLineRenderer2D;
import de.erichseifert.gral.plots.lines.LineRenderer;
import de.erichseifert.gral.ui.InteractivePanel;

public class Main {

    static double lineFunction(double x){
        return 5 * x + 3;
    }

    public static void main(String[] args) {
        Random random= new Random(42);
        // Obtenemos weightX, weightY y bias entre -2 y 2.
        double wX= random.nextDouble() * 4 - 2;
        double wY= random.nextDouble() * 4 - 2;
        double bias= random.nextDouble() * 4 - 2;
        Perceptron perceptron= new Perceptron(wX, wY, bias, 0.1);
        int trainingPoints= 100;
        DataTable tRedPoints= new DataTable(Double.class, Double.class);
        DataTable tBluePoints= new DataTable(Double.class, Double.class);
        double maxX= 5; double minX= -5;
        double maxY= lineFunction(5);
        double minY= lineFunction(-5);
        // Generamos los puntos para el entrenamiento y entrenamos:
        // Azul => true, rojo => false.
        for(int i= 0; i < trainingPoints; i++){
            double randX= random.nextDouble() * (maxX - minX) + minX;
            double randY= random.nextDouble() * (maxY - minY) + minY;
            if(randY < lineFunction(randX)){
                // Azul por debajo de la linea
                tBluePoints.add(randX, randY);
                perceptron.train(randX, randY, true);
            }else{
                tRedPoints.add(randX, randY); // Rojo sobre o en la linea
                perceptron.train(randX, randY, false);
            }
        }

        DataTable linePoints= new DataTable(Double.class, Double.class);
        // Generamos los puntos de la linea:
        int lPoints = 10; // Numero de puntos para la linea
        for(int i= 0; i<= lPoints; i++){
            double x = (maxX - minX) / lPoints * i + minX;
            double y = lineFunction(x);
            linePoints.add(x, y);
        }

        // Testeamos el perceptron:
        int testingPoints= 1000;
        DataTable outputRedPoints= new DataTable(Double.class, Double.class);
        DataTable outputBluePoints= new DataTable(Double.class, Double.class);
        for(int i= 0; i < testingPoints; i++){
            double randX= random.nextDouble() * (maxX - minX) + minX;
            double randY= random.nextDouble() * (maxY - minY) + minY;
            boolean isBlue= perceptron.feed(randX, randY);
            if(isBlue) outputBluePoints.add(randX, randY);
            else outputRedPoints.add(randX, randY);
        }

        // Graficamos utilizando la libreria GRAL http://trac.erichseifert.de/gral/
        JFrame frame= new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 400);
        XYPlot plot = new XYPlot(tRedPoints, tBluePoints, linePoints, outputRedPoints, outputBluePoints);
        frame.getContentPane().add(new InteractivePanel(plot));
        LineRenderer lines = new DefaultLineRenderer2D();
        plot.setLineRenderers(linePoints, lines);
        // Colores de entrenamiento:
        Color tBlueClr= new Color(0, 0, 255);
        Color tRedClr= new Color(255, 0, 0);
        // Colores de testing:
        Color outBluClr= new Color(48, 116, 255);
        Color outRedClr= new Color(255, 98, 111);
        plot.getPointRenderers(tBluePoints).get(0).setColor(tBlueClr);
        plot.getPointRenderers(tRedPoints).get(0).setColor(tRedClr);
        plot.getPointRenderers(outputBluePoints).get(0).setColor(outBluClr);
        plot.getPointRenderers(outputRedPoints).get(0).setColor(outRedClr);
        frame.setVisible(true);
    }
}
