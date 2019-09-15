#!/bin/bash
export DB_USER="${DB_USER}"
export DB_PASSWORD="${DB_PASSWORD}"
sudo docker stop backend
sudo docker rm backend
sudo docker rmi alfaruqi26/happy-trash-backend:v1
sudo docker run --env DB_USER --env DB_PASSWORD -d -p 5000:5000 --name backend alfaruqi26/happy-trash-backend:v1