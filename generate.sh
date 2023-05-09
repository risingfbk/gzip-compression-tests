#!/bin/zsh

SIZE_WITHPREFIX="1G"
SIZE_NOPREFIX="1000000000"
echo "Generating files with size ${SIZE_WITHPREFIX}..."
# Level 1
echo "Level 1"
lorem -c ${SIZE_NOPREFIX} > test-1-${SIZE_WITHPREFIX}.txt
# Level 2
echo "Level 2"
head -c ${SIZE_WITHPREFIX} /dev/urandom > test-2-${SIZE_WITHPREFIX}.txt
# Level 3
# echo "Level 3"
# od --format=x --address-radix=n /dev/urandom | head -c ${SIZE_WITHPREFIX} > test-3-${SIZE_WITHPREFIX}.txt
# Level 4
echo "Level 4"
base64 /dev/urandom | head -c ${SIZE_WITHPREFIX} > test-4-${SIZE_WITHPREFIX}.txt
# Level 5
echo "Level 5"
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c ${SIZE_WITHPREFIX} > test-5-${SIZE_WITHPREFIX}.txt
# Level 6
echo "Level 6"
openssl rand -out test-6-${SIZE_WITHPREFIX}.txt "$(echo ${SIZE_WITHPREFIX} | numfmt --from=iec)"

