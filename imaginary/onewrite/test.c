#include<stdio.h>

int main()
{
    char *test;
    scanf("%p%*c", &test);
    fgets(test, 768, 0);
    return 0;
}