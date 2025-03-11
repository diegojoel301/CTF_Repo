#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#define BUF_SIZE    0x100

void init(char *argv[], char **envp) {
    for (int i = 0; argv[i]; i++) argv[i] = NULL;
    for (int i = 0; envp[i]; i++) envp[i] = NULL;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

void main(int argc, char *argv[], char **envp)
{
    FILE *stream;
    char *buf;
    
    puts("Hello from the void");

    init(argv, envp);

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    stream = fopen("/dev/null", "a");

    buf = malloc(BUF_SIZE);

    while (1) {
        buf[read(STDIN_FILENO, buf, BUF_SIZE) - 1] = '\0';
        fprintf(stream, buf);
    }
}