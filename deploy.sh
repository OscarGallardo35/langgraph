#!/bin/bash

# Build and run the container
docker-compose up --build -d

echo "LangGraph desplegado en http://localhost:8000"