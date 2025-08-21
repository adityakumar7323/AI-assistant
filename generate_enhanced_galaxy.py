#!/usr/bin/env python3
"""
Enhanced Galaxy Video Generator - Pixabay Style
Creates a stunning animated galaxy background with enhanced nebula effects.
"""

import numpy as np
import cv2
import math
import random
from pathlib import Path

class EnhancedGalaxyGenerator:
    def __init__(self, width=1920, height=1080, duration=30, fps=30):
        self.width = width
        self.height = height
        self.duration = duration
        self.fps = fps
        self.total_frames = duration * fps
        
        # Enhanced color palettes
        self.star_colors = [
            (255, 255, 255),  # Pure white
            (255, 255, 240),  # Warm white
            (240, 248, 255),  # Blue white
            (255, 240, 245),  # Pink white
            (240, 255, 255),  # Cyan white
            (255, 255, 224),  # Light yellow
        ]
        
        self.nebula_colors = [
            (138, 43, 226),   # Blue violet
            (75, 0, 130),     # Indigo
            (147, 0, 211),    # Dark violet
            (255, 20, 147),   # Deep pink
            (199, 21, 133),   # Medium violet red
            (72, 61, 139),    # Dark slate blue
            (123, 104, 238),  # Medium slate blue
            (106, 90, 205),   # Slate blue
        ]
        
        # Generate elements
        self.stars = self._generate_star_field(1200)
        self.nebula_clouds = self._generate_nebula_system(25)
        self.cosmic_dust = self._generate_cosmic_dust(50)
        
    def _generate_star_field(self, count):
        """Generate a diverse star field"""
        stars = []
        for _ in range(count):
            # Different star types
            star_type = random.choice(['normal', 'bright', 'distant', 'pulsar'])
            
            if star_type == 'bright':
                size = random.uniform(2, 5)
                brightness = random.uniform(0.8, 1.0)
            elif star_type == 'distant':
                size = random.uniform(0.5, 1.5)
                brightness = random.uniform(0.2, 0.5)
            elif star_type == 'pulsar':
                size = random.uniform(1.5, 3)
                brightness = random.uniform(0.6, 0.9)
            else:  # normal
                size = random.uniform(1, 3)
                brightness = random.uniform(0.4, 0.8)
            
            star = {
                'x': random.uniform(0, self.width),
                'y': random.uniform(0, self.height),
                'size': size,
                'brightness': brightness,
                'color': random.choice(self.star_colors),
                'type': star_type,
                'twinkle_speed': random.uniform(0.008, 0.03),
                'drift_speed': random.uniform(0.05, 0.3),
                'drift_direction': random.uniform(0, 2 * math.pi),
                'pulse_phase': random.uniform(0, 2 * math.pi)
            }
            stars.append(star)
        return stars
    
    def _generate_nebula_system(self, count):
        """Generate an interconnected nebula system"""
        clouds = []
        for i in range(count):
            # Create clusters of nebula clouds
            if i < count // 3:
                # Central cluster
                center_x = self.width * 0.5
                center_y = self.height * 0.5
                spread = min(self.width, self.height) * 0.4
            elif i < 2 * count // 3:
                # Side clusters
                center_x = random.choice([self.width * 0.2, self.width * 0.8])
                center_y = random.uniform(self.height * 0.3, self.height * 0.7)
                spread = min(self.width, self.height) * 0.3
            else:
                # Scattered clouds
                center_x = random.uniform(0, self.width)
                center_y = random.uniform(0, self.height)
                spread = min(self.width, self.height) * 0.2
            
            cloud = {
                'x': center_x + random.uniform(-spread, spread),
                'y': center_y + random.uniform(-spread, spread),
                'radius': random.uniform(80, 250),
                'color': random.choice(self.nebula_colors),
                'opacity': random.uniform(0.15, 0.4),
                'drift_speed': random.uniform(0.02, 0.1),
                'drift_direction': random.uniform(0, 2 * math.pi),
                'pulse_speed': random.uniform(0.003, 0.015),
                'pulse_phase': random.uniform(0, 2 * math.pi),
                'swirl_factor': random.uniform(0.5, 2.0)
            }
            clouds.append(cloud)
        return clouds
    
    def _generate_cosmic_dust(self, count):
        """Generate cosmic dust particles"""
        dust = []
        for _ in range(count):
            particle = {
                'x': random.uniform(-100, self.width + 100),
                'y': random.uniform(-100, self.height + 100),
                'size': random.uniform(20, 80),
                'opacity': random.uniform(0.05, 0.15),
                'drift_speed': random.uniform(0.01, 0.05),
                'drift_direction': random.uniform(0, 2 * math.pi),
                'rotation_speed': random.uniform(0.001, 0.005)
            }
            dust.append(particle)
        return dust
    
    def _create_deep_space_background(self, frame_num):
        """Create a realistic deep space background"""
        background = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create multiple gradient layers
        center_x, center_y = self.width // 2, self.height // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        # Time-based color shifting
        time_factor = frame_num / self.fps
        color_shift = math.sin(time_factor * 0.01) * 0.1
        
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                normalized_distance = distance / max_distance
                
                # Create layered space colors
                if normalized_distance < 0.2:
                    # Deep center - dark purple with slight animation
                    r = int((25 + color_shift * 10) * (1 - normalized_distance))
                    g = int((15 + color_shift * 5) * (1 - normalized_distance))
                    b = int((50 + color_shift * 15) * (1 - normalized_distance))
                elif normalized_distance < 0.5:
                    # Mid-range - cosmic blue
                    r = int((15 + color_shift * 5) * (1 - normalized_distance))
                    g = int((25 + color_shift * 8) * (1 - normalized_distance))
                    b = int((45 + color_shift * 12) * (1 - normalized_distance))
                elif normalized_distance < 0.8:
                    # Outer space - deep blue to black
                    r = int((8 + color_shift * 3) * (1 - normalized_distance))
                    g = int((12 + color_shift * 4) * (1 - normalized_distance))
                    b = int((25 + color_shift * 8) * (1 - normalized_distance))
                else:
                    # Edge - pure black
                    r = g = b = 0
                
                background[y, x] = [b, g, r]  # BGR for OpenCV
        
        return background
    
    def _draw_cosmic_dust(self, frame, frame_num):
        """Draw animated cosmic dust"""
        overlay = frame.copy()
        time_factor = frame_num / self.fps
        
        for dust in self.cosmic_dust:
            # Animate position
            dust['x'] += math.cos(dust['drift_direction']) * dust['drift_speed']
            dust['y'] += math.sin(dust['drift_direction']) * dust['drift_speed']
            
            # Wrap around
            if dust['x'] > self.width + dust['size']:
                dust['x'] = -dust['size']
            elif dust['x'] < -dust['size']:
                dust['x'] = self.width + dust['size']
            
            if dust['y'] > self.height + dust['size']:
                dust['y'] = -dust['size']
            elif dust['y'] < -dust['size']:
                dust['y'] = self.height + dust['size']
            
            # Draw dust cloud as ellipse
            center = (int(dust['x']), int(dust['y']))
            size = (int(dust['size']), int(dust['size'] * 0.7))
            rotation = int(time_factor * dust['rotation_speed'] * 180 / math.pi)
            
            # Create dust color (dark purple/blue)
            dust_color = (40, 20, 15)  # BGR
            
            cv2.ellipse(overlay, center, size, rotation, 0, 360, dust_color, -1)
        
        # Blend with main frame
        cv2.addWeighted(frame, 1.0, overlay, 0.6, 0, frame)
        return frame
    
    def _draw_enhanced_nebula(self, frame, frame_num):
        """Draw enhanced nebula clouds with swirl effects"""
        overlay = frame.copy()
        time_factor = frame_num / self.fps
        
        for cloud in self.nebula_clouds:
            # Animate position
            cloud['x'] += math.cos(cloud['drift_direction']) * cloud['drift_speed']
            cloud['y'] += math.sin(cloud['drift_direction']) * cloud['drift_speed']
            
            # Wrap around with buffer
            if cloud['x'] > self.width + cloud['radius']:
                cloud['x'] = -cloud['radius']
            elif cloud['x'] < -cloud['radius']:
                cloud['x'] = self.width + cloud['radius']
            
            if cloud['y'] > self.height + cloud['radius']:
                cloud['y'] = -cloud['radius']
            elif cloud['y'] < -cloud['radius']:
                cloud['y'] = self.height + cloud['radius']
            
            # Animate opacity with breathing effect
            pulse = math.sin(time_factor * cloud['pulse_speed'] + cloud['pulse_phase']) * 0.15
            current_opacity = max(0.05, cloud['opacity'] + pulse)
            
            # Draw main cloud
            center = (int(cloud['x']), int(cloud['y']))
            radius = int(cloud['radius'])
            
            # Create swirl effect with multiple circles
            swirl_offset = time_factor * cloud['swirl_factor'] * 0.1
            
            for i in range(3):
                offset_x = int(math.cos(swirl_offset + i * 2) * radius * 0.3)
                offset_y = int(math.sin(swirl_offset + i * 2) * radius * 0.3)
                swirl_center = (center[0] + offset_x, center[1] + offset_y)
                swirl_radius = int(radius * (0.8 - i * 0.2))
                
                cv2.circle(overlay, swirl_center, swirl_radius, cloud['color'], -1)
        
        # Blend with main frame using enhanced blending
        cv2.addWeighted(frame, 1.0, overlay, 0.4, 0, frame)
        return frame
    
    def _draw_enhanced_stars(self, frame, frame_num):
        """Draw enhanced star field with different star types"""
        time_factor = frame_num / self.fps
        
        for star in self.stars:
            # Animate position
            star['x'] += math.cos(star['drift_direction']) * star['drift_speed'] * 0.1
            star['y'] += math.sin(star['drift_direction']) * star['drift_speed'] * 0.1
            
            # Wrap around
            if star['x'] > self.width:
                star['x'] = 0
            elif star['x'] < 0:
                star['x'] = self.width
            
            if star['y'] > self.height:
                star['y'] = 0
            elif star['y'] < 0:
                star['y'] = self.height
            
            # Enhanced animation based on star type
            if star['type'] == 'pulsar':
                # Pulsing effect
                pulse = math.sin(time_factor * star['twinkle_speed'] + star['pulse_phase']) * 0.5 + 0.5
                current_brightness = star['brightness'] * (0.3 + pulse * 0.7)
            else:
                # Regular twinkling
                twinkle = math.sin(time_factor * star['twinkle_speed'] + star['pulse_phase']) * 0.4 + 0.6
                current_brightness = star['brightness'] * twinkle
            
            # Draw star with enhanced effects
            pos = (int(star['x']), int(star['y']))
            color = tuple(int(c * current_brightness) for c in star['color'])
            size = int(star['size'] * (0.5 + current_brightness * 0.5))
            
            if size > 0:
                # Main star
                cv2.circle(frame, pos, size, color, -1)
                
                # Bright stars get additional glow
                if star['type'] == 'bright' or star['brightness'] > 0.7:
                    glow_size = size + 2
                    glow_color = tuple(c // 3 for c in color)
                    cv2.circle(frame, pos, glow_size, glow_color, 1)
                    
                    # Cross pattern for brightest stars
                    if star['brightness'] > 0.8:
                        cv2.line(frame, (pos[0]-size-2, pos[1]), (pos[0]+size+2, pos[1]), glow_color, 1)
                        cv2.line(frame, (pos[0], pos[1]-size-2), (pos[0], pos[1]+size+2), glow_color, 1)
        
        return frame
    
    def generate_enhanced_video(self, output_path):
        """Generate the enhanced galaxy video"""
        print(f"🌌 Generating ENHANCED galaxy video: {output_path}")
        print(f"📐 Dimensions: {self.width}x{self.height}")
        print(f"⏱️  Duration: {self.duration}s at {self.fps}fps")
        print(f"🎬 Total frames: {self.total_frames}")
        print(f"✨ Features: Enhanced nebula, cosmic dust, diverse stars")
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        try:
            for frame_num in range(self.total_frames):
                # Create deep space background
                frame = self._create_deep_space_background(frame_num)
                
                # Add cosmic dust (bottom layer)
                frame = self._draw_cosmic_dust(frame, frame_num)
                
                # Add enhanced nebula clouds
                frame = self._draw_enhanced_nebula(frame, frame_num)
                
                # Add enhanced star field (top layer)
                frame = self._draw_enhanced_stars(frame, frame_num)
                
                # Write frame
                out.write(frame)
                
                # Progress indicator
                if frame_num % (self.fps) == 0:
                    progress = (frame_num / self.total_frames) * 100
                    print(f"🚀 Progress: {progress:.1f}%")
            
            print("✅ Enhanced galaxy video generated successfully!")
            
        except Exception as e:
            print(f"❌ Error generating enhanced video: {e}")
        finally:
            out.release()
            cv2.destroyAllWindows()

def main():
    """Generate enhanced galaxy video"""
    output_dir = Path("/Users/aditya/ai project/static/videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(output_dir / "galaxy_enhanced.mp4")
    
    # Create enhanced generator
    generator = EnhancedGalaxyGenerator(
        width=1280,      # HD width
        height=720,      # HD height
        duration=25,     # 25 second loop
        fps=24           # Smooth 24fps
    )
    
    # Generate the enhanced video
    generator.generate_enhanced_video(output_path)
    
    print(f"\n🌟 Enhanced galaxy video ready at: {output_path}")
    print("🎯 This version features:")
    print("   • Enhanced nebula with swirl effects")
    print("   • Cosmic dust particles")
    print("   • Diverse star types (normal, bright, distant, pulsar)")
    print("   • Realistic color transitions")
    print("   • Smooth animations")

if __name__ == "__main__":
    main()
