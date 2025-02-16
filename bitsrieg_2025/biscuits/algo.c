#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main() {
    int val;

    scanf("%d", &val);

    srand(val);

    unsigned long val_rand = rand();

    printf("\n%d\n", val_rand);

    val_rand = rand();

    printf("\n%d\n", val_rand);

    return 0;
}