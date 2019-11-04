#!/bin/sh
sudo mongod --fork --logpath ${1}/mongodb.log --dbpath $1 --port $2

