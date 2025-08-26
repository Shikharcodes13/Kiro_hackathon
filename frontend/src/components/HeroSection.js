import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MessageCircle, Zap, Brain, Car, TrendingUp, Shield } from 'lucide-react';

const HeroSection = ({ onStartChat }) => {
  const [currentText, setCurrentText] = useState('');
  const [textIndex, setTextIndex] = useState(0);
  const [scrollY, setScrollY] = useState(0);
  
  const heroTexts = [
    "Find your perfect car with AI",
    "Get instant market insights",
    "Compare financing options",
    "Discover the best deals"
  ];

  useEffect(() => {
    const text = heroTexts[textIndex];
    let charIndex = 0;
    
    const typeText = () => {
      if (charIndex < text.length) {
        setCurrentText(text.slice(0, charIndex + 1));
        charIndex++;
        setTimeout(typeText, 100);
      } else {
        setTimeout(() => {
          setTextIndex((prev) => (prev + 1) % heroTexts.length);
          setCurrentText('');
        }, 2000);
      }
    };

    const timeout = setTimeout(typeText, 500);
    return () => clearTimeout(timeout);
  }, [textIndex]);

  // Scroll tracking for car animation
  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Search",
      description: "LangChain agents understand your needs and find perfect matches"
    },
    {
      icon: TrendingUp,
      title: "Market Intelligence",
      description: "Real-time pricing, trends, and expert insights from our RAG system"
    },
    {
      icon: Shield,
      title: "Smart Financing",
      description: "Compare loans, subsidies, and get pre-approval instantly"
    }
  ];

  return (
    <>
      {/* First Section - Image Only */}
      <div className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-gray-900 to-black overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-32 h-32 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-40 h-40 bg-gradient-to-r from-red-500 to-pink-500 rounded-full blur-3xl"></div>
          <div className="absolute top-1/2 left-1/4 w-24 h-24 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full blur-2xl"></div>
        </div>
        
        {/* Grid Pattern Overlay */}
        <div className="absolute inset-0 opacity-5" style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, rgba(255,255,255,0.3) 1px, transparent 0)`,
          backgroundSize: '50px 50px'
        }}></div>

        {/* Top Navigation Overlay */}
        <div className="absolute top-0 left-0 right-0 z-20 p-6">
          <div className="flex items-center justify-between">
            {/* Menu Button */}
            <motion.button
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="flex items-center space-x-2 text-white hover:text-yellow-400 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <span className="text-lg font-medium">Menu</span>
            </motion.button>

            {/* Brand/Logo */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex items-center space-x-3"
            >
              <div className="w-10 h-10 bg-yellow-400 rounded-lg flex items-center justify-center">
                <Car className="w-6 h-6 text-black" />
              </div>
              <span className="text-2xl font-bold text-white">AutoAgent</span>
            </motion.div>

            {/* Account Button */}
            <motion.button
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="flex items-center space-x-2 text-white hover:text-yellow-400 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span className="text-lg font-medium">Account</span>
            </motion.button>
          </div>
        </div>

        {/* Conversational Text Box Overlay */}
        <div className="absolute bottom-8 left-8 right-8 z-20">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="max-w-2xl mx-auto"
          >
            <div className="bg-black/40 backdrop-blur-lg rounded-2xl border border-white/20 p-6 shadow-2xl">
              <div className="flex items-center space-x-4">
                <div className="flex-1">
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="Ask me anything about cars... 'Find me a luxury sedan under $50k'"
                      className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent"
                    />
                    <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                      <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                      </svg>
                    </div>
                  </div>
                </div>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={onStartChat}
                  className="bg-yellow-400 hover:bg-yellow-500 text-black px-6 py-3 rounded-xl font-medium transition-colors flex items-center space-x-2"
                >
                  <MessageCircle className="w-5 h-5" />
                  <span>Chat</span>
                </motion.button>
              </div>
              
              {/* Quick Suggestions */}
              <div className="mt-4 flex flex-wrap gap-2">
                <span className="text-sm text-gray-300">Try:</span>
                {["Best electric cars", "Financing options", "Compare models"].map((suggestion, index) => (
                  <button
                    key={index}
                    className="text-sm bg-white/10 hover:bg-white/20 text-white px-3 py-1 rounded-full transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </motion.div>
        </div>

        {/* Car Image */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.2, ease: "easeOut" }}
          className="relative z-10 w-full px-4"
        >
          <motion.img
            animate={{ 
              y: [0, -20, 0],
              x: scrollY * 8 // Car speeds off screen very fast on scroll
            }}
            transition={{ 
              y: { duration: 6, repeat: Infinity, ease: "easeInOut" },
              x: { duration: 0.05, ease: "easeOut" }
            }}
            src="/lamborghini-miura-1971-6-removebg-preview.png"
            alt="Lamborghini Miura 1971"
            className="w-full h-auto drop-shadow-2xl scale-125"
            style={{
              transform: `translateX(${scrollY * 5}px)` // Aggressive movement, no limit
            }}
          />
          
          {/* Glow Effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-yellow-400/30 to-orange-500/30 rounded-full blur-3xl -z-10 transform scale-110"></div>
        </motion.div>
      </div>

      {/* Second Section - Navigation & Content */}
      <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-gray-900 to-black">
        {/* Navigation */}
        <nav className="relative z-10 px-6 py-6">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="flex items-center space-x-3"
            >
              <div className="w-10 h-10 bg-autoagent-primary rounded-lg flex items-center justify-center">
                <Car className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-white">AutoAgent</span>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="hidden md:flex items-center space-x-8"
            >
              <a href="#features" className="text-gray-300 hover:text-autoagent-primary transition-colors">Features</a>
              <a href="#demo" className="text-gray-300 hover:text-autoagent-primary transition-colors">Demo</a>
              <a href="#about" className="text-gray-300 hover:text-autoagent-primary transition-colors">About</a>
            </motion.div>
          </div>
        </nav>

        {/* Hero Content */}
        <div className="relative z-10 max-w-7xl mx-auto px-6 pt-20 pb-32">
          <div className="text-center space-y-8">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="inline-flex items-center space-x-2 bg-blue-100 text-autoagent-primary px-4 py-2 rounded-full text-sm font-medium"
            >
              <Zap className="w-4 h-4" />
              <span>Powered by LangChain AI</span>
            </motion.div>
            
            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-5xl lg:text-6xl font-bold text-white leading-tight"
            >
              <span className="block">The Future of</span>
              <span className="block text-yellow-400">Car Shopping</span>
            </motion.h1>
            
            <div className="h-16 flex items-center justify-center">
              <p className="text-xl text-gray-300 font-medium">
                {currentText}
                <span className="animate-pulse text-yellow-400">|</span>
              </p>
            </div>

            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="text-lg text-gray-300 leading-relaxed max-w-2xl mx-auto"
            >
              Experience the power of AI agents working together to find your perfect car. 
              From search to financing, our intelligent system handles everything seamlessly.
            </motion.p>

            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onStartChat}
                className="btn-primary flex items-center justify-center space-x-2 group"
              >
                <MessageCircle className="w-5 h-5 group-hover:rotate-12 transition-transform" />
                <span>Start Conversation</span>
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-secondary flex items-center justify-center space-x-2"
              >
                <span>Watch Demo</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h1m4 0h1m6-10V7a3 3 0 01-3 3H4a3 3 0 01-3-3V4a3 3 0 013 3z" />
                </svg>
              </motion.button>
            </motion.div>

            {/* Stats */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1 }}
              className="grid grid-cols-3 gap-8 pt-8 border-t border-gray-700 max-w-lg mx-auto"
            >
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-400">50K+</div>
                <div className="text-sm text-gray-400">Cars Analyzed</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-400">98%</div>
                <div className="text-sm text-gray-400">Accuracy Rate</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-400">24/7</div>
                <div className="text-sm text-gray-400">AI Assistant</div>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Features Section */}
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="relative z-10 max-w-7xl mx-auto px-6 pb-20"
        >
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.8 + index * 0.2 }}
                className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
              >
                <div className="w-12 h-12 bg-autoagent-primary/10 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-autoagent-primary" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Floating Action Button for Mobile */}
        <motion.button
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 1.5 }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onStartChat}
          className="fixed bottom-6 right-6 w-16 h-16 bg-autoagent-primary text-white rounded-full shadow-lg flex items-center justify-center z-50 md:hidden"
        >
          <MessageCircle className="w-6 h-6" />
        </motion.button>
      </div>
    </>
  );
};

export default HeroSection;