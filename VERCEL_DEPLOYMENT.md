# SwingView Cloud IDE on Vercel

This guide explains how to integrate the SwingView project with Vercel's cloud development platform.

## Important Note

**code-server cannot run directly on Vercel** because Vercel is a serverless platform designed for frontend apps and serverless functions, not persistent long-running servers.

## Recommended Approach: Hybrid Setup

### Part 1: Deploy SwingView Frontend to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Link your project:**
   ```bash
   vercel link
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

Your frontend will be live at a Vercel URL.

### Part 2: Run code-server Elsewhere

Since code-server needs a persistent server, choose one of these options:

#### Option A: GitHub Codespaces (Recommended - Free tier)
- Native VS Code in browser
- Integrated with your GitHub repo
- No additional setup needed
- Free tier: 60 hours/month

1. Go to your GitHub repo
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Start coding in browser-based VS Code

#### Option B: Replit
- Simple web-based IDE
- Free tier available
- Great for collaborative development

1. Visit https://replit.com
2. Click **Create** → **Import from GitHub**
3. Select your SwingView repo
4. Start development

#### Option C: Self-Hosted on Affordable VPS

Deploy code-server to a cheap VPS ($3-5/month):

1. **DigitalOcean ($5/month):**
   ```bash
   # SSH into your droplet
   ssh root@YOUR_DROPLET_IP
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Clone and run
   git clone https://github.com/Jhonlarry1010/swingview.git
   cd swingview
   docker-compose up -d
   ```

2. **Linode ($5/month):** Same steps as DigitalOcean

3. **Hetzner ($3/month):** Same Docker steps

Access your IDE at `http://YOUR_VPS_IP:8443`

#### Option D: AWS EC2 Free Tier
- Free for 12 months (t2.micro)
- Requires AWS account setup
- Follow DigitalOcean steps above

## Recommended Setup Summary

| Component | Where | Why |
|-----------|-------|-----|
| Frontend (HTML/CSS/JS) | Vercel | Fast, serverless, auto-scaling |
| Backend API (Flask) | Vercel Functions OR VPS | Vercel: simple; VPS: more control |
| Development IDE | GitHub Codespaces or Cheap VPS | Persistent environment for coding |

## Step-by-Step Hybrid Deployment

### Step 1: Prepare Frontend for Vercel

Your project is static HTML/CSS/JS, so it works perfectly on Vercel:

```bash
vercel
```

### Step 2: Set Up Development Environment

**Choose one:**

**A) GitHub Codespaces (Easiest):**
```bash
# In GitHub, click Code → Codespaces → Create codespace
# Terminal opens in browser with full environment
cd swingview
docker-compose up
# Access IDE at http://localhost:8443
```

**B) Self-Hosted VPS:**
```bash
# On your VPS:
curl -fsSL https://get.docker.com | sh
git clone https://github.com/Jhonlarry1010/swingview.git
cd swingview
docker-compose up -d
# Access IDE at http://YOUR_VPS_IP:8443
```

### Step 3: Connect Frontend to Backend

Update your API endpoints in `assets/js/global.js`:

```javascript
// For production (on Vercel)
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-vercel-domain.com/api'
  : 'http://localhost:5000';
```

### Step 4: Deploy Backend API

**Option A: Vercel Serverless Functions**

Create `/api/price.js`:
```javascript
import { PythonShell } from 'python-shell';

export default async (req, res) => {
  // Run Flask endpoint
  const result = await fetch('http://localhost:5000/api/price');
  const data = await result.json();
  res.status(200).json(data);
};
```

**Option B: Self-Hosted Flask on VPS**

Update docker-compose to expose port 5000:
```yaml
services:
  api:
    ports:
      - "5000:5000"
```

Access at `http://YOUR_VPS_IP:5000`

## Environment Variables

Create `.env` file:
```
CODE_SERVER_PASSWORD=your_secure_password
FLASK_ENV=production
API_URL=https://your-vercel-domain.com/api
```

## Security Checklist

- [ ] Change CODE_SERVER_PASSWORD to something strong
- [ ] Use HTTPS (SSL certificate for custom domain)
- [ ] Set firewall rules on VPS (allow only your IP to port 8443)
- [ ] Keep Docker images updated
- [ ] Don't commit `.env` to GitHub
- [ ] Use GitHub Secrets for sensitive data

## Cost Breakdown

| Service | Cost | Purpose |
|---------|------|---------|
| Vercel Frontend | Free | Host static site & API |
| GitHub Codespaces | Free (60hrs/mo) | Development IDE |
| Optional VPS | $3-5/month | Self-hosted code-server |
| **Total** | **Free or $3-5/month** | **Full stack development** |

## Next Steps

1. Deploy frontend to Vercel: `vercel`
2. Set up development IDE (Codespaces recommended)
3. Update API endpoints in your code
4. Push changes to GitHub
5. Monitor at https://vercel.com/dashboard

For full cloud IDE setup, see `CLOUD_SETUP.md`.
