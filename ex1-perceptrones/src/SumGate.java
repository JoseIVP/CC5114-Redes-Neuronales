public class SumGate {

    public class SumResult{

        private boolean sum, carry;

        protected SumResult(boolean sum, boolean carry){
            this.sum= sum;
            this.carry= carry;
        }

        public boolean getSum() {
            return sum;
        }

        public boolean getCarry() {
            return carry;
        }
    }

    public SumResult feed(boolean in1, boolean in2){
        NandPerceptron p1= new NandPerceptron();
        NandPerceptron p2= new NandPerceptron();
        NandPerceptron p3= new NandPerceptron();
        NandPerceptron p4= new NandPerceptron();
        NandPerceptron p5= new NandPerceptron();
        boolean result1= p1.feed(in1, in2);
        boolean result2= p2.feed(in1, result1);
        boolean result3= p3.feed(result1, in2);
        boolean result4= p4.feed(result2, result3);
        boolean result5= p5.feed(result1, result1);
        return new SumResult(result4, result5);
    }
}