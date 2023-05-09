#!/bin/zsh

SIZE_WITHPREFIX="1G"
SIZE_NOPREFIX="1000000000"
echo "Generating files with size ${SIZE_WITHPREFIX}..."
formats=("x1" "x2" "x4" "x8" "a" "c" "d1" "d2" "d4" "d8" "f" "o" "u1" "u2" "u4" "u8")
# i=0
# for format in ${formats}; do
#     printf "Format: ${format}->$((i + 10))\n"
#     i=$((i+1))
# done

i=0
for format in ${formats}; do
    echo "Format: ${format}"
    od --format=${format} --address-radix=n /dev/urandom | tr -d " " | tr -d "\n"  | head -c ${SIZE_WITHPREFIX} > test-$((i + 10))-${SIZE_WITHPREFIX}.txt
    i=$((i+1))
done

