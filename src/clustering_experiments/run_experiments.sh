#!/bin/bash

while getopts n: option
do
    case "${option}" in
        n) number_of_experiments=${OPTARG};;
    esac
done

for ((i = 0; i < $number_of_experiments; i++));
do
    python ./src/clustering_experiments/compare_clustering_algorithms.py
done
