# Quick Setup Guide

## Prerequisites

- Docker and Docker Compose installed
- Terminal/Command line access

## 🚀 Getting Started (5 minutes)

### Step 1: Navigate to Project

```bash
cd /Users/nasheikh/Desktop/personal/python/projects/assets-manager
```

### Step 2: Create Environment File

```bash
cp .env.example .env
```

### Step 3: Build and Start

Using Make:
```bash
make build
make up
```

Or using Docker Compose directly:
```bash
docker-compose up --build -d
```

### Step 4: Access the Application

Open your browser and go to:
```
http://localhost:5000
```

### Step 5: Register Your First User

1. Click "Register" on the login page
2. Create your account
3. Start adding assets!

## 📝 Common Commands

### Using Makefile

```bash
make help        # Show all available commands
make up          # Start the application
make down        # Stop the application
make logs        # View logs
make restart     # Restart containers
make shell       # Access container shell
make clean       # Clean up everything
```

### Using Docker Compose

```bash
docker-compose up -d              # Start in background
docker-compose down               # Stop
docker-compose logs -f            # Follow logs
docker-compose exec app bash     # Access shell
docker-compose ps                 # Check status
```

## 🔧 Troubleshooting

### Port 5000 Already in Use

Edit `docker-compose.yml` and change:
```yaml
ports:
  - "8080:5000"  # Use port 8080 instead
```

### Database Issues

Reset the database:
```bash
make clean
rm -rf data/*.db
make up
```

### Permission Issues

Fix permissions:
```bash
chmod -R 755 backend/
chmod 777 data/
chmod 777 images/
```

## 🍓 Raspberry Pi Deployment

### Build for ARM

On your development machine:

```bash
# Build multi-architecture image
docker buildx create --use
docker buildx build --platform linux/arm64,linux/arm/v7 \
  -t assets-manager:raspi ./backend --load

# Save image
docker save assets-manager:raspi | gzip > assets-manager-raspi.tar.gz

# Transfer to Raspberry Pi
scp assets-manager-raspi.tar.gz pi@raspberrypi.local:/home/pi/
scp docker-compose.yml pi@raspberrypi.local:/home/pi/
scp nginx.conf pi@raspberrypi.local:/home/pi/
```

### On Raspberry Pi

```bash
# Load image
docker load < assets-manager-raspi.tar.gz

# Create directories
mkdir -p data images

# Start application
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Access on Network

Find Raspberry Pi IP:
```bash
hostname -I
```

Access from any device on the same network:
```
http://[RASPBERRY_PI_IP]
```

## 📊 Default Categories

### Physical Assets
- laptop
- mobile
- watch
- tablet
- esp32
- raspberry-pi
- camera
- other

### Digital Assets
- software
- game
- tool
- subscription

### Debt Types
- borrowed (money you borrowed from someone)
- lent (money you lent to someone)

## 🎨 Customization

### Change Secret Key

Edit `.env`:
```env
SECRET_KEY=your-super-secret-random-key-here
```

### Change Upload Limits

Edit `.env`:
```env
MAX_CONTENT_LENGTH=10485760  # 10MB
```

### Adjust Memory Limits

Edit `docker-compose.yml`:
```yaml
app:
  mem_limit: 1024m  # Increase to 1GB
```

## 📚 Next Steps

1. ✅ Register your first user
2. ✅ Add some physical assets
3. ✅ Add digital assets (games, software)
4. ✅ Track debts
5. ✅ Use search to find items quickly
6. ✅ Upload images for your physical assets

## 🆘 Need Help?

Check the main [README.md](./README.md) for detailed documentation.
