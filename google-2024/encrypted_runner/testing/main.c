#include <stdio.h>
#include <string.h>
#include <stdint.h>

int main()
{
  uint32_t data[16];

  for (int i = 0; i < 16; i++)
  {
    scanf("%x", &data[i]);
  }

  return 0;
}
