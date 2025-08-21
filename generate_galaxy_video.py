#!/usr/bin/env python3
"""
Galaxy Video Generator
Creates a beautiful animated galaxy background video for the AI chat interface.
"""

import numpy as np
import cv2
import math
import random
from pathlib import Path

class GalaxyVideoGenerator:
    def __init__(self, width=1920, height=1080, duration=30, fps=30):
        self.width = width
        self.height = height
        self.duration = duration
        self.fps = fps
        self.total_frames = duration * fps
        
        # Colors for galaxy elements
        self.star_colors = [
            (255, 255, 255),  # White
            (255, 255, 200),  # Warm white
            (200, 200, 255),  # Blue white
            (255, 200, 255),  # Pink white
            (200, 255, 255),  # Cyan white
        ]
        
        self.nebula_colors = [
            (147, 51, 234),   # Purple
            (59, 130, 246),   # Blue
            (236, 72, 153),   # Pink
            (34, 197, 94),    # Green
            (251, 146, 60),   # Orange
        ]
        
        # Generate star field
        self.stars = self._generate_stars(800)
        self.nebula_clouds = self._generate_nebula_clouds(15)
        
    def _generate_stars(self, count):
        """Generate random stars with various properties"""
        stars = []
        for _ in range(count):
            star = {
                'x': random.uniform(0, self.width),
                'y': random.uniform(0, self.height),
                'size': random.uniform(1, 4),
                'brightness': random.uniform(0.3, 1.0),
                'color': random.choice(self.star_colors),
                'twinkle_speed': random.uniform(0.01, 0.05),
                'drift_speed': random.uniform(0.1, 0.5),
                'drift_direction': random.uniform(0, 2 * math.pi)
            }
            stars.append(star)
        return stars
    
    def _generate_nebula_clouds(self, count):
        """Generate nebula clouds"""
        clouds = []
        for _ in range(count):
            cloud = {
                'x': random.uniform(-200, self.width + 200),
                'y': random.uniform(-200, self.height + 200),
                'radius': random.uniform(100, 300),
                'color': random.choice(self.nebula_colors),
                'opacity': random.uniform(0.1, 0.3),
                'drift_speed': random.uniform(0.05, 0.2),
                'drift_direction': random.uniform(0, 2 * math.pi),
                'pulse_speed': random.uniform(0.005, 0.02)
            }
            clouds.append(cloud)
        return clouds
    
    def _create_gradient_background(self, frame_num):
        """Create a gradient background"""
        # Create base gradient
        background = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create radial gradient
        center_x, center_y = self.width // 2, self.height // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                normalized_distance = distance / max_distance
                
                # Create deep space colors
                if normalized_distance < 0.3:
                    # Center - deep purple
                    r = int(40 * (1 - normalized_distance))
                    g = int(20 * (1 - normalized_distance))
                    b = int(80 * (1 - normalized_distance))
                elif normalized_distance < 0.7:
                    # Middle - dark blue
                    r = int(20 * (1 - normalized_distance))
                    g = int(30 * (1 - normalized_distance))
                    b = int(60 * (1 - normalized_distance))
                else:
                    # Outer - black
                    r = int(10 * (1 - normalized_distance))
                    g = int(10 * (1 - normalized_distance))
                    b = int(20 * (1 - normalized_distance))
                
                background[y, x] = [b, g, r]  # BGR format for OpenCV
        
        return background
    
    def _draw_nebula_clouds(self, frame, frame_num):
        """Draw animated nebula clouds"""
        overlay = frame.copy()
        
        for cloud in self.nebula_clouds:
            # Animate position
            time_factor = frame_num / self.fps
            cloud['x'] += math.cos(cloud['drift_direction']) * cloud['drift_speed']
            cloud['y'] += math.sin(cloud['drift_direction']) * cloud['drift_speed']
            
            # Wrap around screen
            if cloud['x'] > self.width + cloud['radius']:
                cloud['x'] = -cloud['radius']
            elif cloud['x'] < -cloud['radius']:
                cloud['x'] = self.width + cloud['radius']
            
            if cloud['y'] > self.height + cloud['radius']:
                cloud['y'] = -cloud['radius']
            elif cloud['y'] < -cloud['radius']:
                cloud['y'] = self.height + cloud['radius']
            
            # Animate opacity
            pulse = math.sin(time_factor * cloud['pulse_speed']) * 0.1
            current_opacity = max(0.05, cloud['opacity'] + pulse)
            
            # Draw cloud as filled circle with gradient effect
            center = (int(cloud['x']), int(cloud['y']))
            radius = int(cloud['radius'])
            color = cloud['color']
            
            cv2.circle(overlay, center, radius, color, -1)
        
        # Blend with main frame
        cv2.addWeighted(frame, 1.0, overlay, 0.3, 0, frame)
        return frame
    
    def _draw_stars(self, frame, frame_num):
        """Draw animated twinkling stars"""
        time_factor = frame_num / self.fps
        
        for star in self.stars:
            # Animate position (slow drift)
            star['x'] += math.cos(star['drift_direction']) * star['drift_speed'] * 0.1
            star['y'] += math.sin(star['drift_direction']) * star['drift_speed'] * 0.1
            
            # Wrap around screen
            if star['x'] > self.width:
                star['x'] = 0
            elif star['x'] < 0:
                star['x'] = self.width
            
            if star['y'] > self.height:
                star['y'] = 0
            elif star['y'] < 0:
                star['y'] = self.height
            
            # Twinkling effect
            twinkle = math.sin(time_factor * star['twinkle_speed']) * 0.3 + 0.7
            current_brightness = star['brightness'] * twinkle
            
            # Draw star
            pos = (int(star['x']), int(star['y']))
            color = tuple(int(c * current_brightness) for c in star['color'])
            size = int(star['size'] * (0.5 + twinkle * 0.5))
            
            # Draw star with glow effect
            cv2.circle(frame, pos, size, color, -1)
            if size > 1:
                cv2.circle(frame, pos, size + 1, tuple(c // 3 for c in color), 1)
        
        return frame
    
    def generate_video(self, output_path):
        """Generate the galaxy video"""
        print(f"Generating galaxy video: {output_path}")
        print(f"Dimensions: {self.width}x{self.height}")
        print(f"Duration: {self.duration}s at {self.fps}fps")
        print(f"Total frames: {self.total_frames}")
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        try:
            for frame_num in range(self.total_frames):
                # Create base gradient background
                frame = self._create_gradient_background(frame_num)
                
                # Add nebula clouds
                frame = self._draw_nebula_clouds(frame, frame_num)
                
                # Add stars
                frame = self._draw_stars(frame, frame_num)
                
                # Write frame
                out.write(frame)
                
                # Progress indicator
                if frame_num % 30 == 0:
                    progress = (frame_num / self.total_frames) * 100
                    print(f"Progress: {progress:.1f}%")
            
            print("✅ Galaxy video generated successfully!")
            
        except Exception as e:
            print(f"❌ Error generating video: {e}")
        finally:
            out.release()
            cv2.destroyAllWindows()

def main():
    """Main function to generate galaxy video"""
    # Set output path
    output_dir = Path("/Users/aditya/ai project/static/videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(output_dir / "galaxy.mp4")
    
    # Create generator with optimized settings for web use
    generator = GalaxyVideoGenerator(
        width=1280,      # HD width for better performance
        height=720,      # HD height for better performance  
        duration=20,     # 20 second loop
        fps=24           # 24fps for smooth animation
    )
    
    # Generate the video
    generator.generate_video(output_path)
    
    print(f"\n🌌 Galaxy video ready at: {output_path}")
    print("🚀 Your AI chat interface now has a beautiful galaxy background!")

if __name__ == "__main__":
    main()
