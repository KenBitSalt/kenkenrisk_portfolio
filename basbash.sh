#!/bin/bash

echo "FAIL count: $(grep "FAIL" log.txt | wc -l)"
echo "FAIL users:"
grep "FAIL" log.txt | awk '{print $3}' | sort | uniq -c | sort -nr

echo "All users:"
awk '{print $3}' log.txt | sort | uniq

echo "Login success times:"
grep "login SUCCESS" log.txt | awk '{print $1}'

echo "Top SUCCESS user:"
grep "login SUCCESS" log.txt | awk '{print $3}' | sort | uniq -c | sort -nr | head -n 1
