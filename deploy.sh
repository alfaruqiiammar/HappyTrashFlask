#!/bin/bash
sudo docker stop backend
sudo docker rm backend
sudo docker rmi alfaruqi26/happy-trash-backend:v1
sudo docker run -d -p 5000:5000 --name backend alfaruqi26/happy-trash-backend:v1