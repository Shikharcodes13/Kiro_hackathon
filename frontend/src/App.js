import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import HeroSection from './components/HeroSection';
import ChatInterface from './components/ChatInterface';
import AgentStatus from './components/AgentStatus';
import './index.css';

function App() {
  const [showChat, setShowChat] = useState(false);
  const [agentStatus, setAgentStatus] = useState({
    buyer: 'idle',
    rag: 'idle',
    valuation: 'idle',
    loan: 'idle'
  });

  const handleStartChat = () => {
    setShowChat(true);
  };

  const handleBackToHome = () => {
    setShowChat(false);
    setAgentStatus({
      buyer: 'idle',
      rag: 'idle',
      valuation: 'idle',
      loan: 'idle'
    });
  };

  const updateAgentStatus = (agent, status) => {
    setAgentStatus(prev => ({
      ...prev,
      [agent]: status
    }));
  };

  return (
    <div className="min-h-screen bg-white">
      <AnimatePresence mode="wait">
        {!showChat ? (
          <motion.div
            key="hero"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.5 }}
          >
            <HeroSection onStartChat={handleStartChat} />
          </motion.div>
        ) : (
          <motion.div
            key="chat"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
            className="h-screen flex flex-col"
          >
            {/* Header */}
            <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <button
                  onClick={handleBackToHome}
                  className="flex items-center space-x-2 text-gray-600 hover:text-autoagent-primary transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  <span>Back to Home</span>
                </button>
                <div className="h-6 w-px bg-gray-300"></div>
                <h1 className="text-xl font-bold text-gray-900">AutoAgent Assistant</h1>
              </div>
              <AgentStatus agents={agentStatus} />
            </div>

            {/* Chat Interface */}
            <div className="flex-1 overflow-hidden">
              <ChatInterface 
                onAgentStatusUpdate={updateAgentStatus}
                agentStatus={agentStatus}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;