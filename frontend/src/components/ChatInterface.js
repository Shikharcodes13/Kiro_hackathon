import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Loader, Car, TrendingUp, DollarSign, FileText } from 'lucide-react';
import axios from 'axios';
import CarCard from './CarCard';
import AgentThinking from './AgentThinking';

const ChatInterface = ({ onAgentStatusUpdate, agentStatus }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hi! I'm your AI automotive assistant. I can help you find the perfect car, compare prices, and get financing options. What are you looking for today?",
      timestamp: new Date(),
      agent: 'system'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgentTrace, setCurrentAgentTrace] = useState([]);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentAgentTrace]);

  const simulateAgentProgress = (agentTrace) => {
    setCurrentAgentTrace([]);
    
    agentTrace.forEach((trace, index) => {
      setTimeout(() => {
        const agentName = trace.agent.toLowerCase().split(' ')[0];
        onAgentStatusUpdate(agentName, 'processing');
        
        setCurrentAgentTrace(prev => [...prev, trace]);
        
        setTimeout(() => {
          onAgentStatusUpdate(agentName, 'completed');
        }, 1500);
      }, index * 2000);
    });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setCurrentAgentTrace([]);

    // Reset all agent statuses
    Object.keys(agentStatus).forEach(agent => {
      onAgentStatusUpdate(agent, 'idle');
    });

    try {
      const response = await axios.post('/query', {
        query: inputValue,
        context: { frontend: true }
      });

      const { result, agent_trace } = response.data;

      // Simulate agent progress
      if (agent_trace && agent_trace.length > 0) {
        simulateAgentProgress(agent_trace);
      }

      // Wait for agent simulation to complete
      setTimeout(() => {
        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: result.summary || 'I found some information for you!',
          timestamp: new Date(),
          data: result,
          agentTrace: agent_trace
        };

        setMessages(prev => [...prev, botMessage]);
        setIsLoading(false);
        setCurrentAgentTrace([]);
      }, agent_trace ? agent_trace.length * 2000 + 1000 : 2000);

    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: "I'm sorry, I encountered an error. Please try again or check if the backend server is running.",
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
      setCurrentAgentTrace([]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const getAgentIcon = (agentName) => {
    const name = agentName.toLowerCase();
    if (name.includes('buyer')) return Car;
    if (name.includes('rag')) return TrendingUp;
    if (name.includes('loan')) return DollarSign;
    if (name.includes('valuation')) return FileText;
    return Bot;
  };

  const quickQuestions = [
    "Best EV under ₹15L in Delhi?",
    "Compare Tata Nexon EV vs MG ZS EV",
    "What are the loan options for electric cars?",
    "Show me hybrid cars under ₹20L"
  ];

  const handleQuickQuestion = (question) => {
    setInputValue(question);
    inputRef.current?.focus();
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              transition={{ duration: 0.3 }}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex items-start space-x-3 max-w-4xl ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                  message.type === 'user' 
                    ? 'bg-autoagent-primary text-white' 
                    : message.isError 
                      ? 'bg-red-100 text-red-600'
                      : 'bg-white text-autoagent-primary border-2 border-autoagent-primary'
                }`}>
                  {message.type === 'user' ? (
                    <User className="w-5 h-5" />
                  ) : (
                    <Bot className="w-5 h-5" />
                  )}
                </div>

                {/* Message Content */}
                <div className={`flex-1 ${message.type === 'user' ? 'text-right' : ''}`}>
                  <div className={`inline-block p-4 rounded-2xl ${
                    message.type === 'user'
                      ? 'bg-autoagent-primary text-white'
                      : message.isError
                        ? 'bg-red-50 text-red-800 border border-red-200'
                        : 'bg-white text-gray-800 shadow-sm border border-gray-200'
                  }`}>
                    <p className="text-sm leading-relaxed">{message.content}</p>
                  </div>

                  {/* Cars Display */}
                  {message.data?.cars && message.data.cars.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3 }}
                      className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3"
                    >
                      {message.data.cars.map((car, index) => (
                        <CarCard key={car.id || index} car={car} />
                      ))}
                    </motion.div>
                  )}

                  {/* Insights Display */}
                  {message.data?.insights && message.data.insights.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.5 }}
                      className="mt-4 space-y-3"
                    >
                      <h4 className="text-sm font-semibold text-gray-700">Market Insights:</h4>
                      {message.data.insights.slice(0, 3).map((insight, index) => (
                        <div key={index} className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                          <h5 className="font-medium text-blue-900 text-sm">{insight.title}</h5>
                          <p className="text-blue-700 text-xs mt-1">{insight.content}</p>
                        </div>
                      ))}
                    </motion.div>
                  )}

                  {/* Financing Options */}
                  {message.data?.financing_options && message.data.financing_options.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.7 }}
                      className="mt-4 space-y-3"
                    >
                      <h4 className="text-sm font-semibold text-gray-700">Financing Options:</h4>
                      {message.data.financing_options.slice(0, 2).map((option, index) => (
                        <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-3">
                          <h5 className="font-medium text-green-900 text-sm">{option.car_name}</h5>
                          <div className="grid grid-cols-2 gap-2 mt-2 text-xs text-green-700">
                            <div>Best EMI: ₹{option.loan_options?.[0]?.emi?.toLocaleString()}</div>
                            <div>Rate: {option.loan_options?.[0]?.interest_rate}%</div>
                          </div>
                        </div>
                      ))}
                    </motion.div>
                  )}

                  <div className="text-xs text-gray-500 mt-2">
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Agent Thinking Animation */}
        <AnimatePresence>
          {currentAgentTrace.length > 0 && (
            <AgentThinking 
              traces={currentAgentTrace} 
              getAgentIcon={getAgentIcon}
            />
          )}
        </AnimatePresence>

        {/* Loading Animation */}
        <AnimatePresence>
          {isLoading && currentAgentTrace.length === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="flex justify-start"
            >
              <div className="flex items-start space-x-3">
                <div className="w-10 h-10 rounded-full bg-white text-autoagent-primary border-2 border-autoagent-primary flex items-center justify-center">
                  <Bot className="w-5 h-5" />
                </div>
                <div className="bg-white p-4 rounded-2xl shadow-sm border border-gray-200">
                  <div className="flex items-center space-x-2">
                    <Loader className="w-4 h-4 animate-spin text-autoagent-primary" />
                    <span className="text-sm text-gray-600">AI agents are working...</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Questions */}
      {messages.length === 1 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="px-6 py-4 border-t border-gray-200 bg-white"
        >
          <p className="text-sm text-gray-600 mb-3">Try asking:</p>
          <div className="flex flex-wrap gap-2">
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleQuickQuestion(question)}
                className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-full transition-colors"
              >
                {question}
              </button>
            ))}
          </div>
        </motion.div>
      )}

      {/* Input Area */}
      <div className="p-6 bg-white border-t border-gray-200">
        <div className="flex items-end space-x-4">
          <div className="flex-1">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about cars, pricing, financing, or anything automotive..."
              className="chat-input resize-none"
              rows="1"
              style={{ minHeight: '44px', maxHeight: '120px' }}
              disabled={isLoading}
            />
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className={`p-3 rounded-lg transition-all duration-200 ${
              inputValue.trim() && !isLoading
                ? 'bg-autoagent-primary text-white hover:bg-blue-700 shadow-lg'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }`}
          >
            {isLoading ? (
              <Loader className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </motion.button>
        </div>
        
        <p className="text-xs text-gray-500 mt-2 text-center">
          Powered by LangChain AI • Press Enter to send
        </p>
      </div>
    </div>
  );
};

export default ChatInterface;