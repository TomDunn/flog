#!/bin/bash

tests=("models.tests.Author")

for t in "${tests[@]}"
do
    echo $t
    python -m unittest $t
done
