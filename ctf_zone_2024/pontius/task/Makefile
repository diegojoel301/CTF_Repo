all:
	gcc -fstack-protector -Wl,-z,relro,-z,now main.c ponlloc.c -o pontius unicorn/build/*.a -I unicorn/include -lseccomp -lpthread -lm 
