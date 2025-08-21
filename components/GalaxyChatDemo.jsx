import React, { useState } from 'react';
import GalaxyBackground from './components/GalaxyBackground';
import GalaxyBackgroundCSS from './components/GalaxyBackgroundCSS';

const App = () => {
  const [useVideo, setUseVideo] = useState(false);
  const [useCanvasVersion, setUseCanvasVersion] = useState(true);
  const [advancedEffects, setAdvancedEffects] = useState(true);

  // Your chat messages data
  const [messages, setMessages] = useState([
    { id: 1, type: 'ai', content: 'Hello! Welcome to the galaxy-powered chat interface!' },
    { id: 2, type: 'user', content: 'This looks amazing! The stars are twinkling beautifully.' },
    { id: 3, type: 'ai', content: 'Thank you! This background features both video and pure CSS options for optimal performance.' },
  ]);

  const [inputMessage, setInputMessage] = useState('');

  const sendMessage = () => {
    if (inputMessage.trim()) {
      setMessages([...messages, {
        id: messages.length + 1,
        type: 'user',
        content: inputMessage
      }]);
      setInputMessage('');
    }
  };

  const ChatContent = () => (
    <div className="flex flex-col h-full max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-white">Aditya AI - Galaxy Chat</h1>
        <div className="flex gap-2">
          <button
            onClick={() => setUseCanvasVersion(!useCanvasVersion)}
            className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-lg text-white hover:bg-white/20 transition-colors text-sm"
          >
            {useCanvasVersion ? 'Canvas' : 'CSS'} Mode
          </button>
          {useCanvasVersion && (
            <button
              onClick={() => setUseVideo(!useVideo)}
              className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-lg text-white hover:bg-white/20 transition-colors text-sm"
            >
              {useVideo ? '🎥 Video' : '🎨 Canvas'}
            </button>
          )}
          {!useCanvasVersion && (
            <button
              onClick={() => setAdvancedEffects(!advancedEffects)}
              className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-lg text-white hover:bg-white/20 transition-colors text-sm"
            >
              {advancedEffects ? '✨ Full' : '⚡ Minimal'}
            </button>
          )}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-6">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl backdrop-blur-sm border ${
                message.type === 'user'
                  ? 'bg-blue-600/80 border-blue-500/50 text-white'
                  : 'bg-white/10 border-white/20 text-white'
              }`}
            >
              <p className="text-sm leading-relaxed">{message.content}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Input Area */}
      <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4 border border-white/20">
        <div className="flex gap-3">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
            className="flex-1 bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent backdrop-blur-sm"
          />
          <button
            onClick={sendMessage}
            className="px-6 py-3 bg-blue-600/80 hover:bg-blue-600 text-white rounded-xl transition-colors backdrop-blur-sm border border-blue-500/50"
          >
            Send
          </button>
        </div>
      </div>

      {/* Features Info */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-3 border border-white/10">
          <h3 className="text-white font-semibold text-sm mb-1">🌌 Galaxy Background</h3>
          <p className="text-white/70 text-xs">Animated starfield with twinkling stars</p>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-3 border border-white/10">
          <h3 className="text-white font-semibold text-sm mb-1">⚡ Performance</h3>
          <p className="text-white/70 text-xs">CSS & Canvas options for all devices</p>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-3 border border-white/10">
          <h3 className="text-white font-semibold text-sm mb-1">📱 Responsive</h3>
          <p className="text-white/70 text-xs">Works perfectly on mobile & desktop</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="h-screen w-screen">
      {useCanvasVersion ? (
        <GalaxyBackground useVideo={useVideo}>
          <ChatContent />
        </GalaxyBackground>
      ) : (
        <GalaxyBackgroundCSS enableAdvancedEffects={advancedEffects}>
          <ChatContent />
        </GalaxyBackgroundCSS>
      )}
    </div>
  );
};

export default App;
