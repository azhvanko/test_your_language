FROM postgres:12.6-alpine

COPY ./init_db.sh /docker-entrypoint-initdb.d/
RUN chmod a+x /docker-entrypoint-initdb.d/init_db.sh