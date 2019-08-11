public class Perceptron {

    private double weightX, weightY, bias;
    private double learningRate;

    public Perceptron(double weightX, double weightY, double bias, double learningRate){
        this.weightX= weightX;
        this.weightY= weightY;
        this.bias= bias;
        this.learningRate= learningRate;
    }

    public void train(double x, double y, boolean expected){
        boolean realOutput= this.feed(x, y);
        double diff= (expected? 1: 0) - (realOutput? 1: 0);
        // Para todos los componentes del perceptron recomputamos el peso como:
        // pesoComponenteN = pesoComponenteN + ( TazaDeAprendizaje * inputN * diff)
        // siendo diff la diferencia entre el output esperado y el output real.
        weightX= weightX + (learningRate * x * diff);
        weightY= weightY + (learningRate * y * diff);
        bias= bias + (learningRate * diff);
    }

    public boolean feed(double x, double y){
        return (x * weightX + y * weightY + bias) >= 0;
    }
}
