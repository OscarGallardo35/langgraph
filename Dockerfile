FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e libs/sdk-py
RUN pip install -e libs/cli

EXPOSE 8000

CMD ["langgraph", "dev"]