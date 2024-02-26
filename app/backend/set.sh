#!/bin/bash

# Set environment variables
# feel free to change the values to match your local environment

export DB_HOST="localhost"
export DB_USER="root"
export DB_PASSWORD="root"
export DB_NAME="todo_db"

#dont try to hack me, this is just a simple example xD


# Create the database schema
TABLE_CREATION_SQL="CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  is_complete BOOLEAN DEFAULT false
);"

# Run the SQL statement to create the table
echo "$TABLE_CREATION_SQL" | mysql -u"$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" "$DB_NAME"

# Run Python application
python app.py
