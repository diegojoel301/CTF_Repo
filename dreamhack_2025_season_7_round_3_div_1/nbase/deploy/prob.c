// gcc -o prob prob.c 
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <stdbool.h>

#include <sys/mman.h>

typedef unsigned long long int ull;

void set(char *v, int i, int ptrsize)
{
    ull val;
    scanf("%lld", &val);
    memcpy(v + i * ptrsize, &val, ptrsize);
}

ull get(char *v, int i, int ptrsize)
{
    ull val = 0;
    memcpy(&val, v + i * ptrsize, ptrsize);
    return val;
}

int calc()
{
    ull base;
    char v[0x40] = {0};
    printf("Base: ");
    scanf("%llu", &base);
    
    int ptrsize = 0;
    if(base < (1LL << 8))
        ptrsize = 1;
    else if(base < (1LL << 16))
        ptrsize = 2;
    else if(base < (1LL << 32))
        ptrsize = 4;
    else
        ptrsize = 8;
    printf("Ptr address: %p\n", &ptrsize);

    memset(v, 0, 0x40);
    for(int i = 0; i < 0x10; i++)
    {
        set(v, i, ptrsize);
        
        printf("\nCon Address: %p\n", &base);
        
        /*
        get(v, i, ptrsize) >= base

        0x...  v
        ......
        0x...  base

        Basicamente lo que hace confirmqar que no hayas editado base xd
        */
        if(get(v, i, ptrsize) < 0 || get(v, i, ptrsize) >= base) // Esto siempre se cumplira cuando se pase asi que hay que pensar en otra cosa, no hay forma de saltar esto
        {
            printf("Fcito: %lld", get(v, i, ptrsize));
            sleep(2);
            
            printf("\nNuestra base es: %lld", base);
            printf("\nCon Address: %p\n", base);
            memset(v + i * ptrsize, 0, ptrsize);
            break;
        }
    }
        
    ull val = 0;
    for(int i = 0; i < 0x10; i++)
    {
        val *= base;
        val += get(v, i, ptrsize);
    }
    printf("Value: %llu\n", val);
}

int main()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    
    printf("n Base Calculator\n");

    printf("wait...\n");
    //sleep(60);

    while(true)
        calc();
}