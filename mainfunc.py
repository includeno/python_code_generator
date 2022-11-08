import platform
print(platform.platform())

import torch
print(torch.__version__)
print(torch.device("mps"))

import torch
a = torch.rand(3,5)
print(a)
b = torch.device('mps')
print(b)