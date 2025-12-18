#!/bin/bash
set -e

source env/bin/activate

if [ ! "$(docker ps -q -f name=justwatch)" ]; then
    if [ "$(docker ps -aq -f name=justwatch)" ]; then
        docker start justwatch
    else
        docker run -d \
          --name justwatch \
          -p 5433:5432 \
          -e POSTGRES_PASSWORD=password \
          -e POSTGRES_DB=justwatch \
          postgres:16
    fi
fi

until docker exec justwatch pg_isready; do
  sleep 2
done

python3 db/movie_models.py

python3 tmdb/movies_harvester.py

python3 helpers/export_ids.py

python3 helpers/find_gaps.py

python3 tmdb/movies_collector.py

docker exec justwatch pg_dump -U postgres justwatch > backup_movies.sql