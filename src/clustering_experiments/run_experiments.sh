#!/bin/bash

while getopts n:f: option
do
    case "${option}" in
        n) number_of_experiments=${OPTARG};;
        f) file=${OPTARG};;
    esac
done

for ((i = 0; i < $number_of_experiments; i++));
do
    python ./src/clustering_experiments/$file
done
