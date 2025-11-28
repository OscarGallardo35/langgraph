FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e libs/sdk-py

EXPOSE 8000

CMD ["python", "-m", "langgraph_sdk.server"]