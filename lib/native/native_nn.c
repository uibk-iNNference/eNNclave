#include "forward.h"
#include "native_nn.h"

int native_nn_forward(float *m, int size, int *label){
  return native_f(m, size, label);
}
