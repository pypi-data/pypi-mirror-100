// Avoids C++ name mangling with extern "C"
#define EXTERN_DLL_EXPORT extern "C"
#include <stdlib.h>
#include<iostream>

// Handles 64 bit complex numbers, i.e. two 32 bit (4 byte) floating point numbers
EXTERN_DLL_EXPORT int add(int a, int b);

// Handles 128 bit complex numbers, i.e. two 64 bit (8 byte) floating point numbers
EXTERN_DLL_EXPORT int sub(int a,int b);
