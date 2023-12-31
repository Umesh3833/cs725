# -*- coding: utf-8 -*-
"""nn_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f-FpfvbLzKZNARaWTJH39OfqLptyCQ7j
"""

import sys
import os
import numpy as np
import pandas as pd

# The seed will be fixed to 42 for this assigmnet.
np.random.seed(42)
NUM_FEATS = 90
NUM_CLASSES = 4
DATA_PATH = '22M1078/classification/data/'

class Net(object):
	'''
	'''

	def __init__(self, num_layers, num_units):
		'''
		Initialize the neural network.
		Create weights and biases.

		Here, we have provided an example structure for the weights and biases.
		It is a list of weight and bias matrices, in which, the
		dimensions of weights and biases are (assuming 1 input layer, 2 hidden layers, and 1 output layer):
		weights: [(NUM_FEATS, num_units), (num_units, num_units), (num_units, num_units), (num_units, 1)]
		biases: [(num_units, 1), (num_units, 1), (num_units, 1), (num_units, 1)]

		Please note that this is just an example.
		You are free to modify or entirely ignore this initialization as per your need.
		Also you can add more state-tracking variables that might be useful to compute
		the gradients efficiently.


		Parameters
		----------
			num_layers : Number of HIDDEN layers.
			num_units : Number of units in each Hidden layer.
		'''
		self.num_layers = num_layers
		self.num_units = num_units

		self.biases = []
		self.weights = []
		for i in range(num_layers):

			if i==0:
				# Input layer
				self.weights.append(np.random.uniform(-0.3, 0.3, size = (NUM_FEATS, self.num_units)))
			else:
				# Hidden layer
				self.weights.append(np.random.uniform(-0.3, 0.3, size = (self.num_units, self.num_units)))

			self.biases.append(np.random.uniform(0.0001, 1, size=(self.num_units, 1)))

		# Output layer
		self.biases.append(np.random.uniform(0, 5, size=(NUM_CLASSES, 1)))
		self.weights.append(np.random.uniform(-0.3, 0.3, size =(self.num_units, NUM_CLASSES)))

	def __call__(self, X):
		'''
		Forward propagate the input X through the network,
		and return the output.

		Note that for a classification task, the output layer should
		be a softmax layer. So perform the computations accordingly

		Parameters
		----------
			X : Input to the network, numpy array of shape m x d
		Returns
		----------
			y : Output of the network, numpy array of shape m x 1
		'''
		y, z, a = self.forward_pass(X)
		return y
		

	def forward_pass(self, X):
		'''
		Forward propagate the input X through the network,
		and return the output.

		Parameters
		----------
			X : Input to the network, numpy array of shape m x d
		Returns
		----------
			y : numpy array of predictions of shape m x 1 
			Z : list of hidden layers layers
			A : list of layers after applying activation function on each Z 
		'''
		W = self.weights
		B = []
		#batch size
		m = X.shape[0]
		#Activation layers
		A_Layers = []
		#Hidden Layers
		Z_Layers = []
		for b in self.biases:
				B.append(b.transpose())
		y_pred = []
		for features in X:
				Z = []
				A = []
				current_layer = features
				for i in range(self.num_layers + 1):
						wx = np.dot(current_layer, W[i])
						temp = np.add(wx, B[i])
						Z.append(temp[0])
						#RELU Activation using np.maximum
						current_layer = np.maximum(temp, 0)
						#Softmax for output
						if i == self.num_layers:
							current_layer = self.softmax(current_layer[0])
							#print('current_layer softmaxed')
							#print(current_layer)
						A.append(current_layer[0])

				y_pred.append(current_layer)
				A_Layers.append(A)
				Z_Layers.append(Z)
		
		preds = np.array(y_pred)
		return preds, Z_Layers, A_Layers

	def reluDerivative(self, x):
		x [x <= 0] = 0
		x [x > 0] = 1
		return x

	def softmax(self, arr):
		shift = arr - np.max(arr)
		exps = np.exp(shift)
		return exps / np.sum(exps)
	
	def softmaxDerivative(self, softmax):
		#A square matrix with diagonals as 1 and non diagonals as 0
		skeleton = np.eye(softmax.shape[-1])
		m = softmax.shape[0] #Batch size
		n = softmax.shape[1] #Softmax row classes
		#Declaring 2 temporary multidimensional matrices 
		# m * n * n will have m jacobian matrices each of which is a n * n matrix
		tmp1 = np.zeros((m, n, n),dtype=np.float32)
		tmp2 = np.zeros((m, n, n),dtype=np.float32)
		#Perform einstein summation
		tmp1 = np.einsum('ij,jk->ijk',softmax, skeleton)
		tmp2 = np.einsum('ij,ik->ijk',softmax, softmax)
		#Overall result for Jacobian matrices
		res = tmp1 - tmp2
		#Mean for all samples in a batch to get a 4 * 4 Jacobian
		res = np.mean(res, axis = 0)
		return res
		
	def backward(self, X, y, lamda):
		'''
		Compute and return gradients loss with respect to weights and biases.
		(dL/dW and dL/db)

		Parameters
		----------
			X : Input to the network, numpy array of shape m x d
			y : Output of the network, numpy array of shape m x 1
			lamda : Regularization parameter.

		Returns
		----------
			del_W : derivative of loss w.r.t. all weight values (a list of matrices).
			del_b : derivative of loss w.r.t. all bias values (a list of vectors).

		Hint: You need to do a forward pass before performing backward pass.
		'''
		del_W = []
		del_B = []
		W = self.weights
		B = []
		m = X.shape[0]
		for b in self.biases:
				B.append(b.transpose())
		
		#Forward pass to be performed before backward pass
		o, Z_Layers, A_Layers = self.forward_pass(X)
		y = y.reshape(o.shape)
		#dA is derivative of loss function wrt final output (softmax vctor - one hot vector true label)
		dA = o - y
		#softmax derivative to be considered
		dA = np.dot(dA, self.softmaxDerivative(o)) 
		
		#Preprocess Z_layers and A_Layers required for back propogation
		z_batch = []
		a_batch = []
		for i in range(self.num_layers + 1):
			z = []
			a = []
			for j in range(m):
				z.append(Z_Layers[j][i])
				a.append(A_Layers[j][i])
			z_batch.append(z)
			a_batch.append(a)

		#Back propogation algorithm 
		for i in range(self.num_layers + 1):
			z = np.array(z_batch[-(i+1)])
			if (i == self.num_layers):
				 a_prev = X
			else:
				a_prev = np.array(a_batch[-(i + 2)])
			dZ = dA * self.reluDerivative(z)
			dW = 1./m * np.dot(a_prev.T, dZ)
			dB = 1./m * np.sum(dZ, axis = 0)
			dA = np.dot(dZ, W[-(i+1)].T)
			del_W.append(dW)
			del_B.append(dB)
		return del_W, del_B

