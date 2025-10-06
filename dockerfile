FROM python:3.11-slim

WORKDIR /tts

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "tts.main:app", "--host", "0.0.0.0", "--port", "8000"]
