FROM python:3.10-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install \
      --no-cache-dir \
      -r requirements.txt

RUN apt-get update && \
    apt-get install -y \
      libsndfile1 \
      ffmpeg

COPY src .

EXPOSE 8888

CMD [ \
  "uvicorn", \
  "app:app", \
  "--host", "0.0.0.0", \
  "--port", "8888" \
]
