#!/bin/bash

function sum {
    echo $(( $1 + $2 ))
}

read -p "Enter first number: " first
read -p "Enter second number: " second

result=$(sum "$first" "$second")
echo "The sum is: $result"