class Optimizer(object):
	'''
	'''

	def __init__(self, learning_rate):
		'''
		Create a Gradient Descent based optimizer with given
		learning rate.

		Other parameters can also be passed to create different types of
		optimizers.

		Hint: You can use the class members to track various states of the
		optimizer.
		'''
		self.learning_rate = learning_rate

	def step(self, weights, biases, delta_weights, delta_biases):
		'''
		Parameters
		----------
			weights: Current weights of the network.
			biases: Current biases of the network.
			delta_weights: Gradients of weights with respect to loss.
			delta_biases: Gradients of biases with respect to loss.
		'''
		l = len(weights)
		lr = self.learning_rate
		for i in range(l):
			weights[i] = np.add(weights[i], -1 * lr * delta_weights[l - 1 - i])
			d = delta_biases[l - 1 - i].reshape(biases[i].shape)
			biases[i] = np.add(biases[i], -1 * lr * d)

		return weights, biases

def loss_mse(y, y_hat):
	'''
	Compute Mean Squared Error (MSE) loss betwee ground-truth and predicted values.

	Parameters
	----------
		y : targets, numpy array of shape m x 1
		y_hat : predictions, numpy array of shape m x 1

	Returns
	----------
		MSE loss between y and y_hat.
	'''
	return ((y - y_hat)**2).mean()

