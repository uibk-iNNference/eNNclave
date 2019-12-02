
# Table of Contents

1.  [NN SGX](#orgdf0a29e)
    1.  [People](#org41671f1)
    2.  [Current Status](#orgf14717f)
    3.  [Related Work](#orgf8c6445)
2.  [README](#org217d7cf)
    1.  [Setting up a testing environment](#orgf3292d4)
    2.  [Training a model](#org0514bbd)
    3.  [Extracting the enclave](#org04b99e6)
    4.  [Compiling the enclave](#org5b9c65d)
    5.  [Running the enclave](#org0f7a51e)
        1.  [Setting up `LD_LIBRARY_PATH`](#org7c4798a)
        2.  [Evaluating models](#org3df8e4c)
    6.  [Under the hood](#org0090cbb)


<a id="orgdf0a29e"></a>

# NN SGX

Running some parts or all of a CNN inside the trusted enclave to reduce leakage and protect against model stealing.
We hope to make this as robust against model stealing as online oracles.


<a id="org41671f1"></a>

## People

RBO, CPA, ASC


<a id="orgf14717f"></a>

## Current Status

As of now moving large models (VGG16) into the enclave works correctly, but with massive slowdown.
Some results:

    Taking 10 images from MIT67 test_set
    Predicting with TF model
    Prediction took 0.582809 seconds
    TF model accuracy: 0.6
    Predicting with Enclave model
    Prediction took 972.469672 seconds
    10 of 10 labels are equal, slowdown factor: 1668.591

The slowdown is incurred due to the ineficcient way memory is accessed during convolution, and also because memory has to be paged constantly.


<a id="orgf8c6445"></a>

## Related Work

We have different areas of related work that are relevant to this project.
The most directly relevant area is model stealing attacks and adversarial robustness.
In model stealing an attacker tries to build a replicant model that rivals the prediction accuracy of the stolen model, with hopefully lower cost than using the original model.
[Tramer et al.](related_work/tramer16stealing.pdf) use a model-dependent dataset augmentation algorithm to find a reasonably low number of queries required for extracting the model.
The number they arrive at for NNs is `100*k`, where `k` is the number of parameters.
Our model (even with the weights in the feature extractor fixed) still have ~18,000,000 trainable parameters, which pushes this attack (as it is) outside the realm of feasability in my opinion.

Another relevant area of research is adversarial attacks.
[Papernot et al.](related_work/papernot17practical.pdf) have presented a so-called black-box transfer attack, in which an attacker builds a local replicant model and builds adversarial examples on the gradients of that model.
This requires far less queries than are required for model stealing, but the replicant model does not have to be accurace.
Its only requirement is that its gradients are sufficiently aligned with the target model to build functional adversarial examples.

Our implementation affects data privacy, as it allows users to keep the data they wish to predict on private.
It also allows for the creation of offline black box oracles, which are used e.g. in [set membership attacks](related_work/shokri17membership.pdf).
As it currently stands, we do not return confidence values, only the resulting label.
This makes the attack presented by Shokri et al. not better than chance, as evidenced by their own results.

In the context of data privacy [Ohrimenko et al.](related_work/ohrimenko16enclave.pdf) have also previously combined machine learning with trusted enclaves.
The difference between their approach and ours is that they trained the model inside the enclave, which allows parties to also keep their training data private.
Their focus is on ensuring that no inference on the training data can be made using timing side channels, and they disregard performance.
Our focus is instead on the performance impact of such an approach.

[Tramer et al.](related_work/tramer19slalom.pdf) provide a mechanism to use the enclave as a controller for running NNs on the GPU.
Every layer is verified inside the Enclave, to give a statistical guarantee for integrity.
They also utilize an additive stream cipher which is (as they claim, I don't know enough of the math behind it to verify) invariant to the computations taking place in the DNN.
This gives them data privacy, while running the model on the provider's hardware.

The enclave alone does not provide a mechanism for rate limiting, and thus not for monetization.
[Kaptchuk et al.](related_work/kaptchuk2019state.pdf) utilize signatures coming from a server for this.
Their main contribution is putting the signatures in a public ledger, which might be sexy, but not necessary for our use-case.
The basic idea is very relevant however.
By having a customer send a hash of the data they wish to run inference on to the provider, who then signs the hash (after being paid) and sends the signature back, we can monetize access to the model by query.
The model can then verify the signature using the public testing key of the provider.
Only if the signature is valid will it run inference.


<a id="org217d7cf"></a>

# README


<a id="orgf3292d4"></a>

## Setting up a testing environment

Building SGX enclaves on Linux requires building the SGX-SDK from scratch.
This process only works on Ubuntu 18.04 and some other older distributions.
Our test machines run Ubuntu Server 18.04, and I provide a setup script for the SDK [here](setup/setup_sgx_machine.sh).

The python requirements are all in [requirements.txt](requirements.txt).


<a id="org0514bbd"></a>

## Training a model

Our current evaluation dataset, MIT67, can be downloaded [here](http://web.mit.edu/torralba/www/indoor.html).
The site provides a download of the dataset, as well as a specification of which images are in the training and test sets.
The specification files are great for having consistent and reproducible results.

Our training scripts expect the extracted data to be in `data/mit67`, with both `.txt` files being in that directory as well.
The model can then be trained using the `mit67_train.py` script.


<a id="org04b99e6"></a>

## Extracting the enclave

The script called `build_enclave_files.py` is used to generate the weight files and the C functions.
It takes two parameters: the original model file, and the number of layers to extract into an enclave.
The extracted layers will be replaced by an `EnclaveLayer`, which wraps the generated enclave in a manner compatible with the TensorFlow API.
From the original layers that were not extracted and the new `EnclaveLayer` it builds a new model, and saves it.

The script creates a `forward.cpp` and multiple `.bin` files.
Inside the `.bin` files are the layer weights which will be compiled into the enclave.
The `forward.cpp` file contains the forward function of the enclave.


<a id="org5b9c65d"></a>

## Compiling the enclave

Building the enclave (or native) code happens in the `lib` directory, so move the generated files there.

The decision which version to build is decided based on the `MODE` environment variable.
All directories contain Makefiles, so running `make` in the project root will build all necessary subdirectories.


<a id="org0f7a51e"></a>

## Running the enclave


<a id="org7c4798a"></a>

### Setting up `LD_LIBRARY_PATH`

The enclave model needs to be able to find the shared libraries that were previously compiled.
To provide the location of the libraries, please run this command from the project root:

    source setup/setup_ld_path.sh


<a id="org3df8e4c"></a>

### Evaluating models

TODO


<a id="org0090cbb"></a>

## Under the hood

The underlying interaction with the enclave is a bit roundabout, but that also preserves modularity.

The `EnclaveLayer` calls the Python-C interoperability code in [pymatutilmodule.c](interop/pymatutilmodule.c) (which is previosly compiled into a shared library).
That code does the conversion between Python `byte` arrays and C `char` arrays.
It then calls the libraries generated in the `lib` directory, and converts the output back to Python objects.

The enclave also consists of two shared libraries, one in the enclave and one being the wrapper around the enclave that's autogenerated by the Intel SDK.

The rest is "basic" C interaction.

