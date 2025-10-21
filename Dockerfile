FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml setup.py ./
COPY ecosystems_cli/ ./ecosystems_cli/
COPY apis/ ./apis/
COPY README.md LICENSE ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Expose MCP server (if needed for network access)
EXPOSE 8000

# Run MCP server by default
CMD ["python", "-m", "ecosystems_cli.mcp_server"]
