#!/bin/bash

# SwingView Cloud Deployment Script
# This script helps deploy code-server to various cloud platforms

set -e

echo "🚀 SwingView Cloud Deployment Helper"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check for Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

print_success "Docker found"

# Get deployment target
echo ""
echo "Select deployment target:"
echo "1) Local Docker (localhost:8443)"
echo "2) DigitalOcean Droplet"
echo "3) AWS EC2"
echo "4) Custom VPS"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        print_info "Starting local Docker deployment..."
        
        # Generate random password if not set
        if [ -z "$CODE_SERVER_PASSWORD" ]; then
            PASSWORD=$(openssl rand -base64 12)
            export CODE_SERVER_PASSWORD=$PASSWORD
            print_info "Generated password: $PASSWORD"
            print_info "Set CODE_SERVER_PASSWORD environment variable to change it"
        fi
        
        docker-compose down 2>/dev/null || true
        docker-compose up -d --build
        
        print_success "Code-server is running!"
        print_info "Access at: http://localhost:8443"
        print_info "Password: $CODE_SERVER_PASSWORD"
        ;;
        
    2)
        print_info "DigitalOcean deployment instructions:"
        echo ""
        echo "1. Create a new Droplet at https://cloud.digitalocean.com"
        echo "2. Choose Ubuntu 22.04 LTS"
        echo "3. SSH into your droplet: ssh root@YOUR_DROPLET_IP"
        echo "4. Run these commands:"
        echo ""
        echo "   curl -fsSL https://get.docker.com -o get-docker.sh"
        echo "   sudo sh get-docker.sh"
        echo "   sudo usermod -aG docker \$USER"
        echo "   git clone https://github.com/Jhonlarry1010/swingview.git"
        echo "   cd swingview"
        echo "   docker-compose up -d"
        echo ""
        echo "5. Access at: http://YOUR_DROPLET_IP:8443"
        ;;
        
    3)
        print_info "AWS EC2 deployment instructions:"
        echo ""
        echo "1. Launch an EC2 instance (t2.micro - eligible for free tier)"
        echo "2. OS: Ubuntu 22.04 LTS"
        echo "3. SSH into your instance"
        echo "4. Run the DigitalOcean commands above"
        echo ""
        echo "5. Assign an Elastic IP for static access"
        echo "6. Configure Security Groups to allow ports 8443, 5000, 22"
        ;;
        
    4)
        read -p "Enter your VPS IP address: " vps_ip
        print_info "Instructions for custom VPS:"
        echo ""
        echo "1. SSH into your VPS: ssh user@$vps_ip"
        echo "2. Install Docker and Docker Compose"
        echo "3. Clone the repository: git clone https://github.com/Jhonlarry1010/swingview.git"
        echo "4. Navigate to directory: cd swingview"
        echo "5. Create .env file: echo 'CODE_SERVER_PASSWORD=your_password' > .env"
        echo "6. Start services: docker-compose up -d"
        echo ""
        echo "7. Access at: http://$vps_ip:8443"
        ;;
        
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
print_success "Deployment setup complete!"
echo ""
echo "For more details, see CLOUD_SETUP.md"
