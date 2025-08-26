from typing import Dict, List, Any
import math

class ValuationAgent:
    def __init__(self):
        self.name = "Valuation Agent"
        self.pricing_model = self._initialize_pricing_model()
    
    async def process(self, input_data: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main processing method for valuation agent"""
        cars = input_data.get("cars", [])
        params = params or {}
        
        action = params.get("action", "price_check")
        
        if action == "price_check":
            return await self.perform_price_check(input_data)
        elif action == "full_assessment":
            return await self.perform_full_valuation(input_data)
        else:
            return await self.perform_price_check(input_data)
    
    async def perform_price_check(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform price analysis for cars"""
        cars = input_data.get("cars", [])
        criteria = input_data.get("criteria", {})
        
        # Add valuation data to each car
        priced_cars = []
        for car in cars:
            valuation = self.calculate_market_value(car)
            priced_car = {
                **car,
                "market_value": valuation["market_value"],
                "price_analysis": valuation["analysis"],
                "deal_score": valuation["deal_score"],
                "price_recommendation": valuation["recommendation"]
            }
            priced_cars.append(priced_car)
        
        market_summary = self.generate_market_summary(priced_cars, criteria)
        
        return {
            **input_data,
            "cars": priced_cars,
            "action": "price_analysis",
            "summary": f"Analyzed pricing for {len(cars)} vehicles with market intelligence",
            "market_summary": market_summary
        }
    
    async def perform_full_valuation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive valuation including depreciation and market factors"""
        # This would be used for selling scenarios
        return await self.perform_price_check(input_data)
    
    def calculate_market_value(self, car: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate market-adjusted value for a car"""
        base_price = car["price"]
        market_factors = self.get_market_factors(car)
        
        # Apply market factors to base price
        adjusted_price = base_price
        for factor in market_factors:
            adjusted_price *= (1 + factor["impact"])
        
        adjusted_price = round(adjusted_price)
        deal_score = self.calculate_deal_score(base_price, adjusted_price)
        
        return {
            "market_value": adjusted_price,
            "analysis": {
                "list_price": base_price,
                "market_price": adjusted_price,
                "factors": market_factors,
                "variance_percent": round(((adjusted_price - base_price) / base_price) * 100, 1)
            },
            "deal_score": deal_score,
            "recommendation": self.generate_price_recommendation(deal_score, base_price, adjusted_price)
        }
    
    def get_market_factors(self, car: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get market factors affecting car pricing"""
        factors = []
        
        # EV market demand factor
        if car["fuel_type"] == "Electric":
            factors.append({
                "name": "EV Market Demand",
                "impact": 0.05,
                "description": "High demand for electric vehicles with government incentives"
            })
        
        # Brand reputation factors
        brand_factors = {
            "Tata": 0.02,
            "Hyundai": 0.03,
            "MG": -0.01,
            "Mahindra": 0.01,
            "Maruti": 0.025
        }
        
        if car["make"] in brand_factors:
            factors.append({
                "name": "Brand Premium",
                "impact": brand_factors[car["make"]],
                "description": f"{car['make']} brand positioning and reliability reputation"
            })
        
        # Model year impact (depreciation)
        current_year = 2024
        age_years = current_year - car["year"]
        if age_years > 0:
            age_impact = -0.08 * age_years  # 8% per year depreciation
            factors.append({
                "name": "Model Year Depreciation",
                "impact": age_impact,
                "description": f"{age_years} year(s) old model with standard depreciation"
            })
        
        # Location-based pricing
        location_factors = {
            "Delhi": 0.03,
            "Mumbai": 0.04,
            "Bangalore": 0.02,
            "Chennai": 0.01,
            "Pune": 0.015
        }
        
        if car["location"] in location_factors:
            factors.append({
                "name": "Location Premium",
                "impact": location_factors[car["location"]],
                "description": f"{car['location']} market pricing dynamics"
            })
        
        # Fuel type market dynamics
        if car["fuel_type"] == "Diesel":
            factors.append({
                "name": "Diesel Market Shift",
                "impact": -0.02,
                "description": "Declining diesel preference due to emission norms"
            })
        elif car["fuel_type"] == "Petrol":
            factors.append({
                "name": "Petrol Stability",
                "impact": 0.01,
                "description": "Stable petrol market with consistent demand"
            })
        
        # Rating-based premium
        if car["rating"] >= 4.2:
            factors.append({
                "name": "High Rating Premium",
                "impact": 0.02,
                "description": "Premium for highly-rated vehicles"
            })
        elif car["rating"] <= 3.8:
            factors.append({
                "name": "Rating Discount",
                "impact": -0.015,
                "description": "Discount due to lower market rating"
            })
        
        return factors
    
    def calculate_deal_score(self, list_price: int, market_price: int) -> Dict[str, str]:
        """Calculate deal score based on price comparison"""
        savings = market_price - list_price
        savings_percent = (savings / list_price) * 100
        
        if savings_percent > 5:
            return {"score": "Excellent", "color": "green", "description": "Great value deal"}
        elif savings_percent > 0:
            return {"score": "Good", "color": "blue", "description": "Fair market value"}
        elif savings_percent > -5:
            return {"score": "Fair", "color": "orange", "description": "Slightly above market"}
        else:
            return {"score": "Overpriced", "color": "red", "description": "Above market value"}
    
    def generate_price_recommendation(self, deal_score: Dict[str, str], list_price: int, market_price: int) -> Dict[str, Any]:
        """Generate pricing recommendation"""
        difference = market_price - list_price
        
        if difference > 50000:
            return {
                "action": "buy_immediately",
                "message": f"Excellent deal! Car is priced ₹{abs(difference):,} below market value.",
                "confidence": "high",
                "urgency": "high"
            }
        elif difference > 0:
            return {
                "action": "proceed",
                "message": f"Good value at ₹{abs(difference):,} below market price.",
                "confidence": "high",
                "urgency": "medium"
            }
        elif abs(difference) < 50000:
            return {
                "action": "proceed",
                "message": "Pricing is fair and aligned with current market rates.",
                "confidence": "medium",
                "urgency": "low"
            }
        else:
            return {
                "action": "negotiate",
                "message": f"Consider negotiating. Car is priced ₹{abs(difference):,} above market value.",
                "confidence": "high",
                "urgency": "low"
            }
    
    def generate_market_summary(self, cars: List[Dict[str, Any]], criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Generate market summary for the search results"""
        if not cars:
            return {"message": "No cars to analyze"}
        
        market_values = [car["market_value"] for car in cars]
        list_prices = [car["price"] for car in cars]
        
        avg_market_value = sum(market_values) // len(market_values)
        avg_list_price = sum(list_prices) // len(list_prices)
        
        # Find best deal
        best_deal = None
        best_savings = 0
        for car in cars:
            savings = car["market_value"] - car["price"]
            if savings > best_savings:
                best_savings = savings
                best_deal = car
        
        # Market trend analysis
        total_variance = sum([car["price_analysis"]["variance_percent"] for car in cars]) / len(cars)
        
        if total_variance > 2:
            trend = "Buyer's market - prices below market value"
        elif total_variance < -2:
            trend = "Seller's market - prices above market value"
        else:
            trend = "Balanced market - fair pricing"
        
        return {
            "average_market_value": avg_market_value,
            "average_list_price": avg_list_price,
            "price_range": {
                "min": min(market_values),
                "max": max(market_values)
            },
            "best_deal": {
                "car": f"{best_deal['make']} {best_deal['model']}" if best_deal else None,
                "savings": best_savings if best_deal else 0
            } if best_deal else None,
            "market_trend": trend,
            "average_variance": round(total_variance, 1),
            "recommendation": self._get_market_recommendation(total_variance, criteria)
        }
    
    def _get_market_recommendation(self, variance: float, criteria: Dict[str, Any]) -> str:
        """Get market-level recommendation"""
        if variance > 3:
            return "Great time to buy - multiple vehicles priced below market value"
        elif variance < -3:
            return "Consider waiting or expanding search - current options are overpriced"
        else:
            return "Normal market conditions - focus on features and financing options"
    
    def _initialize_pricing_model(self) -> Dict[str, Any]:
        """Initialize pricing model parameters"""
        return {
            "depreciation": {
                "year1": 0.15,
                "year2": 0.12,
                "year3": 0.10,
                "yearly_after": 0.08
            },
            "brand_multipliers": {
                "Tata": 1.02,
                "Hyundai": 1.03,
                "MG": 0.99,
                "Mahindra": 1.01,
                "Maruti": 1.025
            },
            "fuel_type_adjustments": {
                "Electric": 1.05,
                "Petrol": 1.01,
                "Diesel": 0.98,
                "CNG": 1.02
            }
        }