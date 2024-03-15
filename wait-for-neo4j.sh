#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until curl -s "$host":7474/db/data/ > /dev/null; do
  >&2 echo "Waiting for Neo4j to be ready on $host..."
  sleep 2
done

>&2 echo "Neo4j is ready! Executing command..."
exec $cmd