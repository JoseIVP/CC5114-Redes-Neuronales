# Ejercicio 2

Este ejercicio consiste en implementar un perceptrón que aprenda qué colores
deben tener los puntos que se encuentran bajo una recta (puntos azules) y los
que se encuentran por sobre la recta (puntos rojos), sin que el perceptrón sepa
explícitamente cual es la recta. Al perceptrón solamente se le da la información
del color para algunos puntos y luego se le pide que identifique la clase de
los puntos para un conjunto del que no sabe sus colores.

El algoritmo utilizado para entrenar al perceptrón es:

    diff= desiredOutput - realOutput
    learningRate= 0.1
    for all N in perceptron parameters:
        weightN= weightN + (learningRate * inputN * diff)
    bias= bias + (learningRate * diff)
    
Los pesos y bias son seleccionados incialmente de forma aleatoria con valores
en el rango -2.0 a 2.0.