#!/usr/bin/env bash
set -e

echo "Starting Docker services..."
cd docker
docker compose up -d

echo "Installing Python dependencies..."
cd ../ 
source .venv3.10/bin/activate 

pip install -r requirements.txt

echo "Fixing cryptography / GLIBC issue..."
pip uninstall cryptography -y
pip install "cryptography<42"

#echo "Setting HuggingFace cache..."
#export HF_HOME=~/cache

echo "Initializing MongoDB..."
docker exec -i csab-mongo-1 mongosh -u admin -p admin123 <<EOF
use CSAB_DB
db.ADMIN.insertOne({Role: "admin", Name: "eslam", Password: "eslam"})
EOF

echo "Starting FastAPI app..."
cd src
uvicorn main:app --host 0.0.0.0 --port 5000
