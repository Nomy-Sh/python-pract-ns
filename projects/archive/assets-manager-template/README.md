# Assets Manager

A comprehensive asset tracking system for managing physical assets, digital assets, and debts. Developed for deployment on Raspberry Pi with 1GB RAM.

## Features

- **Physical Assets Management**: Track laptops, mobiles, watches, ESP32, Raspberry Pi, and other electronics
- **Digital Assets Management**: Track software licenses, PS3/PS5 games, tools, and purchased software
- **Debts Tracking**: Monitor borrowed and lent money with status updates
- **Multi-user Support**: Each user has isolated asset collections
- **Image Support**: Upload and store optimized images for physical assets
- **Search Functionality**: Quick search across all asset types
- **Responsive UI**: Lightweight and fast interface

## Tech Stack

- **Backend**: Flask (Python 3.11)
- **Database**: SQLite (file-based, perfect for Raspberry Pi)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Server**: Gunicorn with nginx reverse proxy
- **Containerization**: Docker & Docker Compose

## Project Structure

```
assets-manager/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   │   ├── user.py      # User model
│   │   │   └── asset.py     # Asset models
│   │   ├── routes/          # Route blueprints
│   │   │   ├── main.py      # Main routes
│   │   │   ├── auth.py      # Authentication
│   │   │   └── assets.py    # Asset management
│   │   ├── utils/           # Utility functions
│   │   │   └── file_handler.py
│   │   ├── templates/       # HTML templates
│   │   └── __init__.py      # App factory
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.py               # Entry point
├── data/                    # SQLite database (volume mount)
├── images/                  # Uploaded images (volume mount)
├── docker-compose.yml
├── nginx.conf
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (for version control)

### Development Setup (PC/Mac)

1. **Clone or navigate to the project**:
   ```bash
   cd assets-manager
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Open browser: http://localhost:5000
   - Register a new user account
   - Start adding assets!

### Deployment to Raspberry Pi

1. **Build for ARM architecture** (on your PC/Mac):
   ```bash
   docker buildx create --use
   docker buildx build --platform linux/arm64,linux/arm/v7 -t assets-manager:latest ./backend
   ```

2. **Transfer to Raspberry Pi**:
   ```bash
   # Option 1: Save and transfer image
   docker save assets-manager:latest | gzip > assets-manager.tar.gz
   scp assets-manager.tar.gz pi@raspberrypi:/home/pi/

   # Option 2: Use Docker Hub
   docker tag assets-manager:latest yourusername/assets-manager:latest
   docker push yourusername/assets-manager:latest
   ```

3. **On Raspberry Pi**:
   ```bash
   # Load image (if using Option 1)
   docker load < assets-manager.tar.gz

   # Or pull from Docker Hub (if using Option 2)
   docker pull yourusername/assets-manager:latest

   # Run with docker-compose
   docker-compose up -d
   ```

4. **Access on local network**:
   - Find Raspberry Pi IP: `hostname -I`
   - Access: http://[RASPBERRY_PI_IP]

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/logout` - User logout

### Physical Assets
- `GET /assets/physical` - List all physical assets
- `POST /assets/physical/add` - Add new physical asset
- `GET /assets/physical/<id>` - View asset details
- `POST /assets/physical/<id>/edit` - Edit asset
- `POST /assets/physical/<id>/delete` - Delete asset

### Digital Assets
- `GET /assets/digital` - List all digital assets
- `POST /assets/digital/add` - Add new digital asset

### Debts
- `GET /assets/debts` - List all debts
- `POST /assets/debts/add` - Add new debt record

### Search
- `GET /assets/search?q=<query>` - Search across all assets

## Database Models

### User
- username, email, password_hash
- Relationships to all asset types

### PhysicalAsset
- name, category, location, purchase_price, image_path, notes, status

### DigitalAsset
- name, category, platform, license_key, purchase_price, expiry_date, url

### Debt
- person_name, amount, type (borrowed/lent), date, due_date, status, paid_amount

## Memory Optimization for Raspberry Pi

The application is optimized for low-memory environments:

- **Gunicorn**: 2 workers, 2 threads (512MB max)
- **nginx**: Alpine-based, serves static files (128MB max)
- **Image Processing**: Automatic compression and thumbnail generation
- **Database**: SQLite with connection pooling
- **No Redis**: Keeping it minimal (can add if needed)

## Future Enhancements

- [ ] QR code generation for physical assets
- [ ] Barcode scanning support
- [ ] Export/Import functionality (CSV, JSON)
- [ ] Email notifications for debt due dates
- [ ] Reporting and analytics dashboard
- [ ] Mobile app (PWA)
- [ ] Backup and restore features

## Development

### Run without Docker (local development)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Run tests

```bash
cd backend
pytest tests/
```

## Contributing

This is a personal learning project as part of transitioning from Ruby to Python development.

## License

MIT
