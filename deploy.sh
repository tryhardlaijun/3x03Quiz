#!/usr/bin/env sh

set -x
dcoker build -t my-python-app .
docker run -d -p 8001:8001 --name my-python-app my-python-app 
sleep 1
set +x

echo 'Now...'
echo 'Visit http://localhost to see your PHP application in action.'


