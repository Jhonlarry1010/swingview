FROM codercom/code-server:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install Flask Flask-CORS python-dotenv cryptography requests pandas numpy

# Copy project files
COPY . /home/coder/project

# Set working directory
WORKDIR /home/coder/project

# Expose ports
EXPOSE 8443 5000

# Set code-server password via environment variable
ENV PASSWORD=${CODE_SERVER_PASSWORD:-swingview}

# Start code-server
CMD ["code-server", "--bind-addr", "0.0.0.0:8443", "/home/coder/project"]
