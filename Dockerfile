FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e libs/sdk-py
RUN pip install -e libs/cli
RUN pip install langgraph-api

RUN pip install langchain

RUN pip install langchain-openai

EXPOSE 8000

CMD ["langgraph", "dev", "--host", "0.0.0.0", "--port", "8000"]