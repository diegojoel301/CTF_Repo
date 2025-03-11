bool main(void)

{
  ostream *poVar1;
  char *__command;
  long in_FS_OFFSET;
  bool bVar2;
  allocator local_4d;
  int local_4c;
  string local_48 [40];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  poVar1 = std::operator<<((ostream *)std::cout,"Computing the  MD5 hash of /root/flag.txt.... ");
  poVar1 = (ostream *)std::ostream::operator<<(poVar1,std::end l<>);
  std::ostream::operator<<(poVar1,std::endl<>);
  sleep(2);
  std::allocator<char>::allocator();
                    /* try { // try from 001013aa to 001013ae has its C atchHandler @ 0010144f */
  std::string::string(local_48,"/bin/bash -c \'md5sum /root/flag.tx t\'",&local_4d);
  std::allocator<char>::~allocator((allocator<char> *)&local_4d );
  setgid(0);
  setuid(0);
  __command = (char *)std::string::c_str();
                    /* try { // try from 001013de to 00101423 has its C atchHandler @ 0010146d */
  local_4c = system(__command);
  bVar2 = local_4c != 0;
  if (bVar2) {
    poVar1 = std::operator<<((ostream *)std::cerr,"Error: system () call returned non-zero value: ");
    poVar1 = (ostream *)std::ostream::operator<<(poVar1,local_ 4c);
    std::ostream::operator<<(poVar1,std::endl<>);
  }
  std::string::~string(local_48);
  if (local_20 == *(long *)(in_FS_OFFSET + 0x28)) {
    return bVar2;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
