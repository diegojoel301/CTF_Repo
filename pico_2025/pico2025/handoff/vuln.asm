   0x0000000000401229 <+0>:	    endbr64
   0x000000000040122d <+4>:	    push   rbp
   0x000000000040122e <+5>:	    mov    rbp,rsp
   0x0000000000401231 <+8>:	    sub    rsp,0x2f0
   0x0000000000401238 <+15>:	mov    DWORD PTR [rbp-0x4],0x0 ; total_entries
   0x000000000040123f <+22>:	mov    DWORD PTR [rbp-0x2e4],0xffffffff ; choice 
   0x0000000000401249 <+32>:	mov    eax,0x0
   0x000000000040124e <+37>:	call   0x4011f6 <print_menu>
   0x0000000000401253 <+42>:	lea    rax,[rbp-0x2e4]
   0x000000000040125a <+49>:	mov    rsi,rax
   0x000000000040125d <+52>:	mov    edi,0x402079
   0x0000000000401262 <+57>:	mov    eax,0x0
   0x0000000000401267 <+62>:	call   0x4010f0 <__isoc99_scanf@plt>
   0x000000000040126c <+67>:	cmp    eax,0x1
   0x000000000040126f <+70>:	je     0x40127b <vuln+82>
   0x0000000000401271 <+72>:	mov    edi,0x0
   0x0000000000401276 <+77>:	call   0x401100 <exit@plt>
   0x000000000040127b <+82>:	call   0x4010c0 <getchar@plt>
   0x0000000000401280 <+87>:	mov    eax,DWORD PTR [rbp-0x2e4]
   0x0000000000401286 <+93>:	cmp    eax,0x1
   0x0000000000401289 <+96>:	jne    0x401301 <vuln+216>
   0x000000000040128b <+98>:	mov    DWORD PTR [rbp-0x2e4],0xffffffff
   0x0000000000401295 <+108>:	cmp    DWORD PTR [rbp-0x4],0x9
   0x0000000000401299 <+112>:	jle    0x4012aa <vuln+129>
   0x000000000040129b <+114>:	mov    edi,0x40207c
   0x00000000004012a0 <+119>:	call   0x4010a0 <puts@plt>
   0x00000000004012a5 <+124>:	jmp    0x401407 <vuln+478>
   0x00000000004012aa <+129>:	mov    edi,0x402098
   0x00000000004012af <+134>:	call   0x4010a0 <puts@plt>
   0x00000000004012b4 <+139>:	mov    rax,QWORD PTR [rip+0x2db5]        # 0x404070 <stdin@@GLIBC_2.2.5>
   0x00000000004012bb <+146>:	mov    rdi,rax
   0x00000000004012be <+149>:	call   0x4010d0 <fflush@plt>
   0x00000000004012c3 <+154>:	mov    rcx,QWORD PTR [rip+0x2da6]        # 0x404070 <stdin@@GLIBC_2.2.5>
   0x00000000004012ca <+161>:	lea    rsi,[rbp-0x2e0]
   0x00000000004012d1 <+168>:	mov    eax,DWORD PTR [rbp-0x4]
   0x00000000004012d4 <+171>:	movsxd rdx,eax
   0x00000000004012d7 <+174>:	mov    rax,rdx
   0x00000000004012da <+177>:	shl    rax,0x3
   0x00000000004012de <+181>:	add    rax,rdx
   0x00000000004012e1 <+184>:	shl    rax,0x3
   0x00000000004012e5 <+188>:	add    rax,rsi
   0x00000000004012e8 <+191>:	mov    rdx,rcx
   0x00000000004012eb <+194>:	mov    esi,0x20
   0x00000000004012f0 <+199>:	mov    rdi,rax
   0x00000000004012f3 <+202>:	call   0x4010b0 <fgets@plt>
   0x00000000004012f8 <+207>:	add    DWORD PTR [rbp-0x4],0x1
   0x00000000004012fc <+211>:	jmp    0x401249 <vuln+32>
   0x0000000000401301 <+216>:	mov    eax,DWORD PTR [rbp-0x2e4]
   0x0000000000401307 <+222>:	cmp    eax,0x2
   0x000000000040130a <+225>:	jne    0x4013b6 <vuln+397>
   0x0000000000401310 <+231>:	mov    DWORD PTR [rbp-0x2e4],0xffffffff
   0x000000000040131a <+241>:	mov    edi,0x4020c0
   0x000000000040131f <+246>:	call   0x4010a0 <puts@plt>
   0x0000000000401324 <+251>:	lea    rax,[rbp-0x2e4]
   0x000000000040132b <+258>:	mov    rsi,rax
   0x000000000040132e <+261>:	mov    edi,0x402079
   0x0000000000401333 <+266>:	mov    eax,0x0
   0x0000000000401338 <+271>:	call   0x4010f0 <__isoc99_scanf@plt>
   0x000000000040133d <+276>:	cmp    eax,0x1
   0x0000000000401340 <+279>:	je     0x40134c <vuln+291>
   0x0000000000401342 <+281>:	mov    edi,0x0
   0x0000000000401347 <+286>:	call   0x401100 <exit@plt>
   0x000000000040134c <+291>:	call   0x4010c0 <getchar@plt>
   0x0000000000401351 <+296>:	mov    eax,DWORD PTR [rbp-0x2e4]
   0x0000000000401357 <+302>:	cmp    DWORD PTR [rbp-0x4],eax
   0x000000000040135a <+305>:	jg     0x40136b <vuln+322>
   0x000000000040135c <+307>:	mov    edi,0x4020f5
   0x0000000000401361 <+312>:	call   0x4010a0 <puts@plt>
   0x0000000000401366 <+317>:	jmp    0x401407 <vuln+478>
   0x000000000040136b <+322>:	mov    edi,0x402110
   0x0000000000401370 <+327>:	call   0x4010a0 <puts@plt>
   0x0000000000401375 <+332>:	mov    rcx,QWORD PTR [rip+0x2cf4]        # 0x404070 <stdin@@GLIBC_2.2.5>
   0x000000000040137c <+339>:	mov    eax,DWORD PTR [rbp-0x2e4]
   0x0000000000401382 <+345>:	lea    rsi,[rbp-0x2e0]
   0x0000000000401389 <+352>:	movsxd rdx,eax
   0x000000000040138c <+355>:	mov    rax,rdx
   0x000000000040138f <+358>:	shl    rax,0x3
   0x0000000000401393 <+362>:	add    rax,rdx
   0x0000000000401396 <+365>:	shl    rax,0x3
   0x000000000040139a <+369>:	add    rax,rsi
   0x000000000040139d <+372>:	add    rax,0x8
   0x00000000004013a1 <+376>:	mov    rdx,rcx
   0x00000000004013a4 <+379>:	mov    esi,0x40
   0x00000000004013a9 <+384>:	mov    rdi,rax
   0x00000000004013ac <+387>:	call   0x4010b0 <fgets@plt>
   0x00000000004013b1 <+392>:	jmp    0x401249 <vuln+32>
   0x00000000004013b6 <+397>:	mov    eax,DWORD PTR [rbp-0x2e4]
   0x00000000004013bc <+403>:	cmp    eax,0x3
   0x00000000004013bf <+406>:	jne    0x4013f3 <vuln+458>
   0x00000000004013c1 <+408>:	mov    DWORD PTR [rbp-0x2e4],0xffffffff
   0x00000000004013cb <+418>:	mov    edi,0x402140
   0x00000000004013d0 <+423>:	call   0x4010a0 <puts@plt>
   0x00000000004013d5 <+428>:	mov    rdx,QWORD PTR [rip+0x2c94]        # 0x404070 <stdin@@GLIBC_2.2.5>
   0x00000000004013dc <+435>:	lea    rax,[rbp-0xc]
   0x00000000004013e0 <+439>:	mov    esi,0x20
   0x00000000004013e5 <+444>:	mov    rdi,rax
   0x00000000004013e8 <+447>:	call   0x4010b0 <fgets@plt>
   0x00000000004013ed <+452>:	mov    BYTE PTR [rbp-0x5],0x0
   0x00000000004013f1 <+456>:	jmp    0x40140c <vuln+483>
   0x00000000004013f3 <+458>:	mov    DWORD PTR [rbp-0x2e4],0xffffffff
   0x00000000004013fd <+468>:	mov    edi,0x4021b6
   0x0000000000401402 <+473>:	call   0x4010a0 <puts@plt>
   0x0000000000401407 <+478>:	jmp    0x401249 <vuln+32>
   0x000000000040140c <+483>:	nop
   0x000000000040140d <+484>:	leave
=> 0x000000000040140e <+485>:	ret