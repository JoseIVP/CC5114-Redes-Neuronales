import org.junit.Test;
import static org.junit.Assert.*;

public class TestPerceptron {

    @Test
    public void AndTest(){
        IPerceptron and= new AndPerceptron();
        assertEquals(false, and.feed(false, false));
        assertEquals(false, and.feed(false, true));
        assertEquals(false, and.feed(true, false));
        assertEquals(true, and.feed(true, true));
    }

    @Test
    public void OrTest(){
        IPerceptron or= new OrPerceptron();
        assertEquals(false, or.feed(false, false));
        assertEquals( true, or.feed(false, true));
        assertEquals(true, or.feed(true, false));
        assertEquals(true, or.feed(true, true));
    }

    @Test
    public void NandTest(){
        IPerceptron nand= new NandPerceptron();
        assertEquals(true, nand.feed(false, false));
        assertEquals(true, nand.feed(false, true));
        assertEquals(true, nand.feed(true, false));
        assertEquals(false, nand.feed(true, true));
    }

    @Test
    public void SumGateTest(){
        SumGate gate= new SumGate();
        boolean[][] input= {{false, false},
                {false, true},
                {true, false},
                {true, true}};
        boolean[][] expectedOut= {{false, false},
                {true, false},
                {true, false},
                {false, true}};
        for(int i= 0; i< 4; i++){
            SumGate.SumResult result= gate.feed(input[i][0], input[i][1]);
            assertEquals(expectedOut[i][0], result.getSum());
            assertEquals(expectedOut[i][1], result.getCarry());
        }
    }

}
