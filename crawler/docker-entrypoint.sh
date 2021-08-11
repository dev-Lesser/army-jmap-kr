#!/bin/bash

dockerize -wait tcp://maria_db:3306 -timeout 20s

# # Apply database migrations
# echo "Apply database migrations"  
# make migrate

# Start cralwer
echo "Start crawler"  
python3 main.py