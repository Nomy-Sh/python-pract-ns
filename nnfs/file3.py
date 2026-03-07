# Artificial neural network |  | ep3-1 sentdex nnfs
# 1 layer, L, execution of a neural network
# layer L, has 3 neurons/ nodes

inputs = [1.0, 2.0, 3.0, 2.5] # input layer 
# layer-0, L0, is not considered as one of the functional layer in ANN, since its the features inputs provided externally
# in this examle this could be the inputs from previous layer L-1

weights = [
            [0.2, 0.8, -0.5, 1.0], # weights of individual node # node1 # => each node of L is connected to all nodes of L-1, weights of 4 incoming synapses/ edges/ neurons/nodes
            [0.5, -0.91, 0.26, -0.5], # node2 # => weights of node2 # node2 of L is connected to all nodes of L-1 #
            [-0.26, -0.27, 0.17, 0.87] # node3
         ]

biases = [2.0, # bias of node 1
         3.0,  # bias of node 2
         0.5]  # bias of node 3

layer_output = []
# Layer L execution
for neuron_weights, neuron_bias in zip(weights, biases):
   neuron_output = 0
   # execution of each node # saving the outputs of each node which will each be a scalar value
   for n_input, weight in zip(inputs, neuron_weights):
      neuron_output += n_input * weight
   neuron_output += neuron_bias
   layer_output.append(neuron_output)

print(layer_output)

