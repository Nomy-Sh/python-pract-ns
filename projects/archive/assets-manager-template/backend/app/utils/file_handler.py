import os
from werkzeug.utils import secure_filename
from PIL import Image
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_IMAGE_SIZE = (800, 800)  # Max dimensions for thumbnail


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file, user_id):
    """Save and optimize uploaded image"""
    if not file or not allowed_file(file.filename):
        return None

    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{user_id}_{uuid.uuid4().hex}.{ext}"

    # Get upload folder from environment or use default
    upload_folder = os.getenv('UPLOAD_FOLDER', './images')
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)

    # Open and optimize image
    try:
        img = Image.open(file)

        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background

        # Resize if too large
        img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

        # Save optimized image
        img.save(filepath, optimize=True, quality=85)

        return filename
    except Exception as e:
        print(f"Error saving image: {e}")
        return None


def delete_image(filename):
    """Delete image file"""
    if not filename:
        return

    upload_folder = os.getenv('UPLOAD_FOLDER', './images')
    filepath = os.path.join(upload_folder, filename)

    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error deleting image: {e}")
