import React from 'react';
import { History, Plus, Trash2 } from 'lucide-react';

const Sidebar = ({ 
  chatHistory = [],
  onNewChat,
  onSelectChat,
  onDeleteChat,
  activeChatId = null 
}) => {
  // Mock data if no history provided
  const defaultHistory = [
    { id: 1, title: "Conversation 1", timestamp: "2 hours ago" },
    { id: 2, title: "Image Analysis", timestamp: "5 hours ago" },
    { id: 3, title: "Code Review", timestamp: "1 day ago" },
    { id: 4, title: "Travel Planning", timestamp: "2 days ago" },
    { id: 5, title: "Recipe Ideas", timestamp: "3 days ago" },
    { id: 6, title: "Learning Python", timestamp: "1 week ago" },
    { id: 7, title: "AI Discussion", timestamp: "1 week ago" },
    { id: 8, title: "Project Help", timestamp: "2 weeks ago" },
  ];

  const historyItems = chatHistory.length > 0 ? chatHistory : defaultHistory;

  return (
    <div className="relative w-72 h-screen overflow-hidden">
      {/* Video Background */}
      <video
        className="absolute inset-0 w-full h-full object-cover z-0"
        autoPlay
        loop
        muted
        playsInline
        poster="/public/images/stars-poster.jpg"
      >
        <source src="/public/videos/stars.mp4" type="video/mp4" />
        {/* Fallback for browsers that don't support video */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-blue-900 to-black"></div>
      </video>

      {/* Dark Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/80 to-black/90 z-10"></div>

      {/* Content Layer */}
      <div className="relative z-20 h-full flex flex-col p-4">
        {/* Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-4 tracking-wide">
            Chat History
          </h2>
          
          {/* New Chat Button */}
          <button
            onClick={onNewChat}
            className="w-full flex items-center justify-center gap-3 px-4 py-3 
                     bg-white/10 hover:bg-white/20 rounded-xl transition-all duration-300
                     border border-white/20 hover:border-white/30 group"
          >
            <Plus className="w-5 h-5 text-white group-hover:rotate-90 transition-transform duration-300" />
            <span className="text-white font-medium">New Chat</span>
          </button>
        </div>

        {/* Chat History List */}
        <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent">
          <div className="space-y-2">
            {historyItems.map((item) => (
              <div
                key={item.id}
                className={`group relative flex items-center gap-3 p-3 rounded-xl 
                          transition-all duration-300 cursor-pointer
                          ${activeChatId === item.id 
                            ? 'bg-white/20 border border-white/30' 
                            : 'bg-white/10 hover:bg-white/20 border border-white/10 hover:border-white/20'
                          }`}
                onClick={() => onSelectChat?.(item.id)}
              >
                {/* History Icon */}
                <div className="flex-shrink-0">
                  <History className="w-4 h-4 text-white/80 group-hover:text-white transition-colors" />
                </div>

                {/* Chat Info */}
                <div className="flex-1 min-w-0">
                  <p className="text-white font-medium text-sm truncate">
                    {item.title}
                  </p>
                  <p className="text-white/60 text-xs mt-1">
                    {item.timestamp}
                  </p>
                </div>

                {/* Delete Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteChat?.(item.id);
                  }}
                  className="opacity-0 group-hover:opacity-100 transition-opacity duration-200
                           p-1 hover:bg-red-500/20 rounded-md"
                >
                  <Trash2 className="w-3 h-3 text-red-400 hover:text-red-300" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-4 pt-4 border-t border-white/20">
          <div className="text-center">
            <p className="text-white/60 text-xs">
              Aditya AI Assistant
            </p>
            <p className="text-white/40 text-xs mt-1">
              Galaxy-Powered Intelligence
            </p>
          </div>
        </div>
      </div>

      {/* Futuristic Border Glow */}
      <div className="absolute inset-0 z-30 pointer-events-none">
        <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-blue-400/50 to-transparent"></div>
        <div className="absolute bottom-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-purple-400/50 to-transparent"></div>
        <div className="absolute top-0 right-0 w-px h-full bg-gradient-to-b from-transparent via-cyan-400/50 to-transparent"></div>
      </div>
    </div>
  );
};

export default Sidebar;
