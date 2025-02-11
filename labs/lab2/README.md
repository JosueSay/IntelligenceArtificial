# Lab 2


## Ejecutar en docker

´´´sh
docker buildx build -t ia_lab2 .    
docker run --rm -v "$(pwd)/images:/app/images" -v "$(pwd)/areas.csv:/app/areas.csv" ia_lab2 
´´´
