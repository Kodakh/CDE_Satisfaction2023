sudo chown -R jben:jben app

docker build -f src/containers/Dockerfile.extraction -t image-extraction .
docker build -f src/containers/Dockerfile.transformation -t image-transformation .