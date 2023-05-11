#!/bin/zsh

SIZE_WITHPREFIX="100M"
SIZE_NOPREFIX="100000000"
echo "Generating files with size ${SIZE_WITHPREFIX}..."
formats=("x" "a" "c" "d1" "d2" "d4" "d8" "f" "o" "u1" "u2" "u4" "u8")
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

