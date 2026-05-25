FROM postgres:17

# Install PostGIS packages for PostgreSQL 17
RUN apt-get update && apt-get install -y --no-install-recommends \
      postgis \
      postgresql-17-postgis-3 \
    && rm -rf /var/lib/apt/lists/*

# Copy initialization SQL scripts (extensions, schemas, tables)
COPY init-db/ /docker-entrypoint-initdb.d/