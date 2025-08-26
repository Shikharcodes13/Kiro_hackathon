import React from 'react';
import { motion } from 'framer-motion';
import { Car, Brain, TrendingUp, DollarSign, CheckCircle, Clock, Zap } from 'lucide-react';

const AgentStatus = ({ agents }) => {
  const agentConfig = {
    buyer: {
      name: 'Buyer Agent',
      icon: Car,
      color: 'blue'
    },
    rag: {
      name: 'RAG Agent',
      icon: Brain,
      color: 'purple'
    },
    valuation: {
      name: 'Valuation Agent',
      icon: TrendingUp,
      color: 'green'
    },
    loan: {
      name: 'Loan Agent',
      icon: DollarSign,
      color: 'yellow'
    }
  };

  const getStatusColor = (status, baseColor) => {
    switch (status) {
      case 'processing':
        return `text-${baseColor}-600 bg-${baseColor}-100`;
      case 'completed':
        return 'text-green-600 bg-green-100';
      case 'idle':
      default:
        return 'text-gray-400 bg-gray-100';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'processing':
        return <Zap className="w-3 h-3 animate-pulse" />;
      case 'completed':
        return <CheckCircle className="w-3 h-3" />;
      case 'idle':
      default:
        return <Clock className="w-3 h-3" />;
    }
  };

  return (
    <div className="flex items-center space-x-4">
      <span className="text-sm text-gray-600 font-medium">AI Agents:</span>
      <div className="flex items-center space-x-3">
        {Object.entries(agents).map(([agentKey, status]) => {
          const config = agentConfig[agentKey];
          if (!config) return null;

          const IconComponent = config.icon;

          return (
            <motion.div
              key={agentKey}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.3 }}
              className="flex items-center space-x-2"
            >
              <div className={`relative p-2 rounded-full transition-all duration-300 ${getStatusColor(status, config.color)}`}>
                <IconComponent className="w-4 h-4" />
                
                {/* Status indicator */}
                <div className="absolute -top-1 -right-1">
                  {getStatusIcon(status)}
                </div>

                {/* Processing animation */}
                {status === 'processing' && (
                  <motion.div
                    className="absolute inset-0 rounded-full border-2 border-current opacity-30"
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  />
                )}
              </div>
              
              <div className="hidden md:block">
                <div className="text-xs font-medium text-gray-700">{config.name}</div>
                <div className={`text-xs capitalize ${
                  status === 'processing' ? 'text-blue-600' :
                  status === 'completed' ? 'text-green-600' :
                  'text-gray-500'
                }`}>
                  {status === 'processing' ? 'Working...' : status}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export default AgentStatus;