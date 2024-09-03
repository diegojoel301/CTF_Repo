#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

int main() {
    const char *filename = "flag.txt";
    char buf[1024];  // Buffer para almacenar el contenido leído
    int file_fd;     // Descriptor de archivo

    // Abrir el archivo con openat
    int dir_fd = AT_FDCWD;  // Directorio actual
    file_fd = openat(dir_fd, filename, O_RDONLY);
    if (file_fd == -1) {
        perror("Error al abrir el archivo");
        exit(EXIT_FAILURE);
    }

    // Leer el contenido del archivo con read
    ssize_t num_read = read(file_fd, buf, sizeof(buf)-1);
    if (num_read == -1) {
        perror("Error al leer el archivo");
        close(file_fd);
        exit(EXIT_FAILURE);
    }

    // Asegurarse de que el buffer termina con un carácter nulo
    buf[num_read] = '\0';

    // Imprimir el contenido leído
    printf("Contenido de '%s':\n%s\n", filename, buf);

    // Cerrar el archivo
    close(file_fd);

    return 0;
}

