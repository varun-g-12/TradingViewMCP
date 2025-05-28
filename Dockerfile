FROM python:3.12-slim-bookworm

# Build argument for development dependencies
ARG INSTALL_DEV=false

# Set working directory
WORKDIR /app

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --only main

# Copy source code
COPY src/ ./src/

# Run the MCP server
CMD ["python", "-m", "src.mcp_server.main"]