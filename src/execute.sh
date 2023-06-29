#!/bin/zsh

# Oh, look at this script, how it does zip! With levels and sizes, it's quite a trip!
# We check the size, to make sure it's there, And if it's not, we give a scare!
# We check the cache, to see if it's on, And if it is, we sing a song!
# We check the platform, to see what's what, And if it's Mac, we do one thing, but not!
# We loop through the levels, from one to six, And eleven, fourteen, fifteen, sixteen, and twenty, oh what a mix!
# We loop through the gzip levels, from one to nine, And for each one, we do a test, oh so fine!
# We check if the file exists, before we zip, And if it does, we give it a skip!
# We time the zip, and we time the unzip, And we write the results, with a little quip!
# And finally, we clean up the mess, With a little rm, oh what a success!
# So run this script, and see what it does, With zips and unzips, it's sure to buzz!

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

levels=(13 14 15 16 17 18 19 20 21 22 23 24 25)
# levels=(1 2 4 5 6 13 14 15 16 20)
# levels=(1 2 3 4 5 6)
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
