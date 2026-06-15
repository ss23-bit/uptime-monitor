# Builder Stage
FROM python:3.14-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt

# Runtime Stage    
FROM python:3.14-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY ./app ./app

COPY alembic.ini .

COPY alembic ./alembic

COPY start.sh .

RUN chmod +x start.sh

CMD ["./start.sh"]