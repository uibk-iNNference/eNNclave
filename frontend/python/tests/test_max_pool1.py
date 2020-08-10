from tensorflow.python.framework.test_util import TensorFlowTestCase
from tensorflow.keras.models import Sequential
import tensorflow.keras.layers as layers

import os
import unittest

from common import common_test_basis


class MaxPool1D(TensorFlowTestCase):
    def testSmallNative(self):
        model = Sequential([
            layers.MaxPool1D(pool_size=3, input_shape=(5, 3))
        ])
        common_test_basis(model, False)

    def testMediumNative(self):
        model = Sequential([
            layers.MaxPool1D(pool_size=3, input_shape=(50, 3))
        ])
        common_test_basis(model, False)

    def testLargeNative(self):
        model = Sequential([
            layers.MaxPool1D(pool_size=5, input_shape=(500, 10))
        ])
        common_test_basis(model, False)

    def testHugeNative(self):
        model = Sequential([
            layers.MaxPool1D(pool_size=64, input_shape=(1000, 1000))
        ])
        common_test_basis(model, False)
    
    @unittest.skipIf(os.environ.get('SGX_SDK') is None, "SGX is not available")
    def testSmallEnclave(self):
        model = Sequential([
            layers.MaxPool1D(pool_size=3, input_shape=(5, 3))
        ])
        common_test_basis(model, True)

    @unittest.skipIf(os.environ.get('SGX_SDK') is None, "SGX is not available")
    def testMediumEnclave(self):
        model = Sequential([
            layers.MaxPool1D(pool_size=3, input_shape=(50, 3))
        ])
        common_test_basis(model, True)

    @unittest.skipIf(os.environ.get('SGX_SDK') is None, "SGX is not available")
    def testLargeEnclave(self):
        model = Sequential([
            layers.MaxPool1D(pool_size=5, input_shape=(500, 10))
        ])
        common_test_basis(model, True)

    @unittest.skip
    @unittest.skipIf(os.environ.get('SGX_SDK') is None, "SGX is not available")
    def testHugeEnclave(self):
        model = Sequential([
            layers.MaxPool1D(pool_size=64, input_shape=(1000, 1000))
        ])
        common_test_basis(model, True)

if __name__ == "__main__":
    unittest.main()