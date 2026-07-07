#!/bin/bash
echo "Waiting for Kafka to be ready..."
sleep 15

kafka-topics --create --if-not-exists --topic order-created --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
kafka-topics --create --if-not-exists --topic payment-confirmed --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
kafka-topics --create --if-not-exists --topic payment-failed --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
kafka-topics --create --if-not-exists --topic download-unlocked --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
kafka-topics --create --if-not-exists --topic product-created --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1

echo "Kafka topics created!"