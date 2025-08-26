import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, CheckCircle } from 'lucide-react';

const AgentThinking = ({ traces, getAgentIcon }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex justify-start"
    >
      <div className="flex items-start space-x-3 max-w-4xl">
        <div className="w-10 h-10 rounded-full bg-white text-autoagent-primary border-2 border-autoagent-primary flex items-center justify-center">
          <Bot className="w-5 h-5" />
        </div>
        
        <div className="bg-white p-4 rounded-2xl shadow-sm border border-gray-200 min-w-80">
          <div className="flex items-center space-x-2 mb-3">
            <div className="flex space-x-1">
              <div className="typing-indicator"></div>
              <div className="typing-indicator"></div>
              <div className="typing-indicator"></div>
            </div>
            <span className="text-sm text-gray-600">AI agents collaborating...</span>
          </div>
          
          <div className="space-y-3">
            <AnimatePresence>
              {traces.map((trace, index) => {
                const IconComponent = getAgentIcon(trace.agent);
                
                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className="flex items-center space-x-3 p-2 bg-gray-50 rounded-lg"
                  >
                    <div className="w-6 h-6 bg-autoagent-primary/10 rounded-full flex items-center justify-center">
                      <IconComponent className="w-3 h-3 text-autoagent-primary" />
                    </div>
                    
                    <div className="flex-1">
                      <div className="text-xs font-medium text-gray-700">{trace.agent}</div>
                      <div className="text-xs text-gray-600">{trace.output}</div>
                    </div>
                    
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.5 }}
                    >
                      <CheckCircle className="w-4 h-4 text-green-500" />
                    </motion.div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default AgentThinking;