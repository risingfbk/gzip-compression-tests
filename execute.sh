#!/bin/zsh

SIZE=$1

if [[ -z $SIZE ]]; then
    echo "Usage: $0 <size>"
    exit 1
fi

if [[ -n $CACHE && "$CACHE" == 1 ]]; then
    echo "gz caching is enabled"
else
  echo "gz caching is disabled, files will be destroyed after each test"
fi

echo "Platform: $PLATFORM"
if [[ -z "$PLATFORM" || "$PLATFORM" != "mac" ]]; then
  field=2
  opts="-p"
  echo "Using Linux opts"
else
  field=1
  opts=""
fi

TEST_DIR=files

levels=(1 2 4 5 6 11 14 15 16 20)
#for level in {10..25}; do
for level in ${levels}; do
    echo "Level ${level} ----"
    unzipped=$(du -h ${TEST_DIR}/test-${level}-${SIZE}.txt | cut -f1)
    for gziplevel in {1..9}; do
        echo "Gzip level ${gziplevel} ----"
        if [[ ! -f ${TEST_DIR}/test-${level}-${gziplevel}-${SIZE}.txt.gz ]]; then
          ziptime=$(/usr/bin/time $opts gzip --keep -c -${gziplevel} ${TEST_DIR}/test-${level}-${SIZE}.txt >${TEST_DIR}/test-${level}-${gziplevel}-${SIZE}.txt.gz 2> >(grep real | sed -E "s/^ +//g" | cut -f $field -d " "))
          zipped=$(du -h ${TEST_DIR}/test-${level}-${gziplevel}-${SIZE}.txt.gz | cut -f1)
        else
          ziptime=""
          zipped=""
        fi
        unziptime=$(/usr/bin/time $opts gunzip -k -f ${TEST_DIR}/test-${level}-${gziplevel}-${SIZE}.txt.gz 2>&1 | grep real | sed -E "s/^ +//g" | cut -f $field -d " ")
        rm -rf ${TEST_DIR}/test-${level}-${gziplevel}-${SIZE}.txt
        if [[ -z "$CACHE" || "$CACHE" != 1 ]]; then
          rm -rf ${TEST_DIR}/test-${level}-${gziplevel}-${SIZE}.txt.gz
        fi
        echo "Unzipped: ${unzipped} -> Ziptime: ${ziptime} -> Zipped: ${zipped} -> Unziptime: ${unziptime}"
        printf "${level},${gziplevel},${unzipped},${ziptime},${zipped},${unziptime}\n" >> results.csv
    done
done
