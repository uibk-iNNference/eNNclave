# coding: utf-8
import tensorflow as tf
from enclave_layer import EnclaveLayer
import numpy as np

tf.compat.v1.enable_eager_execution()

test_layer = EnclaveLayer(10)
arr = np.arange(9216).reshape((-1, 9216))

print('\n\n\n\n')
print(test_layer(arr))