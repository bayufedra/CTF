#!/usr/bin/env python

import ast
from pwn import *

nc = remote("35.187.236.126", 8022)

for i in range(50):
	nc.recvuntil("Wordlist: ")
	wordlist = ast.literal_eval(str(nc.recvline()))
	nc.recvuntil("Nama kota yang di acak: ")
	random = str(nc.recvline()).replace("\n", "")
	jawaban = ""
	print "[+] Wordlist ->", wordlist
	print "[+] Kota Acak ->", random
	
	for i in wordlist:
		if len(i) == len(random) and sorted(i) == sorted(random):
			jawaban = i
			
	print "[+] Jawaban ->", jawaban
	nc.sendline(jawaban)
	print nc.recvline()
	
print nc.recvline()