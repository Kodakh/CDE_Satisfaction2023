import time
import subprocess

def run_script():
    subprocess.run(["python", "src/scripts/extract/E0.py"])

if __name__ == "__main__":
    while True:
        run_script()
        time.sleep(86400)  # Attendre 24 heures