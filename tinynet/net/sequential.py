from .base import Net

from tinynet.core import Backend as np
from tinynet.utilities.logger import output_intermediate_result
from tinynet.layers import MaxPool2D
class Sequential(Net):
    '''
    Sequential model reads a list of layers and stack them to be a neural network.
    '''
    def __init__(self, layers):
        super().__init__(layers)
    
    def forward(self, input):
        output = input
        for layer in self.layers:
            if isinstance(layer, MaxPool2D) and layer.return_index:
                output, max_indices = layer.forward(output)
            else:
                output = layer.forward(output)
            output_intermediate_result(layer.name, output, 'data', layer)
        return output
    
    def backward(self, in_gradient):
        for layer in self.layers[::-1]:
            in_gradient = layer.backward(in_gradient)
            output_intermediate_result(layer.name, in_gradient, 'gradient', layer)
        return in_gradient
    
    def add(self, layer):
        self.layers.append(layer)

    def __call__(self, input):
        return self.forward(input)
    
    def predict(self, data, batch_size=None):
        results = None
        if batch_size:
            for i in range(0, len(data), batch_size):
                result = self.forward(data[i:i+batch_size])
                if results is None:
                    results = result
                else:
                    results = np.concatenate((results, result))
            return results
        else:
            return self.forward(data)