#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/random.h>

typedef struct {
    long uid;
    char username[8];
    char password[8];
} user_t;

typedef struct user_entry user_entry_t;

struct user_entry {
    user_t* user;
    user_entry_t* prev;
    user_entry_t* next;
};

user_entry_t user_list;
long UID = 1;

void init() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
}

int menu() {
    int choice;
    puts("1. Sign up");
    puts("2. Sign in");
    puts("3. Remove account");
    puts("4. Get shell");
    printf("> ");
    scanf("%d", &choice);
    return choice;
}

void sign_up() {
    user_t* user = malloc(sizeof(user_t));  /* En el heap ser reserva un espacio de tamaño user_t para un user_t */
    user_entry_t* entry = malloc(sizeof(user_entry_t)); /* En el heap ser reserva un espacio de tamaño user_entry_t para un user_t, es decir reservamos un espacio en el heap para un nuevo nodo */
    user->uid = UID++; /* El UID se incrementa y se asigna a este nuevo usuario */
    /*Lectura de username y password de nuestro user */
    printf("username: ");
    read(0, user->username, 8);
    printf("password: ");
    read(0, user->password, 8);
    entry->user = user; /* En el nuevo nodo lo enlazamos con el user que estamos creando*/

    /* curr tomara la direccion de memoria del user_list  */
    user_entry_t* curr = &user_list;

    /* Se recorrera nodo a nodo hasta el final de la lista triplemente enlazada */

    while(curr->next) {
        curr = curr->next;
    }

    /*
    Una vez se llega al final de la lista triplemente enlazada
    Del nuevo nodo, el enlace anterior se enlaza al user_list
    */
    entry->prev = curr;
    /* Y el enlace siguiente del user_list lo enlazara a nuestro nuevo nodo*/
    curr->next = entry;
}

void remove_account(int uid) {
    /* curr sera el user_list */
    user_entry_t* curr = &user_list;
    do {
        /* Se recorrera cada nodo del user_list y se comprabara el user_t de cada nodo si el uid es igual al uid pasado por argumento*/
        if(curr->user->uid == uid) {
            /*Por si: Se comprueba primeramente que el nodo anterior no sea null */
            if(curr->prev) {
                /* Cuando no es null entonces el enlace al nodo anterior en el nodo actual se enlazara con el siguiente elemento del nodo actual*/
                curr->prev->next = curr->next;
            }
            /* Se comprueba si de nuestro nodo a eliminar el siguiente elemento es null */
            if(curr->next) {
                /* Cuando no es null entonces el enlace al nodo siguiente en el nodo actual se enlazara con el anterior elemento del nodo actual*/
                curr->next->prev = curr->prev;
            }
            /* Primero se libera el user_t al nodo a eliminar */

            free(curr->user);

            /* Posterior a ello liberamos el nodo actual */

            free(curr);
            break;
        }
        /* Caso contrario se seguira recorriendo al siguiente nodo del user_list */
        curr = curr->next;
    } while(curr);
}

long sign_in() {
    char username[9] = {0}; /* Vector username con un buffer de 9 bytes y un null byte */
    char password[9] = {0}; /* Vector password con un buffer de 9 bytes y un null byte */
    printf("username: ");
    read(0, username, 8);   
    printf("password: ");
    read(0, password, 8);
    /* curr como la posicion de memoria de user_list */
    user_entry_t* curr = &user_list;
    do {
        /*
            En el nodo actual se va por el enlace a la estructura user_t y se comprueba el usuario y password
            Por si, se retornara el UID de ese user_t del nodo actual
        */
        if(memcmp(curr->user->username, username, 8) == 0 && memcmp(curr->user->password, password, 8) == 0) {
            printf("Logging in as %s\n", username);
            
            return curr->user->uid;
        }
        /*
            Caso contrario, se recorrera al siguiente nodo
        */
        curr = curr->next;
        /* Asi sucesivamente hasta llegar a 0x0 para romper el bucle*/
    } while(curr);
    /* Caso contrario se retornara -1 */
    return -1; 
}

int main() {
    init();

    long uid = -1;
    user_t root = {
        .uid = 0,
        .username = "root",
    };
    if(getrandom(root.password, 8, 0) != 8) {
        exit(1);
    }

    user_list.next = NULL;
    user_list.prev = NULL;
    user_list.user = &root;

    while(1) {
        int choice = menu();
        if(choice == 1) {
            sign_up();
        } else if(choice == 2) {
            uid = sign_in();
            if(uid == -1) {
                puts("Invalid username or password!");
            }
        } else if(choice == 3) {
            if(uid == -1) {
                puts("Please sign in first!");
            } else {
                remove_account(uid);
                uid = -1;
            }
        } else if(choice == 4) {
            if(uid == 0) {
                system("/bin/sh");
            } else {
                puts("Please sign in as root first!");
            }
        } else {
            exit(1);
        }
    }
}
