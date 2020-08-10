from tensorflow.keras.models import Sequential
import tensorflow.keras.layers as layers
import numpy as np
import os
from invoke.context import Context

from ennclave import Enclave
import frontend_python as ennclave


def build_library(model: Enclave, mode: str, target_dir="backend/generated"):
    model.generate_state(target_dir)
    model.generate_forward(mode, target_dir)
    context = Context()
    if mode == 'sgx':
        model.generate_config(target_dir)
        context.run('build/backend_sgx_encryptor')

    with context.cd("build"):  # TODO: make more robust
        context.run(f"make backend_{mode}")


def common_test_basis(model: Sequential, use_sgx: bool):
    # TODO: seed with current date (for consistent results within a day)
    rng = np.random.default_rng()

    input_shape = model.input_shape[1:]
    inputs = rng.normal(loc=0., scale=2., size=(
        input_shape)).astype(np.float32)
    inputs = np.expand_dims(inputs, 0)
    size = np.prod(inputs.shape)

    expected_result = model(inputs).numpy().flatten()
    output_size = np.prod(expected_result.shape)

    ennclave_model = Enclave(model.layers)
    build_library(ennclave_model, "sgx" if use_sgx else "native")

    if use_sgx:
        test_bytes = ennclave.sgx_forward(
            inputs.tobytes(), size, output_size)
    else:
        test_bytes = ennclave.native_forward(
            inputs.tobytes(), size, output_size)

    test_result = np.frombuffer(test_bytes, dtype=np.float32)
    np.testing.assert_almost_equal(test_result, expected_result, decimal=5)


if __name__ == '__main__':
    test_shape = (1, 5)

    test_input = np.arange(test_shape[1]).reshape((1,) + test_shape)
    test_model = Sequential(layers.Dense(5, input_shape=test_shape))
    test_model(test_input)
    common_test_basis(test_model, False)
    print("Generated code returns the same result :)")
