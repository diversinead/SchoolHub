FROM python:3.11-slim

WORKDIR /app

COPY server.py .
COPY launcher.html .
COPY student.html .
COPY Assessments/ Assessments/
COPY Homework/ Homework/

EXPOSE 8080

CMD ["python", "server.py"]