def loss_regularization(weights, biases):
	'''
	Compute l2 regularization loss.

	Parameters
	----------
		weights and biases of the network.

	Returns
	----------
		l2 regularization loss 
	'''
	reg_loss = 0
	for W in weights:
		reg_loss = reg_loss + np.sum(np.square(W))
	for B in biases:
		reg_loss = reg_loss + np.sum(np.square(B))
	return reg_loss

def loss_fn(y, y_hat, weights, biases, lamda):
	'''
	Compute loss =  loss_mse(..) + lamda * loss_regularization(..)

	Parameters
	----------
		y : targets, numpy array of shape m x 1
		y_hat : predictions, numpy array of shape m x 1
		weights and biases of the network
		lamda: Regularization parameter

	Returns
	----------
		l2 regularization loss 
	'''
	return loss_mse(y, y_hat) + lamda * loss_regularization(weights, biases)

def rmse(y, y_hat):

	

	'''
	Compute Root Mean Squared Error (RMSE) loss betwee ground-truth and predicted values.

	Parameters
	----------
		y : targets, numpy array of shape m x 1
		y_hat : predictions, numpy array of shape m x 1
	


	Returns
	----------
		RMSE between y and y_hat.
	'''
	return np.sqrt(((y - y_hat) ** 2).mean())

def cross_entropy_loss(y, y_hat):
	'''
	Compute cross entropy loss

	Parameters
	----------
		y : targets, numpy array of shape m x 1
		y_hat : predictions, numpy array of shape m x 1

	Returns
	----------
		cross entropy loss
	'''
	loss = -np.sum(y*np.log(y_hat))
	#For normalization
	m = y_hat.shape[0]
	loss = loss / m
	#Divide by NUM of classes for avg per class
	return loss/ NUM_CLASSES

def is_strictly_degrading(arr, delta):
  for i in range(len(arr) - 1):
    diff = arr[i] - arr[i + 1] 
    if diff > delta:
      return False
  return True

def train(
	net, optimizer, lamda, batch_size, max_epochs,
	train_input, train_target,
	dev_input, dev_target, patience, min_delta
):
	'''
	In this function, you will perform following steps:
		1. Run gradient descent algorithm for `max_epochs` epochs.
		2. For each bach of the training data
			1.1 Compute gradients
			1.2 Update weights and biases using step() of optimizer.
		3. Compute RMSE on dev data after running `max_epochs` epochs.

	Here we have added the code to loop over batches and perform backward pass
	for each batch in the loop.
	For this code also, you are free to heavily modify it.
	'''

	m = train_input.shape[0]
	past_dev_loss = []
	#For Early Stopping
	min_dev_loss = 99999999
	for e in range(max_epochs):
		epoch_loss = 0.0
		bn = 1
		for i in range(0, m, batch_size):
			batch_input = train_input[i:i+batch_size]
			batch_target = train_target[i:i+batch_size]
			pred = net(batch_input)

			# Compute gradients of loss w.r.t. weights and biases
			dW, db = net.backward(batch_input, batch_target, lamda)

			# Get updated weights based on current weights and gradients
			weights_updated, biases_updated = optimizer.step(net.weights, net.biases, dW, db)

			# Update model's weights and biases
			net.weights = weights_updated
			net.biases = biases_updated

			# Compute loss for the batch
			batch_loss = cross_entropy_loss(batch_target, pred)
			#Normalize per sample
			batch_loss = batch_loss/batch_size
			
			epoch_loss += batch_loss

		dev_pred = net(dev_input)
		dev_loss = cross_entropy_loss(dev_target, dev_pred)
		#dev_fscore = get_micro_fscore(dev_target, dev_pred)
		print("Epoch", "Train_Loss", "Dev_Loss",)
		print(e+1, '{:.4f}'.format(epoch_loss), '{:.4f}'.format(dev_loss))
		print()
		# Writing early stopping conditions (Part 2)
		if (e < patience):
			past_dev_loss.append(dev_loss)
		else:
			past_dev_loss.pop(0)
			past_dev_loss.append(dev_loss)
		
		diff = dev_loss - min_dev_loss
		if diff < min_delta:
				#This is an improvement
				min_dev_loss = dev_loss

		if len(past_dev_loss) == patience:
			if is_strictly_degrading(past_dev_loss, min_delta):
				print("Early Stopping Now")
				break
		print()

	# After running `max_epochs` (for Part 1) epochs OR early stopping (for Part 2), compute the RMSE on dev data.
	dev_pred = net(dev_input)
	dev_loss = cross_entropy_loss(dev_target, dev_pred)
	print('Loss on dev data: {:.5f}'.format(dev_loss))

