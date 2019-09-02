import numpy as np

class Neuron:

	def __init__(self, weights, bias, actFunc, learningRate=0.1):
		self.weights = weights
		self.bias = bias
		self.actFunc = actFunc()
		self.lr = learningRate
		self.cache = None # Memoria para recordar output de la neurona
		self.delta = None
		self.inputCache = None


	def feed(self, inputs):
		if len(inputs) != len(self.weights):
			print(len(inputs))
			print(len(self.weights))
			raise Exception('Cantidad de inputs de la neurona no coincide con la cantidad de pesos.')

		XW = 0
		for x, w in zip(inputs, self.weights):
			if type(x) not in [int, float, np.float64, np.int32]:
				raise Exception('El input de la neurona debe ser numérico.')
			XW += x * w

		self.inputCache = inputs
		self.cache = self.actFunc.apply(XW + self.bias) 
		return self.cache


	def getCache(self):
		return self.cache


	def setDelta(self, error):
		self.delta = error * self.actFunc.derivative(self.cache)


	def getWeight(self, index):
		return self.weights[index]


	def update(self):
		for i in range(len(self.weights)):
			self.weights[i] = self.weights[i] + (self.lr * self.delta * self.inputCache[i])

		self.bias += self.lr * self.delta
		self.delta = None
		self.cache = None
		self.inputCache = None