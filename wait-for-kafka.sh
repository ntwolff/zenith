#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 9092; do
  >&2 echo "Waiting for Kafka to be ready on $host..."
  sleep 1
done

>&2 echo "Kafka is ready! Executing command..."
exec $cmd