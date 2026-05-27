# SwingView Cloud Development Environment Setup

This guide helps you set up a cloud-based IDE (code-server) for SwingView development.

## Option 1: Local Docker Setup (Recommended for testing)

### Prerequisites
- Docker and Docker Compose installed on your machine
- Git

### Quick Start

1. **Clone and navigate to the project:**
   ```bash
   git clone https://github.com/Jhonlarry1010/swingview.git
   cd swingview
   ```

2. **Start the cloud IDE:**
   ```bash
   docker-compose up -d
   ```

3. **Access VS Code in your browser:**
   - Open: `http://localhost:8443`
   - Password: `swingview123` (change in docker-compose.yml)

4. **Stop the services:**
   ```bash
   docker-compose down
   ```

---

## Option 2: Deploy to DigitalOcean (Cloud Hosting)

### Prerequisites
- DigitalOcean account
- Docker and Docker Compose installed locally
- SSH client

### Setup Steps

1. **Create a Droplet:**
   - Size: Basic ($5-6/month minimum)
   - OS: Ubuntu 22.04 LTS
   - Region: Your closest region

2. **SSH into your droplet:**
   ```bash
   ssh root@YOUR_DROPLET_IP
   ```

3. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

4. **Clone your repository:**
   ```bash
   git clone https://github.com/Jhonlarry1010/swingview.git
   cd swingview
   ```

5. **Create environment file:**
   ```bash
   echo "CODE_SERVER_PASSWORD=your_secure_password_here" > .env
   ```

6. **Start services:**
   ```bash
   docker-compose up -d
   ```

7. **Access your cloud IDE:**
   - Visit: `http://YOUR_DROPLET_IP:8443`
   - Login with your password

8. **Setup SSL (optional but recommended):**
   ```bash
   # Install certbot
   sudo apt-get install certbot
   
   # Get a free SSL certificate
   sudo certbot certonly --standalone -d yourdomain.com
   ```

---

## Option 3: Deploy to Railway.app (Easiest)

Railway provides free tier and one-click deployments.

1. **Sign up at [Railway.app](https://railway.app)**

2. **Connect your GitHub repository:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize and select `swingview`

3. **Add environment variable:**
   - `CODE_SERVER_PASSWORD` = your secure password

4. **Configure Dockerfile:**
   - Railway will auto-detect `Dockerfile`

5. **Deploy:**
   - Click "Deploy" and wait for build completion

6. **Access your IDE:**
   - Open the Railway-provided domain
   - Append `:8443` if needed

---

## Option 4: Deploy to AWS EC2 (Production-Ready)

### Prerequisites
- AWS account
- EC2 instance running Ubuntu 22.04

### Steps
1. Launch EC2 instance (t2.micro eligible for free tier)
2. SSH into instance
3. Follow DigitalOcean steps (same process)
4. Use Elastic IP for static access
5. Configure Security Groups to allow ports 8443 and 5000

---

## Troubleshooting

### Can't access code-server on localhost:8443
```bash
# Check if containers are running
docker-compose ps

# View logs
docker-compose logs code-server

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### API not connecting
```bash
# Verify API is running
docker-compose ps api

# Check Python dependencies
docker-compose logs api

# Rebuild API service
docker-compose up -d --build api
```

### Permission denied errors
```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
newgrp docker
```

---

## Development Workflow

Once your cloud IDE is running:

1. **Open Terminal in VS Code**
   - Already in `/home/coder/project`

2. **Run your Flask app:**
   ```bash
   cd scripts
   python app.py
   ```

3. **Access your app:**
   - Frontend: `http://localhost:5000` (via terminal port forward)
   - Or use the built-in port forwarding in code-server

4. **Install packages:**
   - Open terminal: `pip install <package_name>`

5. **Commit and push changes:**
   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```

---

## Security Best Practices

1. **Change default password** in docker-compose.yml or .env
2. **Use HTTPS** with a domain and SSL certificate
3. **Limit network access** - only allow your IP
4. **Keep Docker updated**: `docker-compose pull && docker-compose up -d`
5. **Use `.env` file** for sensitive data (add to .gitignore)

---

## Next Steps

- Customize Python dependencies in `scripts/requirements.txt`
- Add database support (PostgreSQL, MongoDB)
- Set up GitHub Actions for automated testing
- Configure continuous deployment

For questions, check the [code-server documentation](https://coder.com/docs).
