#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *fp;
    char flag[128];

    fp = fopen("/app/flag.txt", "r");
    if (fp == NULL) {
        printf("Error: cannot read flag.\n");
        return 1;
    }
    fgets(flag, sizeof(flag), fp);
    printf("%s", flag);
    fclose(fp);

    return 0;
}