def get_test_data_predictions(net, inputs):
	'''
	Perform forward pass on test data and get the final predictions that can
	be submitted on Kaggle.
	Write the final predictions to the part2.csv file.

	Parameters
	----------
		net : trained neural network
		inputs : test input, numpy array of shape m x d

	Returns
	----------
		predictions (optional): Predictions obtained from forward pass
								on test data, numpy array of shape m x 1
	'''
	return net(inputs)

def feature_scaling(df):
  '''
  Perform feature scaling for values in the dataframe for columns 2 to 91
  '''
  #print(df.head())
  df = df.loc[: , '2':'91']
  min = df.iloc[:,:].min()
  max = df.iloc[:,:].max()
  df.iloc[:,:] = (df.iloc[:,:] - min) / (max - min)
  #print(df.head())
  return df.to_numpy()

def encode_targets(arr):
  encodedlist= []
  for x in arr:
    label = x
    #print(label)
    category = 1
    if (label == 'Very Old'):
      category = [1, 0, 0, 0]
    if (label == 'Old'):
      category = [0, 1, 0, 0]
    if (label == 'New'):
      category = [0, 0, 1, 0]
    if (label == 'Recent'):
      category = [0, 0, 0, 1]
    encodedlist.append(category)
  encodedarray = np.array(encodedlist)
  return encodedarray

def decode_targets(arr):
  decodedlist= []
  for vector in arr:
    x = np.argmax(vector)
    if (x == 0):
      category = 'Very Old'
    if (x == 1):
      category = 'Old'
    if (x == 2):
      category = 'New'
    if (x == 3):
      category = 'Recent'
    decodedlist.append(category)
  decodedarray = np.array(decodedlist)
  return decodedarray

def read_data():
	'''
	Read the train, dev, and test datasets
	'''
	df_train = pd.read_csv(DATA_PATH + 'train.csv')
	df_dev = pd.read_csv(DATA_PATH + 'dev.csv')
	df_test = pd.read_csv(DATA_PATH + 'test.csv')
	train_input = feature_scaling(df_train)
	dev_input = feature_scaling(df_dev)
	test_input = feature_scaling(df_test)
	train_target = df_train.loc[: , '1'].to_numpy()
	m = train_target.shape[0]
	train_target = encode_targets(train_target)
	train_target = train_target.reshape(m, NUM_CLASSES)
	dev_target = df_dev.loc[: , '1'].to_numpy()
	m = dev_target.shape[0]
	dev_target = encode_targets(dev_target)
	dev_target = dev_target.reshape(m, NUM_CLASSES)
	return train_input, train_target, dev_input, dev_target, test_input

def main():

	# Hyper-parameters 
	max_epochs = 200
	batch_size = 64
	learning_rate = 0.25
	num_layers = 4
	num_units = 64
	lamda = 0.001 # Regularization Parameter
	patience = 4
	min_delta = 0.0001

	train_input, train_target, dev_input, dev_target, test_input = read_data()
	net = Net(num_layers, num_units)
	#optimizer = Optimizer(learning_rate, beta1, beta2, epsilon, num_units, num_layers)
	optimizer = Optimizer(learning_rate)
	train(
		net, optimizer, lamda, batch_size, max_epochs,
		train_input, train_target,
		dev_input, dev_target, patience, min_delta
	)
	#Only for Part 2
	test_pred = get_test_data_predictions(net, test_input)
	test_pred_classes = decode_targets(test_pred)
	print(list(test_pred_classes))
	np.savetxt('preds.csv', test_pred_classes, fmt='"%s"')

if __name__ == "__main__":
  main()

