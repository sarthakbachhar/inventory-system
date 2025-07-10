#!/bin/bash
set -o errexit

pip install -r requirements.txt

# Ensure static/uploads folder exists
mkdir -p static/uploads

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"
