FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.10.12-slim-buster


# Install system dependencies for pyodbc
# Install Microsoft ODBC Driver for SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    curl \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /scheduling
COPY . /scheduling
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
