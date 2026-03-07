# Artificial neural network |  | ep4 sentdex nnfs
import numpy as np

inputs = [[1.0, 2.0, 3.0, 2.5],
          [2.0, 5.0, -1.0, 2.0],
          [-1.5, 2.7, 3.3, -0.8]
         ]
weights = [
            [0.2, 0.8, -0.5, 1.0],
            [0.5, -0.91, 0.26, -0.5],
            [-0.26, -0.27, 0.17, 0.87]
          ]

biases = [2.0, 3.0, 0.5]


output = np.dot(inputs, np.array(weights).T) + biases
print(output)

#print(np.shape(inputs))

# 3x4 . 3x4 # transpose is needed for dot mul 
# 3x4 . 4x3 # T(3x4) => 4x3 # output shape is 3x3