#!/usr/bin/env python3
"""
Test script to demonstrate the image upload functionality and PIL validation
"""

import requests
import os
from PIL import Image, ImageDraw
import io

def create_test_image():
    """Create a simple test image using PIL"""
    # Create a new RGB image
    img = Image.new('RGB', (200, 200), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    draw.text((50, 90), "Test Image", fill='darkblue')
    draw.rectangle([20, 20, 180, 180], outline='darkblue', width=3)
    
    # Save to bytes buffer
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return img_buffer

def test_upload():
    """Test the upload endpoint"""
    print("🧪 Testing Aditya AI Image Upload...")
    
    # Create test image
    test_image = create_test_image()
    
    # Test upload
    url = 'http://localhost:5001/upload_image'
    files = {'image': ('test_image.png', test_image, 'image/png')}
    
    try:
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Upload successful!")
            print(f"📄 Message: {data.get('message')}")
            if 'details' in data:
                details = data['details']
                print(f"🖼️  Image Details:")
                print(f"   - Filename: {details.get('filename')}")
                print(f"   - Size: {details.get('size')}")
                print(f"   - Format: {details.get('format')}")
                print(f"   - Mode: {details.get('mode')}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Error: {response.json().get('error', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the Flask app is running on localhost:5001")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    test_upload()
