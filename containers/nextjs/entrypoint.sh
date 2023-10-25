#!/bin/sh
cd /var/www/html
yarn install
if [ $DEBUG = "True" ]
then
    yarn dev -p 3000
else
    yarn build
    yarn start
fi
