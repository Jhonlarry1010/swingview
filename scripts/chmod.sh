#!/bin/bash

# Make deployment and setup scripts executable
echo "Setting executable permissions on scripts..."

chmod +x /vercel/share/v0-project/deploy.sh 2>/dev/null || true
chmod +x /vercel/share/v0-project/docker-compose.yml 2>/dev/null || true

# Make Python scripts executable
chmod +x /vercel/share/v0-project/scripts/app.py 2>/dev/null || true
chmod +x /vercel/share/v0-project/scripts/auth_service.py 2>/dev/null || true
chmod +x /vercel/share/v0-project/scripts/crypto_analyzer.py 2>/dev/null || true

echo "✓ All scripts are now executable"
echo ""
echo "Next steps:"
echo "1. Local development: docker-compose up -d"
echo "2. Access VS Code: http://localhost:8443"
echo "3. For cloud deployment, see CLOUD_SETUP.md"
