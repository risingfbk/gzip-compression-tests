#!/bin/zsh

while [ 0 = 0 ]; do
    if pgrep gzip gunzip &>/dev/null; then
        printf "%s - gzip gunzip are running [%s]\n" "$(date)" "$(pgrep gzip gunzip | xargs ps | grep -E "(gzip|gunzip)" )"
        while pgrep gzip gunzip &>/dev/null; do
            printf "%s - " "$(date)"
            if [[ "$PLATFORM" == "mac" ]]; then
                top -l1 -s 0 | grep ^CPU | cut -f 1 -d % | rev | cut -f 1 -d ' ' | rev
            else
                top -bn1 | awk '/Cpu/ { print $2}'
            fi
        done
    else
        printf "%s - Nothing\n" "$(date)"
        sleep 0.5
    fi
done