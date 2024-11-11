#include<stdio.h>

int main()
{
  char *format;

  fgets(format, 0x80, stdin);

  printf(format);
}
