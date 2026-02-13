# SwingView Cloud IDE - Quick Start Guide

Choose your preferred setup method:

## 🚀 Option 1: Local Docker (Fastest - 30 seconds)

```bash
# Clone the repo (if you haven't already)
git clone https://github.com/Jhonlarry1010/swingview.git
cd swingview

# Start the cloud IDE
docker-compose up -d

# Open your browser
# Visit: http://localhost:8443
# Password: swingview123
```

**Done!** You now have VS Code running in your browser.

---

## 💻 Option 2: GitHub Codespaces (Easiest - No Setup)

1. Go to: https://github.com/Jhonlarry1010/swingview
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait 30 seconds for VS Code to load in browser
4. Start coding!

**Pros:** Free 60 hours/month, full VS Code, GitHub integration
**Cons:** Limited to 60 hours/month on free tier

---

## 🌐 Option 3: Cloud VPS ($3-5/month)

### DigitalOcean Setup (Recommended)

1. **Create account:** https://digitalocean.com
2. **Create Droplet:**
   - OS: Ubuntu 22.04 LTS
   - Size: $5/month (Basic)
   - Click "Create Droplet"

3. **SSH into droplet:**
   ```bash
   ssh root@YOUR_DROPLET_IP
   ```

4. **Install Docker & Deploy:**
   ```bash
   curl -fsSL https://get.docker.com | sh
   git clone https://github.com/Jhonlarry1010/swingview.git
   cd swingview
   docker-compose up -d
   ```

5. **Access IDE:**
   - Open: `http://YOUR_DROPLET_IP:8443`
   - Password: `swingview123`

### AWS EC2 Setup (Free for 12 months)

1. **Launch EC2 Instance:**
   - Type: t2.micro (free tier eligible)
   - OS: Ubuntu 22.04 LTS
   - Assign Elastic IP

2. **Security Group:** Allow ports 22, 8443, 5000

3. **SSH and run same Docker commands as DigitalOcean**

---

## 📊 Comparison

| Method | Cost | Setup Time | Always On | Best For |
|--------|------|-----------|-----------|----------|
| **Local Docker** | Free | 30 sec | While running | Testing locally |
| **Codespaces** | Free (60h/mo) | 30 sec | 24/7 | Quick development |
| **DigitalOcean** | $5/mo | 5 min | 24/7 | Production IDE |
| **AWS Free Tier** | Free (12mo) | 10 min | 24/7 | Long-term setup |

---

## What Next?

### For Local Docker:
```bash
# View logs
docker-compose logs -f code-server

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### For Cloud Deployment:
1. Change PASSWORD in docker-compose.yml to something secure
2. Set up domain + SSL (for production)
3. Configure firewall rules
4. Monitor your cloud bills

### Development Workflow:
```bash
# In terminal (inside VS Code):
cd scripts
python app.py    # Run Flask backend on port 5000

# Frontend already running on port 8080 (or configured port)

# Make changes, then:
git add .
git commit -m "Your changes"
git push origin main
```

---

## Troubleshooting

### Can't connect to localhost:8443
```bash
# Check if Docker is running
docker ps

# View logs
docker-compose logs code-server

# Restart
docker-compose restart
```

### Port already in use
```bash
# Change ports in docker-compose.yml
# From: ports: - "8443:8443"
# To:   ports: - "8080:8443"
```

### Connection issues on cloud
```bash
# SSH into your server and check:
docker-compose ps              # Check container status
docker-compose logs code-server # View error logs
sudo systemctl restart docker   # Restart Docker
```

---

## Security Tips

✅ Change default password before deploying to internet
✅ Use HTTPS with SSL certificate
✅ Restrict firewall access to your IP only
✅ Keep Docker updated
✅ Don't commit `.env` files to GitHub

---

## Need Help?

- **GitHub Issues:** https://github.com/Jhonlarry1010/swingview/issues
- **code-server Docs:** https://coder.com/docs
- **Docker Docs:** https://docs.docker.com

---

## For Vercel Users

SwingView is designed for cloud deployment:

1. **Deploy frontend to Vercel:**
   ```bash
   npm install -g vercel
   vercel
   ```

2. **Keep IDE running elsewhere:**
   - Use GitHub Codespaces for development
   - OR Deploy code-server to cheap VPS ($3-5/month)

3. **Backend API:**
   - Use Vercel Serverless Functions
   - OR Deploy Flask to same VPS as code-server

See `VERCEL_DEPLOYMENT.md` for complete setup.

---

## Your Next 5 Minutes

1. ✅ Choose one setup option above
2. ✅ Follow the installation steps
3. ✅ Open VS Code in browser
4. ✅ Open terminal in VS Code
5. ✅ Run: `python scripts/app.py`
6. ✅ Start building! 🚀

Happy coding!
