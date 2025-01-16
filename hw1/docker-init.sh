#!/bin/bash

echo "Clearing data"
rm -rf /var/lib/postgresql/data/*
rm -rf /var/lib/postgresql/data-slave/*
echo "Starting postgres_master node..."
docker-compose up -d postgres_master

echo "Wait for postgres_master to be ready..."
sleep 10  # Waits for master node start complete

echo "Prepare replica config..."
docker exec -it postgres_master sh /etc/postgresql/init-script/init.sh
echo "Restart master node"
docker-compose restart postgres_master
sleep 10

echo "Starting slave node..."
docker-compose up -d postgres_slave
sleep 10  # Waits for node start complete

echo "Done"
