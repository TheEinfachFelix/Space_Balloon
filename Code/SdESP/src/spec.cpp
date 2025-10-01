#include "spec.hpp"

int chanels = 18;
float* values = (float*) malloc(chanels * sizeof(float)); //hier allokieren wir den Speicher für die Werte

bool setUpSpec(){
  return (spec_scl, spec_sda);
}
bool setUpSpec(int scl, int sda)
{
    return true;
}

float readOne()
{
    return 0.0;
}
float* readAll()
{
    return values;
}