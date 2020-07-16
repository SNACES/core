#!/bin/sh
docker run --name mongodb  -v /dockerlocalstorage/data/mongodb:/data/db --hostname="dock01" -p 27017:27017 -d mongo
