# SwingView Cloud IDE - Setup Checklist

Follow this checklist to ensure your cloud development environment is properly configured.

## Pre-Setup

- [ ] GitHub account created
- [ ] Repository cloned locally or forked
- [ ] Docker/Docker Compose installed (for local testing)
- [ ] SSH client available (for cloud deployment)
- [ ] Text editor or IDE for editing configuration files

---

## Local Docker Setup

- [ ] Navigate to project directory: `cd swingview`
- [ ] Verify `docker-compose.yml` exists
- [ ] Verify `Dockerfile` exists
- [ ] Run: `docker-compose up -d`
- [ ] Wait 30-60 seconds for build to complete
- [ ] Open browser to `http://localhost:8443`
- [ ] Log in with password: `swingview123`
- [ ] Verify VS Code interface loads
- [ ] Open terminal in VS Code (Ctrl+`)
- [ ] Verify you can see project files
- [ ] Test running Flask: `cd scripts && python app.py`
- [ ] Verify no port conflicts on your machine

**Troubleshooting:**
- [ ] Check Docker is running: `docker ps`
- [ ] Check logs: `docker-compose logs code-server`
- [ ] Rebuild: `docker-compose down && docker-compose up -d --build`

---

## GitHub Codespaces Setup

- [ ] GitHub account with access to repository
- [ ] Go to: https://github.com/Jhonlarry1010/swingview
- [ ] Click **Code** button (top right)
- [ ] Click **Codespaces** tab
- [ ] Click **Create codespace on main**
- [ ] Wait for environment to build (30-90 seconds)
- [ ] Verify VS Code loads in browser
- [ ] Open terminal in Codespace
- [ ] Verify Python 3 is installed: `python --version`
- [ ] Install dependencies: `pip install -r scripts/requirements.txt`
- [ ] Test running app: `python scripts/app.py`
- [ ] Verify ports are accessible
- [ ] Check monthly hours usage (free: 60 hours/month)

**Troubleshooting:**
- [ ] Clear browser cache and retry
- [ ] Check GitHub Codespaces quota
- [ ] Verify repository has execute permissions

---

## DigitalOcean Deployment

### Account Setup
- [ ] Create DigitalOcean account: https://digitalocean.com
- [ ] Add payment method
- [ ] Enable SSH key authentication (recommended)

### Droplet Creation
- [ ] Create new Droplet
- [ ] Select OS: Ubuntu 22.04 LTS
- [ ] Select size: Basic ($5-6/month minimum)
- [ ] Select region: Closest to you
- [ ] Add SSH key (optional but recommended)
- [ ] Create Droplet
- [ ] Note Droplet IP address
- [ ] Wait for Droplet to be ready (status: green)

### Server Setup
- [ ] SSH into Droplet: `ssh root@YOUR_DROPLET_IP`
- [ ] Update packages: `apt-get update && apt-get upgrade -y`
- [ ] Install Docker: `curl -fsSL https://get.docker.com | sh`
- [ ] Add user to Docker group: `usermod -aG docker root`
- [ ] Clone repository: `git clone https://github.com/Jhonlarry1010/swingview.git`
- [ ] Navigate to directory: `cd swingview`
- [ ] Create `.env` file with secure password
- [ ] Start services: `docker-compose up -d`
- [ ] Wait for containers to build (5-10 minutes)
- [ ] Verify containers running: `docker-compose ps`

### Access & Security
- [ ] Open browser to `http://YOUR_DROPLET_IP:8443`
- [ ] Log in with your PASSWORD
- [ ] Change PASSWORD in docker-compose.yml to something strong
- [ ] Test Flask backend: Port 5000 should be accessible
- [ ] Set firewall rules (optional but recommended)
- [ ] Configure domain + SSL (for production)

### Maintenance
- [ ] Set up auto-updates: `apt-get install unattended-upgrades`
- [ ] Enable automatic Docker cleanup
- [ ] Monitor disk space: `df -h`
- [ ] Monitor memory usage: `free -h`
- [ ] Keep Docker updated: `docker-compose pull && docker-compose up -d`

---

## AWS EC2 Deployment

### Account & Instance Setup
- [ ] AWS account created: https://aws.amazon.com
- [ ] Billing alert set (optional but recommended)
- [ ] EC2 instance launched:
  - [ ] Type: t2.micro (free tier eligible)
  - [ ] OS: Ubuntu 22.04 LTS
  - [ ] Storage: 20 GB (free tier)
  - [ ] Security group created
  - [ ] Key pair generated and saved

### Security Configuration
- [ ] Security group allows port 22 (SSH)
- [ ] Security group allows port 8443 (code-server)
- [ ] Security group allows port 5000 (Flask API)
- [ ] Restrict source IPs if possible
- [ ] Elastic IP assigned for static access
- [ ] Instance tagged for cost tracking

### Server Setup
- [ ] SSH into instance using key pair
- [ ] Install Docker (same as DigitalOcean)
- [ ] Clone repository
- [ ] Start Docker Compose
- [ ] Verify services running

### Production Setup
- [ ] Configure domain name to Elastic IP
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Update docker-compose.yml for HTTPS
- [ ] Configure monitoring/alerts
- [ ] Set up backups if needed

---

## Vercel Deployment

### Frontend Deployment
- [ ] Install Vercel CLI: `npm i -g vercel`
- [ ] Connect to GitHub account
- [ ] Run: `vercel`
- [ ] Select appropriate project settings
- [ ] Deploy frontend
- [ ] Verify frontend is live at Vercel URL
- [ ] Update API endpoints to production URL

### Backend Configuration
- [ ] Choose backend hosting:
  - [ ] Option A: Vercel Serverless Functions (for simple APIs)
  - [ ] Option B: Separate VPS for Flask (for complex apps)
- [ ] Configure environment variables
- [ ] Update CORS settings
- [ ] Test API connectivity from frontend

### IDE Hosting
- [ ] Keep Codespaces for development IDE
- [ ] OR Deploy code-server to cheap VPS
- [ ] Update development documentation

---

## Project Configuration

### Environment Variables
- [ ] Create `.env` file
- [ ] Set `CODE_SERVER_PASSWORD`
- [ ] Set `FLASK_ENV`
- [ ] Set any API keys or credentials
- [ ] Add `.env` to `.gitignore`
- [ ] Never commit `.env` to GitHub

### Docker Configuration
- [ ] Review `Dockerfile` for your needs
- [ ] Review `docker-compose.yml` for your needs
- [ ] Update port mappings if needed
- [ ] Update volume mounts if needed
- [ ] Verify all dependencies are in `requirements.txt`

### Repository Settings
- [ ] Branch protection enabled (optional)
- [ ] GitHub Secrets configured for CD/CI
- [ ] Contributing guidelines updated
- [ ] README.md reflects current setup

---

## Security Hardening

### Access Control
- [ ] Change all default passwords
- [ ] Use strong, unique passwords (16+ characters)
- [ ] Enable 2FA on GitHub account
- [ ] Enable 2FA on cloud provider account
- [ ] Restrict firewall access to known IPs

### Data Protection
- [ ] HTTPS/SSL enabled in production
- [ ] `.env` file excluded from Git
- [ ] API keys stored as environment variables
- [ ] Database credentials secured (if applicable)
- [ ] Regular backups configured

### Monitoring
- [ ] Monitor resource usage (CPU, memory, disk)
- [ ] Set up alerts for high usage
- [ ] Check logs regularly for errors
- [ ] Monitor security updates
- [ ] Review access logs periodically

---

## Testing & Validation

### Local Testing
- [ ] Docker containers start without errors
- [ ] VS Code loads in browser
- [ ] File editor is responsive
- [ ] Terminal works in VS Code
- [ ] Git commands work
- [ ] Python packages install correctly
- [ ] Flask app starts without errors
- [ ] Frontend loads on port 8080 (or configured port)

### Cloud Testing
- [ ] Can connect to cloud IDE from multiple locations
- [ ] Password authentication works
- [ ] File changes persist
- [ ] Terminal commands execute
- [ ] Backend API is accessible
- [ ] Database connections work (if applicable)
- [ ] File permissions are correct

### Performance
- [ ] Page load time is acceptable (< 3 seconds)
- [ ] No console errors
- [ ] Memory usage is stable
- [ ] Disk space is not filling up
- [ ] Network latency is acceptable

---

## Documentation & Knowledge Transfer

- [ ] README.md is up to date
- [ ] CLOUD_SETUP.md reviewed
- [ ] QUICK_START.md reviewed
- [ ] VERCEL_DEPLOYMENT.md reviewed
- [ ] Team members have access documentation
- [ ] Deployment procedures documented
- [ ] Troubleshooting guide prepared
- [ ] Contact info for support documented

---

## Ongoing Maintenance

### Weekly
- [ ] Check Docker container status
- [ ] Monitor disk space
- [ ] Review error logs
- [ ] Verify backups (if applicable)

### Monthly
- [ ] Update Docker images: `docker-compose pull`
- [ ] Update system packages
- [ ] Review security alerts
- [ ] Monitor cloud provider bills
- [ ] Review and rotate credentials

### Quarterly
- [ ] Major dependency updates
- [ ] Security audit
- [ ] Performance review
- [ ] Disaster recovery test
- [ ] Documentation review

---

## Completion

- [ ] All sections above completed ✅
- [ ] Team notified of deployment
- [ ] Documentation published
- [ ] Backup verified
- [ ] Monitoring enabled
- [ ] Ready for production!

**Deployment Date:** _______________

**Deployed By:** _______________

**Notes:** 
```




```

---

## Quick Reference

### Local Docker
```bash
docker-compose up -d        # Start
docker-compose down         # Stop
docker-compose logs -f      # View logs
http://localhost:8443       # Access
```

### Cloud Deployment
```bash
ssh root@YOUR_IP                      # Connect
docker-compose ps                     # Check status
docker-compose logs code-server       # View logs
docker-compose restart code-server    # Restart
```

### Updates
```bash
git pull origin main        # Get latest code
docker-compose up -d --build  # Rebuild and restart
```

---

**Last Updated:** 2024
**Questions?** Check CLOUD_SETUP.md or create GitHub issue
