# Hopfield4py

With this package it is possible to run the Hopfield model.

For more information about the model see: [The Hopfield Network](https://towardsdatascience.com/the-hopfield-network-67267d0569d2) or [Wikipedia](https://en.wikipedia.org/wiki/Hopfield_network)

## Hopfield_Diluted

## Install 
```
pip install hopfield4py
```

# Run

```python
import tensorflow as tf
from hopfield4py import Hopfield

data = tf.convert_to_tensor([[1,1,1,1,1,1],[1,-1,-1,1,1,1]])
model = Hopfield(6)
model.load(data)
corrupted = tf.convert_to_tensor([1,-1,-1,1,1,1], dtype=tf.double)
reconstructed = model.reconstruct(corrupted)
```

# Documentation

The documentation is available at [https://hopfield4py.readthedocs.io](https://hopfield4py.readthedocs.io/en/latest/)

# LICENSE

See [LICENSE](LICENSE)