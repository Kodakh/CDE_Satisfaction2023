sudo chown -R freebox:freebox app

docker build -f src/containers/Dockerfile.extraction -t image-extraction .
docker build -f src/containers/Dockerfile.transformation -t image-transformation .
docker build -f src/containers/Dockerfile.loading -t image-loading .