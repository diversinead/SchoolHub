FROM python:3.11-slim

WORKDIR /app

COPY server.py .
COPY launcher.html .
COPY student.html .
COPY favicon.svg .
COPY apple-touch-icon.png .
COPY Assessments/ Assessments/
COPY Homework/ Homework/
COPY TodoLists/ TodoLists/

EXPOSE 8080

CMD ["python", "server.py"]
