import React, { useEffect, useRef } from 'react';

const GalaxyBackground = ({ children, useVideo = false }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  useEffect(() => {
    if (useVideo) return; // Skip canvas animation if using video

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let stars = [];

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    // Create stars
    const createStars = (count = 200) => {
      stars = [];
      for (let i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 2 + 0.5,
          opacity: Math.random() * 0.8 + 0.2,
          twinkleSpeed: Math.random() * 0.02 + 0.01,
          twinkleDirection: Math.random() > 0.5 ? 1 : -1,
          color: getStarColor(),
        });
      }
    };

    // Get random star color (white, blue, purple hues)
    const getStarColor = () => {
      const colors = [
        'rgba(255, 255, 255,', // White
        'rgba(173, 216, 230,', // Light blue
        'rgba(221, 160, 221,', // Plum
        'rgba(255, 182, 193,', // Light pink
        'rgba(135, 206, 235,', // Sky blue
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    };

    // Animate stars
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw galaxy background gradient
      const gradient = ctx.createRadialGradient(
        canvas.width / 2, canvas.height / 2, 0,
        canvas.width / 2, canvas.height / 2, Math.max(canvas.width, canvas.height) / 2
      );
      gradient.addColorStop(0, 'rgba(25, 25, 112, 0.3)'); // Dark blue center
      gradient.addColorStop(0.3, 'rgba(72, 61, 139, 0.2)'); // Dark slate blue
      gradient.addColorStop(0.6, 'rgba(0, 0, 0, 0.4)'); // Black
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0.8)'); // Darker black

      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw and animate stars
      stars.forEach(star => {
        // Update twinkle
        star.opacity += star.twinkleSpeed * star.twinkleDirection;
        if (star.opacity <= 0.1 || star.opacity >= 1) {
          star.twinkleDirection *= -1;
        }

        // Draw star
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = star.color + star.opacity + ')';
        ctx.fill();

        // Add glow effect for brighter stars
        if (star.opacity > 0.7) {
          ctx.beginPath();
          ctx.arc(star.x, star.y, star.radius * 2, 0, Math.PI * 2);
          ctx.fillStyle = star.color + (star.opacity * 0.3) + ')';
          ctx.fill();
        }
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    // Initialize
    resizeCanvas();
    createStars();
    animate();

    // Handle resize
    const handleResize = () => {
      resizeCanvas();
      createStars();
    };

    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      window.removeEventListener('resize', handleResize);
    };
  }, [useVideo]);

  return (
    <div className="relative h-screen w-screen overflow-hidden bg-black">
      {/* Video Background Option */}
      {useVideo && (
        <video
          className="absolute inset-0 w-full h-full object-cover z-0"
          autoPlay
          loop
          muted
          playsInline
          poster="/public/images/galaxy-poster.jpg"
        >
          <source src="/public/videos/galaxy.mp4" type="video/mp4" />
          {/* Fallback to canvas if video fails */}
          <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-blue-900 to-black"></div>
        </video>
      )}

      {/* Canvas Background Option */}
      {!useVideo && (
        <canvas
          ref={canvasRef}
          className="absolute inset-0 z-0"
          style={{ background: 'radial-gradient(ellipse at center, #1a1a2e 0%, #16213e 25%, #000 70%)' }}
        />
      )}

      {/* CSS Fallback Stars (for low-performance devices) */}
      <div className="absolute inset-0 z-0">
        {/* Static CSS stars as fallback */}
        <div className="absolute top-1/4 left-1/4 w-1 h-1 bg-white rounded-full opacity-60 animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-0.5 h-0.5 bg-blue-200 rounded-full opacity-40 animate-ping"></div>
        <div className="absolute bottom-1/4 left-1/3 w-1.5 h-1.5 bg-purple-200 rounded-full opacity-70 animate-pulse"></div>
        <div className="absolute top-1/2 right-1/3 w-0.5 h-0.5 bg-white rounded-full opacity-50 animate-ping"></div>
        <div className="absolute bottom-1/3 right-1/2 w-1 h-1 bg-pink-200 rounded-full opacity-60 animate-pulse"></div>
      </div>

      {/* Semi-transparent overlay for readability */}
      <div className="absolute inset-0 bg-black/60 z-5"></div>

      {/* Chat UI Content */}
      <div className="relative z-10 h-full w-full">
        {children}
      </div>
    </div>
  );
};

export default GalaxyBackground;
