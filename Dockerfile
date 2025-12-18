FROM postgres:18-alpine

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=watch
ENV POSTGRES_DB=justwatch

COPY justwatch_backup.sql /docker-entrypoint-initdb.d/1-schema.sql

EXPOSE 5432