public class AbstractPerceptron implements IPerceptron {

    private int weightIn1;
    private int weightIn2;
    private int bias;

    protected AbstractPerceptron(int weightIn1, int weightIn2, int bias){
        this.weightIn1= weightIn1;
        this.weightIn2= weightIn2;
        this.bias= bias;
    }

    @Override
    public boolean feed(boolean in1, boolean in2){
        return ((in1? 1: 0) * weightIn1 + (in2? 1: 0) * weightIn2 + bias) > 0;
    }
}
