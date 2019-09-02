import numpy as np
from NeuralNetwork import NeuralNetwork
from functions import Step, Tanh, Sigmoid, mse
import matplotlib.pyplot as plt


def hotEncoding(flower_type):
	enc = {'Iris-setosa': 0,
		'Iris-versicolor': 1,
		'Iris-virginica': 2}
	return enc[flower_type]


def normalizeData(data):
	dataMax = np.max(data, axis=0)
	dataMin = np.min(data, axis=0)
	return (data - dataMin) / (dataMax - dataMin)

 
def confusionMatrix(real, predicted, numberOfClasses):
	matrix = np.zeros((numberOfClasses, numberOfClasses), dtype=int)
	for r, p in zip(real.astype(int), predicted.astype(int)):
		matrix[r, p] += 1
	return matrix 


def testNetwork(network, testData):
	classes = testData[:, -1]
	features = testData[:, 0:-1]
	realOutput = []
	for inputs in features:
		output = network.feed(inputs)
		realOutput.append(np.argmax(output))

	realOutput = np.array(realOutput)
	mseResult = mse(realOutput, classes)
	hits = (realOutput == classes).mean()
	return mseResult, hits, realOutput


def trainNetwork(network, trainingData, numberOfClasses, batchSize=35, epochs=10, seed=42, ):
	print('Entrenando...')
	np.random.seed(seed)
	mseList = []
	hitList = []
	for e in range(1, epochs+1):
		np.random.shuffle(trainingData)
		for start in range(0, len(trainingData), batchSize):
			batch = trainingData[start:start+batchSize, :]
			classes = batch[:, -1]
			features = batch[:, 0:-1]
			for inputs, clss in zip(features, classes.astype(int)):
				expected = [0 for _ in range(numberOfClasses)]
				expected[clss] = 1
				network.train(inputs, expected)
		mseResult, hits, _ = testNetwork(network, trainingData)
		mseList.append(mseResult)
		hitList.append(hits * 100)
		print('Época: %d\tMSE: %.4f\tAcierto (%%): %.4f' % (e, mseResult, hits * 100))
		#print('Época:', e, '\tMSE:', mseResult, '\tAcierto (%):', hits * 100)
	return mseList, hitList



# Se cargan los datos.
data = np.loadtxt('data/iris.data', delimiter=',', converters={4: hotEncoding}, encoding='utf-8')

# Se revuelven los datos.
np.random.seed(3)
np.random.shuffle(data)
data = np.append(normalizeData(data[:, 0:-1]), np.reshape(data[:, -1], (len(data), 1)), axis=1)
# Separamos en datos para entrenamiento (70%) y datos para test (30%).
trainingData = data[0:105, :]
testData = data[105:-1, :]

# Se crea y entrena la red neuronal.
nn = NeuralNetwork(3, [6, 4, 3], [Tanh, Tanh, Sigmoid], 4, 3, Sigmoid, seed=3)
mseList, hitList = trainNetwork(nn, trainingData, 3)
realClss = testData[:, -1]
mseResult, hits, predictedClss = testNetwork(nn, testData)
print('\nPruebas con datos de testig:')
print('MSE:', mseResult, '\tAcierto (%):', hits * 100)
matrix = confusionMatrix(realClss, predictedClss, 3)
print('\nMatriz de confusión: (Eje x: predicción, Eje y: real)')
print('    0  1  2')
for f in range(3): print(f, matrix[f])

# Plot MSE y Porcentaje de acierto.
x = np.arange(1, 11)
_, msePlot = plt.subplots()
msePlot.plot(x, mseList)
msePlot.set(xlabel='Época', ylabel='MSE', title='MSE por época')
msePlot.grid()

_, hitRatePlot = plt.subplots()
hitRatePlot.plot(x, hitList)
hitRatePlot.set(xlabel='Época', ylabel='Porcentaje de acierto', title='Porcentaje de acierto por época')
hitRatePlot.grid()
plt.show()
