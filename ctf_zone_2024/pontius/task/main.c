#define _GNU_SOURCE
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <seccomp.h>
#include <unicorn/unicorn.h>

#include "ponlloc.h"

typedef struct text {
	char* str;
	uint32_t size;
} text;

#define ADDRESS 0xcafeb000
#define CODE_SIZE 0x1000

#define TEXTS_SIZE 16
text* texts = 0;

void setup() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);
	seccomp_load(ctx);
	seccomp_release(ctx);
}

void hook_call(uc_engine* uc, unsigned intno, void* user_data) {
	uint64_t rax, rbx, rcx, rdx, rdi, rsi, r8, r9;
	uc_reg_read(uc, UC_X86_REG_RAX, &rax);
	if (rax > 4) {
		return;
	}
	switch (rax) {
		case 1: // create_text
			uint64_t i = 0;
			uc_reg_read(uc, UC_X86_REG_RDI, &rdi);
			for (; i < TEXTS_SIZE; i++) {
				if (!texts[i].str) {
					break;
				} 
			}
			if (i == TEXTS_SIZE) {
				break;
			}
			texts[i].size = rdi;
			texts[i].str = ponlloc(rdi);
			uc_reg_write(uc, UC_X86_REG_RAX, &i);
			break;
		case 2: // edit_text
			uc_reg_read(uc, UC_X86_REG_RDI, &rdi);
			uc_reg_read(uc, UC_X86_REG_RSI, &rsi);
			uc_reg_read(uc, UC_X86_REG_RDX, &rdx);
			if ((rdi > TEXTS_SIZE - 1) || (rdx > texts[rdi].size)) {
				break;
			}
			uc_mem_read(uc, rsi, texts[rdi].str, rdx);
			break;
		case 3: // delete_text
			uc_reg_read(uc, UC_X86_REG_RDI, &rdi);
			if ((rdi > TEXTS_SIZE - 1) || !texts[rdi].str) {
				break;
			}
			ponfree(texts[rdi].str);
			texts[rdi].str = 0;
			texts[rdi].size = 0;
			break;
		case 4: // print_text
			uc_reg_read(uc, UC_X86_REG_RDI, &rdi);
			if ((rdi > TEXTS_SIZE - 1) || !texts[rdi].str) {
				break;
			}
			puts(texts[rdi].str);
			break;
		default:
			break;
	}
}

int main(int argc, char **argv, char **envp)
{
	char shellcode[0x1000] = {0};

	uc_engine *uc;
	uc_hook trace;
	uc_err err;
	int bytes_read;

	setup();

	texts = ponlloc(TEXTS_SIZE * sizeof(text));

	for (;;) {
		err = uc_open(UC_ARCH_X86, UC_MODE_64, &uc);
		if (err != UC_ERR_OK) {
			printf("Failed on uc_open() with error returned: %u\n", err);
			return -1;
		}

		uc_mem_map(uc, ADDRESS, 0x1000, UC_PROT_ALL);
		err = uc_hook_add(uc, &trace, UC_HOOK_INTR, hook_call, 0, 1, 0);

		printf("Waiting for your shellcode...\n");

		if ((bytes_read = read(0, shellcode, CODE_SIZE)) < 0) {
			exit(-1);
		}

		if (uc_mem_write(uc, ADDRESS, shellcode, bytes_read)) {
			printf("Failed to write emulation code to memory, quit!\n");
			return -1;
		}

		err = uc_emu_start(uc, ADDRESS, ADDRESS + bytes_read, 0, 0);
		if (err) {
			printf("Failed on uc_emu_start() with error returned %u: %s\n",
			err, uc_strerror(err));
		}

		uc_close(uc);
	}
	return 0;
}
