#!/bin/bash
echo "Waiting for Kafka to be ready..."
sleep 10

kafka-topics --create --if-not-exists --topic order-created --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
kafka-topics --create --if-not-exists --topic payment-confirmed --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
kafka-topics --create --if-not-exists --topic payment-failed --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
kafka-topics --create --if-not-exists --topic download-unlocked --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
kafka-topics --create --if-not-exists --topic product-created --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

echo "Kafka topics created!"