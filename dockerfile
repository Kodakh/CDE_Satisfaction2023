FROM python:3.9

# répertoire de travail dans le conteneur
WORKDIR /app

COPY requirements.txt .
COPY SRC/main.py .

RUN pip install --no-cache-dir -r requirements.txt

# exécuter le script main.py
CMD ["python", "main.py"]