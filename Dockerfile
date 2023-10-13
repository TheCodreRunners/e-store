FROM python:3.11 As development



COPY dependencies.txt ./dependencies.txt

# WORKDIR /app
COPY . .

RUN pip install -r dependencies.txt
CMD ["python", "app.py"]

FROM python:3.11-slim As production

COPY dependencies.txt ./dependencies.txt

# WORKDIR /app
COPY . .

RUN pip install -r dependencies.txt
CMD ["python", "app.py"]