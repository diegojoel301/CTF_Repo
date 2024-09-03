#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <limits.h>
#include <linux/limits.h>

int main() {
    char path[PATH_MAX];
    char linkbuf[PATH_MAX];
    int fd;

    // Abrir el archivo flag.txt usando openat
    fd = openat(AT_FDCWD, "flag.txt", O_RDONLY);
    if (fd == -1) {
        perror("Error al abrir el archivo");
        exit(EXIT_FAILURE);
    }

    // Leer el enlace simbólico asociado al descriptor fd
    ssize_t len = readlinkat(fd, "", linkbuf, sizeof(linkbuf));
    if (len == -1) {
        perror("Error al leer el enlace simbólico");
        exit(EXIT_FAILURE);
    }

    // Asegurar que la cadena de caracteres está terminada correctamente
    linkbuf[len] = '\0';

    // Imprimir el contenido del enlace simbólico
    printf("Contenido del enlace simbólico: %s\n", linkbuf);

    // Cerrar el descriptor de archivo
    close(fd);

    return 0;
}

