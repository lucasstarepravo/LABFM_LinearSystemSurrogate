import pickle as pk
import torch
import torch.nn as nn


class ANN_topology(nn.Module):
    def __init__(self, input_size, output_size, hidden_layers):
        super(ANN_topology, self).__init__()
        layers = [nn.Linear(input_size, hidden_layers[0])]
        layers += [nn.SiLU()]

        for i in range(1, len(hidden_layers)):
            layers.append(nn.Linear(hidden_layers[i - 1], hidden_layers[i]))
            layers.append(nn.SiLU())

        # Add the final layer
        layers.append(nn.Linear(hidden_layers[-1], output_size))

        # Use ModuleList to hold all the layers
        self.layers = nn.ModuleList(layers)

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def predict(self, x):
        x = self.forward(x)
        return x


def load_attrs(filepath):
    ''' In this case the filepath must contain the complete directory including the file'''

    with open(filepath, 'rb') as f:
        attrs = pk.load(f)
    return attrs


def load_model_instance(filepath, attrs):
    ''' In this case the filepath must contain the complete directory including the file'''
    input_size = attrs['input_size']
    output_size = attrs['output_size']
    hidden_layers = attrs['hidden_layers']
    model_state = torch.load(filepath)

    # In this case it doesn't matter if ANN_topology or PINN_topology is used as they
    model = ANN_topology(input_size, output_size, hidden_layers)
    model.load_state_dict(model_state)
    return model
