from tensorflow.python.framework.test_util import TensorFlowTestCase
from tensorflow.keras.models import Sequential
import tensorflow.keras.layers as layers

import os
import unittest

from common import common_test_basis


class DenseTests(TensorFlowTestCase):
    @staticmethod
    def testSmallNative():
        model = Sequential([
            layers.Dense(5, input_shape=(1, 5))
        ])
        common_test_basis(model, False)

    @staticmethod
    def testMediumNative():
        model = Sequential([
            layers.Dense(10, input_shape=(1, 10))
        ])
        common_test_basis(model, False)

    @staticmethod
    def testLargeNative():
        model = Sequential([
            layers.Dense(100, input_shape=(1, 100))
        ])
        common_test_basis(model, False)

    @unittest.skip
    def testHugeNative(self):
        model = Sequential([
            layers.Dense(1000, input_shape=(1, 1000))
        ])
        common_test_basis(model, False)

    @unittest.skipIf(os.environ.get('SGX_SDK') is None, "SGX is not available")
    def testSmallEnclave(self):
        model = Sequential([
            layers.Dense(5, input_shape=(1, 5))
        ])
        common_test_basis(model, True)

    @unittest.skipIf(os.environ.get('SGX_SDK') is None, "SGX is not available")
    def testMediumEnclave(self):
        model = Sequential([
            layers.Dense(10, input_shape=(1, 10))
        ])
        common_test_basis(model, True)

    @unittest.skipIf(os.environ.get('SGX_SDK') is None, "SGX is not available")
    def testLargeEnclave(self):
        model = Sequential([
            layers.Dense(100, input_shape=(1, 100))
        ])
        common_test_basis(model, True)

    @unittest.skip
    @unittest.skipIf(os.environ.get('SGX_SDK') is None, "SGX is not available")
    def testHugeEnclave(self):
        model = Sequential([
            layers.Dense(1000, input_shape=(1, 1000))
        ])
        common_test_basis(model, True)


if __name__ == "__main__":
    unittest.main()
