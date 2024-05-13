sudo apt update
sudo apt install python3-pip
git clone https://github.com/Kodakh/CDE_Satisfaction2023
pip install -r requirements.txt
sudo groupadd docker
sudo usermod -aG docker $USER
nano ~/.bashrc
export PATH="/home/freebox/.local/bin:$PATH"
source ~/.bashrc