sudo apt update
sudo apt install python3-pip

pip install -r requirements.txt
sudo groupadd docker
sudo usermod -aG docker $USER

docker build -f src/containers/Dockerfile.extraction -t image-extraction .
docker build -f src/containers/Dockerfile.loading -t image-loading .
docker build -f src/containers/Dockerfile.archive -t image-archive .
docker build -f src/containers/Dockerfile.transformation -t image-transformation .

# Debugging
# docker-compose up --no-deps --build transformation
# sudo chown -R freebox:freebox app
# Alias Kibana
#POST /_aliases
#{
#  "actions": [
#    {
#      "add": {
#        "index": "reviews_*",
#        "alias": "areviews"
#      }
#    }
#  ]
#}