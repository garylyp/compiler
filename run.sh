#!/bin/bash

file=$1
python3 src/compile.py test/$file.j > test/$file.s

arm-linux-gnueabi-gcc -g -o test/$file.out test/$file.s --static

qemu-arm test/$file.out