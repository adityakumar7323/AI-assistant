import React, { useState, useEffect } from 'react';

const GalaxyBackgroundCSS = ({ children, enableAdvancedEffects = true }) => {
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    // Check for reduced motion preference
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mediaQuery.matches);

    const handleChange = (e) => setReducedMotion(e.matches);
    mediaQuery.addEventListener('change', handleChange);

    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  // Generate random floating particles
  const generateParticles = (count = 8) => {
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      size: Math.random() * 4 + 2,
      left: Math.random() * 100,
      animationDelay: Math.random() * 15,
      animationDuration: Math.random() * 10 + 15,
    }));
  };

  const particles = generateParticles();

  return (
    <div className="relative h-screen w-screen overflow-hidden">
      {/* Main Galaxy Background */}
      <div className="absolute inset-0 galaxy-starfield"></div>

      {/* Nebula Clouds Layer */}
      {enableAdvancedEffects && !reducedMotion && (
        <div className="absolute inset-0 nebula-cloud opacity-60"></div>
      )}

      {/* Galaxy Spiral Effect */}
      {enableAdvancedEffects && !reducedMotion && (
        <div className="absolute inset-0 galaxy-spiral opacity-40"></div>
      )}

      {/* CSS Animated Stars */}
      <div className="absolute inset-0">
        {/* Large twinkling stars */}
        <div className="absolute top-[15%] left-[20%] w-2 h-2 bg-white rounded-full star-twinkle-1"></div>
        <div className="absolute top-[25%] right-[15%] w-1.5 h-1.5 bg-blue-200 rounded-full star-twinkle-2"></div>
        <div className="absolute bottom-[30%] left-[10%] w-3 h-3 bg-purple-200 rounded-full star-twinkle-3"></div>
        <div className="absolute top-[45%] right-[25%] w-1 h-1 bg-pink-200 rounded-full star-twinkle-4"></div>
        <div className="absolute bottom-[20%] right-[35%] w-2 h-2 bg-cyan-200 rounded-full star-twinkle-5"></div>
        <div className="absolute top-[60%] left-[30%] w-1.5 h-1.5 bg-white rounded-full star-twinkle-1"></div>
        <div className="absolute top-[35%] left-[60%] w-1 h-1 bg-blue-300 rounded-full star-twinkle-2"></div>
        <div className="absolute bottom-[45%] right-[20%] w-2.5 h-2.5 bg-purple-300 rounded-full star-twinkle-3"></div>
        <div className="absolute top-[70%] right-[45%] w-1 h-1 bg-pink-300 rounded-full star-twinkle-4"></div>
        <div className="absolute bottom-[60%] left-[45%] w-1.5 h-1.5 bg-cyan-300 rounded-full star-twinkle-5"></div>

        {/* Medium stars */}
        <div className="absolute top-[12%] left-[45%] w-1 h-1 bg-white/70 rounded-full star-twinkle-2"></div>
        <div className="absolute top-[28%] right-[30%] w-0.5 h-0.5 bg-blue-200/80 rounded-full star-twinkle-3"></div>
        <div className="absolute bottom-[35%] left-[25%] w-1.5 h-1.5 bg-purple-200/60 rounded-full star-twinkle-1"></div>
        <div className="absolute top-[55%] right-[40%] w-0.5 h-0.5 bg-pink-200/70 rounded-full star-twinkle-4"></div>
        <div className="absolute bottom-[25%] right-[50%] w-1 h-1 bg-cyan-200/80 rounded-full star-twinkle-5"></div>
        <div className="absolute top-[75%] left-[15%] w-0.5 h-0.5 bg-white/60 rounded-full star-twinkle-2"></div>
        <div className="absolute top-[40%] left-[75%] w-1 h-1 bg-blue-300/70 rounded-full star-twinkle-1"></div>
        <div className="absolute bottom-[50%] right-[10%] w-0.5 h-0.5 bg-purple-300/80 rounded-full star-twinkle-3"></div>

        {/* Small distant stars */}
        <div className="absolute top-[18%] left-[35%] w-0.5 h-0.5 bg-white/50 rounded-full star-twinkle-4"></div>
        <div className="absolute top-[32%] right-[55%] w-0.5 h-0.5 bg-blue-200/40 rounded-full star-twinkle-5"></div>
        <div className="absolute bottom-[40%] left-[55%] w-0.5 h-0.5 bg-purple-200/50 rounded-full star-twinkle-1"></div>
        <div className="absolute top-[65%] right-[60%] w-0.5 h-0.5 bg-pink-200/40 rounded-full star-twinkle-2"></div>
        <div className="absolute bottom-[15%] right-[65%] w-0.5 h-0.5 bg-cyan-200/50 rounded-full star-twinkle-3"></div>
        <div className="absolute top-[85%] left-[25%] w-0.5 h-0.5 bg-white/40 rounded-full star-twinkle-4"></div>
        <div className="absolute top-[50%] left-[85%] w-0.5 h-0.5 bg-blue-300/50 rounded-full star-twinkle-5"></div>
        <div className="absolute bottom-[65%] right-[5%] w-0.5 h-0.5 bg-purple-300/40 rounded-full star-twinkle-1"></div>
      </div>

      {/* Floating Particles */}
      {enableAdvancedEffects && !reducedMotion && (
        <div className="absolute inset-0 pointer-events-none">
          {particles.map((particle) => (
            <div
              key={particle.id}
              className="floating-particle"
              style={{
                left: `${particle.left}%`,
                width: `${particle.size}px`,
                height: `${particle.size}px`,
                animationDelay: `${particle.animationDelay}s`,
                animationDuration: `${particle.animationDuration}s`,
              }}
            />
          ))}
        </div>
      )}

      {/* Semi-transparent overlay for text readability */}
      <div className="absolute inset-0 bg-black/60 z-5"></div>

      {/* Content Layer */}
      <div className="relative z-10 h-full w-full">
        {children}
      </div>

      {/* Add CSS styles */}
      <style jsx>{`
        .galaxy-starfield {
          background: 
            radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.8), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(173,216,230,0.6), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(221,160,221,0.7), transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,182,193,0.5), transparent),
            radial-gradient(2px 2px at 160px 30px, rgba(135,206,235,0.8), transparent),
            radial-gradient(1px 1px at 200px 60px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 240px 90px, rgba(173,216,230,0.7), transparent),
            radial-gradient(1px 1px at 280px 20px, rgba(221,160,221,0.5), transparent),
            radial-gradient(1px 1px at 320px 50px, rgba(255,182,193,0.8), transparent),
            radial-gradient(2px 2px at 360px 80px, rgba(135,206,235,0.6), transparent),
            linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #16213e 75%, #1a1a2e 100%);
          background-size: 400px 400px;
          animation: galaxyMove 120s linear infinite;
        }

        @keyframes galaxyMove {
          0% { background-position: 0% 0%; }
          25% { background-position: 50% 25%; }
          50% { background-position: 100% 50%; }
          75% { background-position: 50% 75%; }
          100% { background-position: 0% 0%; }
        }

        .star-twinkle-1 { animation: twinkle1 3s ease-in-out infinite; }
        .star-twinkle-2 { animation: twinkle2 4s ease-in-out infinite; }
        .star-twinkle-3 { animation: twinkle3 2.5s ease-in-out infinite; }
        .star-twinkle-4 { animation: twinkle4 3.5s ease-in-out infinite; }
        .star-twinkle-5 { animation: twinkle5 2s ease-in-out infinite; }

        @keyframes twinkle1 {
          0%, 100% { opacity: 0.3; transform: scale(1); }
          25% { opacity: 0.8; transform: scale(1.2); }
          50% { opacity: 0.5; transform: scale(1.1); }
          75% { opacity: 0.9; transform: scale(1.3); }
        }

        @keyframes twinkle2 {
          0%, 100% { opacity: 0.4; transform: scale(1); }
          33% { opacity: 0.9; transform: scale(1.1); }
          66% { opacity: 0.6; transform: scale(1.2); }
        }

        @keyframes twinkle3 {
          0%, 100% { opacity: 0.2; transform: scale(0.8); }
          50% { opacity: 1; transform: scale(1.4); }
        }

        @keyframes twinkle4 {
          0%, 100% { opacity: 0.5; transform: scale(1); }
          25% { opacity: 0.8; transform: scale(1.1); }
          75% { opacity: 0.7; transform: scale(1.2); }
        }

        @keyframes twinkle5 {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 1; }
        }

        .floating-particle {
          background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
          border-radius: 50%;
          animation: float 15s infinite linear;
          pointer-events: none;
        }

        @keyframes float {
          0% {
            transform: translateY(100vh) translateX(0px);
            opacity: 0;
          }
          10% { opacity: 1; }
          90% { opacity: 1; }
          100% {
            transform: translateY(-100px) translateX(100px);
            opacity: 0;
          }
        }

        .galaxy-spiral {
          background: radial-gradient(ellipse 800px 300px at 50% 50%, 
            rgba(138, 43, 226, 0.1) 0%, 
            rgba(72, 61, 139, 0.15) 30%, 
            rgba(25, 25, 112, 0.1) 60%, 
            transparent 80%);
          animation: spiral 60s linear infinite;
        }

        @keyframes spiral {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .nebula-cloud {
          background: 
            radial-gradient(ellipse 400px 200px at 20% 30%, rgba(147, 0, 211, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse 300px 150px at 80% 70%, rgba(75, 0, 130, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse 500px 250px at 40% 80%, rgba(138, 43, 226, 0.06) 0%, transparent 50%);
          animation: nebulaDrift 40s ease-in-out infinite alternate;
        }

        @keyframes nebulaDrift {
          0% { transform: translateX(-20px) translateY(-10px); }
          100% { transform: translateX(20px) translateY(10px); }
        }

        @media (prefers-reduced-motion: reduce) {
          .galaxy-starfield,
          .star-twinkle-1, .star-twinkle-2, .star-twinkle-3, .star-twinkle-4, .star-twinkle-5,
          .floating-particle, .galaxy-spiral, .nebula-cloud {
            animation: none !important;
          }
          .galaxy-starfield {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
          }
        }

        @media (max-width: 768px) {
          .galaxy-starfield {
            background-size: 200px 200px;
            animation-duration: 180s;
          }
          .floating-particle {
            animation-duration: 20s;
          }
        }
      `}</style>
    </div>
  );
};

export default GalaxyBackgroundCSS;
