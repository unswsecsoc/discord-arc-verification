#!/bin/sh

set -e

DBNAME="arc_verification"
DBUSER="postgres"
DBPASS="postgres"
DBHOST="172.17.0.2"

execute_root_query() {
    echo "$1" | PGPASSWORD="$DBPASS" psql -A -t -h "$DBHOST" -U "$DBUSER" postgres
}

execute_db_query() {
    echo "$1" | PGPASSWORD="$DBPASS" psql -A -t -h "$DBHOST" -U "$DBUSER" "$DBNAME"
}

while ! execute_root_query "SELECT 1;"; do
    echo "Waiting for postgres to come online..."
    sleep 1
done

if [ -z $(execute_root_query "select datname from pg_database" | egrep '^'$DBNAME'$') ]
then
    echo "Creating tables for migration"
    execute_root_query "CREATE DATABASE $DBNAME;"
    execute_db_query "CREATE TABLE migrations(version VARCHAR(32) PRIMARY KEY NOT NULL);"
fi

# Get last migration
last=`execute_db_query "SELECT version FROM migrations ORDER BY version DESC LIMIT 1"`
echo "$last"
if [ -z $last ]
then
    last="0"
fi


for i in `dirname "$(readlink -f "$0")"`/../sql/up-*.sql
do
    name=$(basename "$i" | sed -e 's/\.sql$//g')
    if [ "$last" \<  "$name" ]
    then
        echo "Applying migration $name."
        tmpf=`mktemp`
        echo "BEGIN;" >> "$tmpf"
        cat "$i" >> "$tmpf"
        echo "INSERT INTO migrations (version) VALUES ('$name'); COMMIT;" >> "$tmpf"
        PGPASSWORD="$DBPASS" psql -A -t -h "$DBHOST" -U "$DBUSER" "$DBNAME" < "$tmpf"
        rm "$tmpf"
    fi
done

newest=$name

if [ "$newest" \> "$last" ]
then
    echo "Schema has been upgraded to $newest."
else
    echo "Schema is already up to date."
fi

