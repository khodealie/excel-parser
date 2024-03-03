#!/bin/bash

# Prompt for database details
read -sp 'Enter the database root password: ' DB_ROOT_PASSWORD
echo
read -p 'Enter your database name: ' DB_NAME
read -p 'Enter your database user: ' DB_USER
read -sp 'Enter your database user password: ' DB_PASSWORD
echo

# Create .env file with environment variables
cat << EOF > .env
DB_ROOT_PASSWORD=$DB_ROOT_PASSWORD
DB_ENGINE=django.db.backends.mysql
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=excel_parser_database
DB_PORT=3306
REDIS_HOST=excel_parser_redis
REDIS_PORT=6379
EOF

# Run Docker Compose
docker-compose up -d
