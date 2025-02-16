#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main() {
    int val;

    scanf("%d", &val);

    srand(val);

    int val_rand;

    for(int i = 0; i < 100 - 1; i++)
    {
        val_rand = rand();
        printf("%d,", val_rand % 100);
    }
    printf("%d", rand() % 100);

    return 0;
}