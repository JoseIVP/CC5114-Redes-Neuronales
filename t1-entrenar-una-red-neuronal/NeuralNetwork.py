from Neuron import Neuron
from random import Random
import numpy as np

class NeuralNetwork:

	def __init__(self, numberOfLayers, neuronsPerLayer, funPerLayer,  numberOfInputs,
		numberOfOutputs, outputsFunc, learningRate=0.1, weights=None, biases=None, seed=42):

		if numberOfLayers != len(neuronsPerLayer):
			raise Exception('Largo de neuronsPerLayer no coincide con el número de capas de la red.')
		if numberOfLayers != len(funPerLayer):
			raise Exception('Largo de funPerLayer no coincide con el número de capas de la red.')

		if weights is not None and len(weights) != numberOfLayers:
			raise Exception('La cantidad de listas en weights no coincide con la cantidad de capas de la red.')

		rand = Random()
		rand.seed(seed)
		self.layers = []
		layerInputs = numberOfInputs
		for l in range(numberOfLayers):
			layer = []
			for n in range(neuronsPerLayer[l]):
				if weights is not None:
					neuronWeights = weights[l][n]
					if len(neuronWeights) != layerInputs:
						raise Exception('El número de inputs no coincide con los parámetros de la neurona')
				else:
					neuronWeights = [rand.uniform(-2, 2) for _ in range(layerInputs)]
				if biases is not None:
					neuronBias = biases[l][n]
				else:
					neuronBias = rand.uniform(-2, 2)
				layer.append(Neuron(neuronWeights, neuronBias, funPerLayer[l], learningRate))
			layerInputs = len(layer)
			self.layers.append(layer)

		
		self.outputLayer= []
		for _ in range(numberOfOutputs):
			neuronWeights = [rand.uniform(-2, 2) for _ in range(len(self.layers[-1]))]
			self.outputLayer.append(Neuron(neuronWeights, rand.uniform(-2, 2), outputsFunc, learningRate))


	def feed(self, inputs):
		# Se entregan los inputs de un ejemplo.
		for i in inputs:
			if type(i) not in [int, float, np.float64, np.int32]:
				raise Exception('El input de la red debe ser numérico.')
		nextInput = inputs # Input para la próxima capa
		for layer in self.layers:
			layerOutput = []
			for neuron in layer: 
				 neuronOutput = neuron.feed(nextInput)
				 layerOutput.append(neuronOutput)
			nextInput = layerOutput

		output = []
		for neuron in self.outputLayer:
			neuronOutput = neuron.feed(nextInput)
			output.append(neuronOutput)

		return output


	def __transferDerivative(output):
		return output * (1.0 - output)


	def train(self, inputs, expectedOutput):
		realOut = self.feed(inputs)
		for neuron, expected in zip(self.outputLayer, expectedOutput):
			error = expected - neuron.getCache()
			neuron.setDelta(error)

		# Recorremos la red desde la capa de output hasta la de input.
		lastLayer = self.outputLayer
		for layer in reversed(self.layers):
			for i, neuron in enumerate(layer):
				error = 0
				for nextNeuron in lastLayer:
					error += nextNeuron.getWeight(i) * nextNeuron.delta
				neuron.setDelta(error)
			lastLayer = layer

		# Se actualizan los pesos luego de propagar el error.
		for layer in self.layers:
			for neuron in layer:
				neuron.update()

		for neuron in self.outputLayer:
			neuron.update()
