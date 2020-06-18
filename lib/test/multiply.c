#include "test/multiply.h"

#include "matutil.h"
#include "test/util.h"
#include "test/assert.h"

#include <stdlib.h>

int mul_zeros()
{
  int h = 5;
  int w = 5;
  float a[] = {0.916, 0.315, 0.935, 0.254, -0.717, 0.847, 0.88, 0.839, 0.978, -0.685, 0.318, -0.752, -0.246, 0.698, -0.193, 0.231, 0.241, 0.29, -0.471, 0.646, -0.525, -0.211, -0.964, 0.673, -0.364};
  float b[] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
  float expected[] = {0.0, 0.0, 0.0, 0.0, -0.0, 0.0, 0.0, 0.0, 0.0, -0.0, 0.0, -0.0, -0.0, 0.0, -0.0, 0.0, 0.0, 0.0, -0.0, 0.0, -0.0, -0.0, -0.0, 0.0, -0.0};
  float res[h * w];
  matutil_multiply(a, h, w, b, h, w, res);
  return print_result("Multiplication zeroes", assert_equality(res, expected, h * w));
}

int mul_sequential()
{
  int h = 5;
  int w = 5;
  float a[] = {0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0};
  float b[] = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
  float expected[] = {10.0, 10.0, 10.0, 10.0, 10.0, 35.0, 35.0, 35.0, 35.0, 35.0, 60.0, 60.0, 60.0, 60.0, 60.0, 85.0, 85.0, 85.0, 85.0, 85.0, 1.1e+02, 1.1e+02, 1.1e+02, 1.1e+02, 1.1e+02};
  float res[h * w];
  matutil_multiply(a, h, w, b, h, w, res);
  return print_result("Multiplication sequential", assert_equality(res, expected, h * w));
}

int mul_random_1()
{
  int h = 3;
  int w = 3;
  float a[] = {0.535, 0.728, -0.815, 0.3, 0.314, 0.258, 0.681, -0.292, 0.153};
  float b[] = {-0.226, -0.229, 0.318, -0.268, -0.343, 0.623, -0.397, -0.709, -0.753};
  float expected[] = {0.00786, 0.206, 1.24, -0.254, -0.359, 0.0964, -0.137, -0.164, -0.0808};
  float res[h * w];
  matutil_multiply(a, h, w, b, h, w, res);
  return print_result("Multiplication random 1", assert_similarity(res, expected, h * w));
}

int mul_random_2()
{
  int h = 3;
  int w = 3;
  float a[] = {-0.389, 0.332, -0.0812, -0.734, -0.29, 0.177, -0.0822, 0.618, 0.103};
  float b[] = {-0.409, -0.261, -0.697, -0.883, -0.476, -0.815, 0.142, -0.0649, 0.132};
  float expected[] = {-0.145, -0.0513, -0.0103, 0.581, 0.318, 0.772, -0.498, -0.28, -0.433};

  float res[h * w];
  matutil_multiply(a, h, w, b, h, w, res);
  return print_result("Multiplication random 2", assert_similarity(res, expected, h * w));
}

int mul_random_3()
{
  int h = 7;
  int w = 7;
  float a[] = {-0.425, 0.596, -0.801, 0.318, -0.101, 0.553, -0.647, 0.273, -0.694, -0.59, -0.759, -0.39, 0.391, -0.992, 0.921, 0.0571, -0.824, 0.947, -0.412, -0.243, 0.608, -0.0493, 0.37, 0.271, 0.0185, 0.692, -0.9, -0.0625, -0.348, 0.112, 0.376, -0.63, 0.874, -0.798, -0.63, 0.159, -0.971, 0.634, 0.416, 0.63, -0.165, -0.293, 0.633, -0.781, -0.833, -0.208, -0.294, -0.518, -0.757};
  float b[] = {0.333, 0.22, -0.689, -0.3, 0.579, -0.329, 0.666, -0.864, -0.587, 0.277, -0.391, -0.679, -0.363, -0.092, -0.869, 0.501, -0.479, -0.117, -0.0777, -0.0364, 0.46, 0.628, -0.833, 0.639, -0.0929, -0.454, -0.821, 0.195, -0.0742, -0.784, -0.0664, 0.0842, -0.599, 0.185, 0.465, -0.152, 0.185, -0.26, -0.434, -0.592, 0.576, -0.415, -0.0513, 0.112, 0.324, -0.623, -0.403, -0.816, -0.917};
  float expected[] = {0.195, -1.0, 0.698, 0.113, -0.74, 0.519, -0.328, 0.747, 1.07, -0.98, 0.744, 1.42, 1.77, 0.392, 1.61, -0.687, 0.668, -0.597, 0.274, -1.78, -0.234, -0.472, -0.824, 0.186, 0.325, -0.165, -0.483, 0.814, -0.846, -0.333, -0.366, 0.888, 0.182, 0.793, 1.12, 0.596, 0.0188, -0.51, 0.526, 0.353, 0.196, 1.2, 1.62, 0.403, -0.478, 0.904, 1.84, 0.54, 0.842};

  float res[h * w];
  matutil_multiply(a, h, w, b, h, w, res);
  return print_result("Multiplication random 3", assert_similarity(res, expected, h * w));
}

void test_multiply(int *correct_cases, int *total_cases)
{
  *correct_cases += mul_zeros();
  *total_cases += 1;

  *correct_cases += mul_sequential();
  *total_cases += 1;

  *correct_cases += mul_random_1();
  *total_cases += 1;

  *correct_cases += mul_random_2();
  *total_cases += 1;

  *correct_cases += mul_random_3();
  *total_cases += 1;
}