import React from 'react';
import { motion } from 'framer-motion';
import { Star, Zap, Fuel, MapPin, TrendingUp, TrendingDown } from 'lucide-react';

const CarCard = ({ car }) => {
  const formatPrice = (price) => {
    return `₹${(price / 100000).toFixed(1)}L`;
  };

  const getDealScoreColor = (score) => {
    if (!score) return 'text-gray-500';
    switch (score.score?.toLowerCase()) {
      case 'excellent': return 'text-green-600';
      case 'good': return 'text-blue-600';
      case 'fair': return 'text-yellow-600';
      case 'overpriced': return 'text-red-600';
      default: return 'text-gray-500';
    }
  };

  const getDealScoreIcon = (score) => {
    if (!score) return null;
    switch (score.score?.toLowerCase()) {
      case 'excellent':
      case 'good':
        return <TrendingUp className="w-4 h-4" />;
      case 'overpriced':
        return <TrendingDown className="w-4 h-4" />;
      default:
        return null;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5, shadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)" }}
      transition={{ duration: 0.3 }}
      className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-all duration-300"
    >
      {/* Car Image */}
      <div className="relative h-48 bg-gradient-to-br from-gray-100 to-gray-200">
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="w-16 h-16 bg-autoagent-primary/10 rounded-full flex items-center justify-center mx-auto mb-2">
              <Zap className="w-8 h-8 text-autoagent-primary" />
            </div>
            <p className="text-sm text-gray-600 font-medium">{car.make} {car.model}</p>
          </div>
        </div>
        
        {/* Deal Score Badge */}
        {car.deal_score && (
          <div className={`absolute top-3 right-3 px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${
            car.deal_score.score === 'Excellent' ? 'bg-green-100 text-green-700' :
            car.deal_score.score === 'Good' ? 'bg-blue-100 text-blue-700' :
            car.deal_score.score === 'Fair' ? 'bg-yellow-100 text-yellow-700' :
            'bg-red-100 text-red-700'
          }`}>
            {getDealScoreIcon(car.deal_score)}
            <span>{car.deal_score.score}</span>
          </div>
        )}

        {/* Year Badge */}
        <div className="absolute top-3 left-3 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full text-xs font-medium text-gray-700">
          {car.year}
        </div>
      </div>

      {/* Car Details */}
      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="text-lg font-bold text-gray-900">{car.make} {car.model}</h3>
            <div className="flex items-center space-x-2 mt-1">
              {car.location && (
                <div className="flex items-center space-x-1 text-gray-500">
                  <MapPin className="w-3 h-3" />
                  <span className="text-xs">{car.location}</span>
                </div>
              )}
              {car.fuel_type && (
                <div className="flex items-center space-x-1 text-gray-500">
                  <Fuel className="w-3 h-3" />
                  <span className="text-xs">{car.fuel_type}</span>
                </div>
              )}
            </div>
          </div>
          
          {car.rating && (
            <div className="flex items-center space-x-1 bg-yellow-50 px-2 py-1 rounded-full">
              <Star className="w-3 h-3 text-yellow-500 fill-current" />
              <span className="text-xs font-medium text-yellow-700">{car.rating}</span>
            </div>
          )}
        </div>

        {/* Price */}
        <div className="mb-4">
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-bold text-gray-900">
              {formatPrice(car.market_value || car.price)}
            </span>
            {car.market_value && car.market_value !== car.price && (
              <span className="text-sm text-gray-500 line-through">
                {formatPrice(car.price)}
              </span>
            )}
          </div>
          
          {car.price_analysis?.variance_percent && (
            <div className={`text-xs mt-1 flex items-center space-x-1 ${
              car.price_analysis.variance_percent > 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {car.price_analysis.variance_percent > 0 ? (
                <TrendingDown className="w-3 h-3" />
              ) : (
                <TrendingUp className="w-3 h-3" />
              )}
              <span>
                {Math.abs(car.price_analysis.variance_percent)}% 
                {car.price_analysis.variance_percent > 0 ? ' below' : ' above'} market
              </span>
            </div>
          )}
        </div>

        {/* Features */}
        {car.features && car.features.length > 0 && (
          <div className="mb-4">
            <div className="flex flex-wrap gap-1">
              {car.features.slice(0, 3).map((feature, index) => (
                <span
                  key={index}
                  className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full"
                >
                  {feature}
                </span>
              ))}
              {car.features.length > 3 && (
                <span className="text-xs text-gray-500 px-2 py-1">
                  +{car.features.length - 3} more
                </span>
              )}
            </div>
          </div>
        )}

        {/* Market Position */}
        {car.market_position && (
          <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-xs text-blue-800 font-medium mb-1">Market Position</p>
            <p className="text-xs text-blue-700">{car.market_position}</p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-2">
          <button className="flex-1 bg-autoagent-primary text-white text-sm font-medium py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
            View Details
          </button>
          <button className="flex-1 bg-gray-100 text-gray-700 text-sm font-medium py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors">
            Compare
          </button>
        </div>

        {/* Price Recommendation */}
        {car.price_recommendation && (
          <div className="mt-3 p-2 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-600">
              <span className="font-medium">Recommendation:</span> {car.price_recommendation.message}
            </p>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default CarCard;