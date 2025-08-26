from typing import Dict, List, Any
import re
import json
import os

# LangChain imports with fallback handling
try:
    from langchain.agents import Tool, AgentExecutor, create_react_agent
    from langchain.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain.memory import ConversationBufferMemory
    LANGCHAIN_AVAILABLE = True
except ImportError:
    print("LangChain not available, using fallback implementation")
    LANGCHAIN_AVAILABLE = False

class BuyerAgent:
    def __init__(self, llm_model: str = "gpt-3.5-turbo"):
        self.name = "Buyer Agent"
        self.capabilities = ["car_search", "financing_options", "test_drive_booking"]
        
        # Initialize LangChain components if available
        if LANGCHAIN_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.llm = ChatOpenAI(model=llm_model, temperature=0.1, api_key=api_key)
                self.memory = ConversationBufferMemory(return_messages=True)
                self.tools = self._create_langchain_tools()
                self.agent_executor = self._create_langchain_agent()
            else:
                print("OpenAI API key not found, using fallback mode")
                self.llm = None
                self.agent_executor = None
        else:
            self.llm = None
            self.agent_executor = None
    
    async def process(self, input_data: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main processing method for buyer agent"""
        query = input_data.get("query", "")
        context = input_data.get("context", {})
        params = params or {}
        
        # Try LangChain agent first if available
        if self.agent_executor and self.llm:
            try:
                return await self._process_with_langchain(query, context, params)
            except Exception as e:
                print(f"LangChain processing failed: {e}, falling back to direct processing")
        
        # Fallback to direct processing
        action = params.get("action", "search")
        
        if action == "search":
            return await self.search_cars(query, context)
        elif action == "general":
            return await self.handle_general_query(query, context)
        else:
            return await self.search_cars(query, context)
    
    async def search_cars(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for cars based on user query"""
        print(f"🤝 Buyer Agent: Analyzing search query '{query}'")
        
        # Extract search criteria from query
        criteria = self.extract_search_criteria(query)
        
        # Find matching cars
        cars = await self.find_matching_cars(criteria)
        
        return {
            **context,
            "action": "car_search",
            "criteria": criteria,
            "cars": cars,
            "summary": f"Found {len(cars)} cars matching your criteria",
            "next_steps": ["Get detailed pricing", "Check financing options", "Book test drive"],
            "reasoning": f"Based on your query '{query}', I identified key criteria: {self._format_criteria(criteria)}"
        }
    
    def extract_search_criteria(self, query: str) -> Dict[str, Any]:
        """Extract search criteria from natural language query"""
        criteria = {}
        
        # Price extraction
        price_patterns = [
            r"under ₹(\d+)L",
            r"below ₹(\d+)L", 
            r"less than ₹(\d+)L",
            r"₹(\d+)L or less"
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                criteria["max_price"] = int(match.group(1)) * 100000
                break
        
        # Vehicle type
        if any(term in query.lower() for term in ["ev", "electric"]):
            criteria["fuel_type"] = "Electric"
        elif any(term in query.lower() for term in ["petrol", "gasoline"]):
            criteria["fuel_type"] = "Petrol"
        elif any(term in query.lower() for term in ["diesel"]):
            criteria["fuel_type"] = "Diesel"
        
        # Location extraction
        location_match = re.search(r"in (\w+)", query, re.IGNORECASE)
        if location_match:
            criteria["location"] = location_match.group(1).title()
        
        # Brand extraction
        brands = ["Tata", "Hyundai", "MG", "Mahindra", "Maruti", "Honda", "Toyota"]
        for brand in brands:
            if brand.lower() in query.lower():
                criteria["make"] = brand
                break
        
        return criteria
    
    async def find_matching_cars(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find cars matching the search criteria"""
        # Mock car database
        mock_cars = [
            {
                "id": "car_001",
                "make": "Tata",
                "model": "Nexon EV",
                "year": 2023,
                "price": 1400000,
                "fuel_type": "Electric",
                "location": "Delhi",
                "rating": 4.2,
                "features": ["Fast Charging", "Connected Car Tech", "312km Range"]
            },
            {
                "id": "car_002", 
                "make": "MG",
                "model": "ZS EV",
                "year": 2023,
                "price": 1350000,
                "fuel_type": "Electric",
                "location": "Delhi",
                "rating": 4.0,
                "features": ["AI Assistant", "419km Range", "Panoramic Sunroof"]
            },
            {
                "id": "car_003",
                "make": "Hyundai", 
                "model": "Kona Electric",
                "year": 2022,
                "price": 1450000,
                "fuel_type": "Electric",
                "location": "Delhi",
                "rating": 4.3,
                "features": ["Premium Interior", "452km Range", "Wireless Charging"]
            },
            {
                "id": "car_004",
                "make": "Tata",
                "model": "Harrier",
                "year": 2023,
                "price": 1600000,
                "fuel_type": "Diesel",
                "location": "Mumbai",
                "rating": 4.1,
                "features": ["Panoramic Sunroof", "JBL Audio", "Terrain Modes"]
            },
            {
                "id": "car_005",
                "make": "Hyundai",
                "model": "Creta",
                "year": 2023,
                "price": 1200000,
                "fuel_type": "Petrol",
                "location": "Bangalore",
                "rating": 4.4,
                "features": ["Ventilated Seats", "Wireless Charging", "BlueLink"]
            }
        ]
        
        # Filter cars based on criteria
        filtered_cars = []
        for car in mock_cars:
            if self._matches_criteria(car, criteria):
                filtered_cars.append(car)
        
        # Sort by rating and return top 3
        filtered_cars.sort(key=lambda x: x["rating"], reverse=True)
        return filtered_cars[:3]
    
    def _matches_criteria(self, car: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if car matches search criteria"""
        if criteria.get("max_price") and car["price"] > criteria["max_price"]:
            return False
        
        if criteria.get("fuel_type") and car["fuel_type"] != criteria["fuel_type"]:
            return False
        
        if criteria.get("location") and car["location"] != criteria["location"]:
            return False
        
        if criteria.get("make") and car["make"] != criteria["make"]:
            return False
        
        return True
    
    def _format_criteria(self, criteria: Dict[str, Any]) -> str:
        """Format criteria for display"""
        formatted = []
        for key, value in criteria.items():
            if key == "max_price":
                formatted.append(f"Budget: ₹{value//100000}L")
            else:
                formatted.append(f"{key.replace('_', ' ').title()}: {value}")
        return ", ".join(formatted)
    
    async def handle_general_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general queries and provide assistance"""
        return {
            **context,
            "action": "general_assistance",
            "response": "I'm here to help you find the perfect car! I can assist with car search, financing options, and booking test drives.",
            "suggestions": [
                "Search for cars by budget and location",
                "Compare financing options", 
                "Book test drives",
                "Get market insights"
            ],
            "summary": "Provided general assistance and suggestions"
        } 
   def _create_langchain_tools(self) -> List:
        """Create LangChain tools for the buyer agent"""
        if not LANGCHAIN_AVAILABLE:
            return []
        
        return [
            Tool(
                name="search_cars_tool",
                description="Search for cars based on criteria like price, fuel type, location. Input should be JSON string with criteria.",
                func=self._langchain_search_cars
            ),
            Tool(
                name="extract_criteria_tool", 
                description="Extract search criteria from user query. Input should be the user query string.",
                func=self._langchain_extract_criteria
            ),
            Tool(
                name="compare_cars_tool",
                description="Compare multiple cars based on features and value. Input should be JSON array of cars.",
                func=self._langchain_compare_cars
            ),
            Tool(
                name="get_recommendations_tool",
                description="Get personalized car recommendations. Input should be user profile or preferences.",
                func=self._langchain_get_recommendations
            )
        ]
    
    def _create_langchain_agent(self):
        """Create the LangChain agent with tools and prompt"""
        if not LANGCHAIN_AVAILABLE or not self.llm:
            return None
        
        prompt = PromptTemplate.from_template("""
        You are a helpful Buyer Agent specializing in automotive purchases in India. Your role is to:
        1. Help users find the perfect car based on their needs and budget
        2. Provide detailed comparisons and recommendations with Indian market context
        3. Explain your reasoning clearly with market insights
        4. Guide users through the car buying process
        5. Consider Indian-specific factors like fuel prices, road conditions, and government policies
        
        You have access to the following tools:
        {tools}
        
        Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        Question: {input}
        Thought: {agent_scratchpad}
        """)
        
        agent = create_react_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True, max_iterations=5)
    
    async def _process_with_langchain(self, query: str, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Process using LangChain agent"""
        # Add context to memory
        if context:
            self.memory.chat_memory.add_user_message(f"Context: {json.dumps(context)}")
        
        # Process through LangChain agent
        result = await self.agent_executor.ainvoke({
            "input": query,
            "chat_history": self.memory.chat_memory.messages
        })
        
        # Extract structured data from result
        cars = self._extract_cars_from_langchain_result(result["output"])
        criteria = self.extract_search_criteria(query)
        
        return {
            "action": "car_search_langchain",
            "query": query,
            "criteria": criteria,
            "cars": cars,
            "summary": f"LangChain agent found {len(cars)} cars matching your criteria",
            "reasoning": result["output"],
            "next_steps": ["Get detailed pricing", "Check financing options", "Book test drive"],
            "agent_response": result["output"],
            "langchain_used": True
        }
    
    def _langchain_search_cars(self, criteria_str: str) -> str:
        """LangChain tool function to search for cars"""
        try:
            criteria = json.loads(criteria_str) if isinstance(criteria_str, str) else criteria_str
        except:
            criteria = self.extract_search_criteria(criteria_str)
        
        # Use existing find_matching_cars method
        import asyncio
        cars = asyncio.run(self.find_matching_cars(criteria))
        
        # Enhanced car data for LangChain
        enhanced_cars = []
        for car in cars:
            enhanced_car = car.copy()
            enhanced_car.update({
                "market_position": self._get_market_position(car),
                "value_proposition": self._get_value_proposition(car),
                "target_audience": self._get_target_audience(car)
            })
            enhanced_cars.append(enhanced_car)
        
        return json.dumps(enhanced_cars, indent=2)
    
    def _langchain_extract_criteria(self, query: str) -> str:
        """LangChain tool function to extract search criteria"""
        criteria = self.extract_search_criteria(query)
        return json.dumps(criteria, indent=2)
    
    def _langchain_compare_cars(self, cars_json: str) -> str:
        """LangChain tool function to compare cars"""
        try:
            cars = json.loads(cars_json)
            if not cars:
                return "No cars to compare"
            
            comparison = {
                "total_cars": len(cars),
                "price_range": {
                    "min": min(car["price"] for car in cars),
                    "max": max(car["price"] for car in cars),
                    "average": sum(car["price"] for car in cars) // len(cars)
                },
                "best_value": min(cars, key=lambda x: x["price"]),
                "highest_rated": max(cars, key=lambda x: x["rating"]),
                "comparison_matrix": [],
                "recommendations": self._generate_comparison_recommendations(cars)
            }
            
            for car in cars:
                comparison["comparison_matrix"].append({
                    "name": f"{car['make']} {car['model']}",
                    "price": car["price"],
                    "rating": car["rating"],
                    "fuel_type": car["fuel_type"],
                    "key_features": car.get("features", [])[:3],
                    "pros": car.get("pros", []),
                    "cons": car.get("cons", [])
                })
            
            return json.dumps(comparison, indent=2)
            
        except Exception as e:
            return f"Error comparing cars: {str(e)}"
    
    def _langchain_get_recommendations(self, user_profile: str) -> str:
        """LangChain tool function to get personalized recommendations"""
        recommendations = {
            "first_time_buyer": {
                "car": "Tata Nexon EV",
                "reason": "Best value, proven reliability, extensive service network"
            },
            "tech_enthusiast": {
                "car": "MG ZS EV", 
                "reason": "Advanced tech features, AI assistant, connected car capabilities"
            },
            "premium_buyer": {
                "car": "Hyundai Kona Electric",
                "reason": "Most refined experience, premium build quality, comprehensive warranty"
            },
            "budget_conscious": {
                "car": "Tata Nexon EV",
                "reason": "Best price-to-feature ratio, government subsidies applicable"
            },
            "range_priority": {
                "car": "Hyundai Kona Electric",
                "reason": "Longest range, excellent efficiency, fast charging capability"
            },
            "family_oriented": {
                "car": "MG ZS EV",
                "reason": "Spacious cabin, safety features, comfortable ride quality"
            }
        }
        
        return json.dumps(recommendations, indent=2)
    
    def _extract_cars_from_langchain_result(self, result_text: str) -> List[Dict[str, Any]]:
        """Extract car data from LangChain agent result"""
        try:
            # Look for JSON arrays in the result
            import re
            json_matches = re.findall(r'\[.*?\]', result_text, re.DOTALL)
            for match in json_matches:
                try:
                    cars = json.loads(match)
                    if isinstance(cars, list) and cars and isinstance(cars[0], dict):
                        return cars
                except:
                    continue
        except:
            pass
        
        # Fallback: extract car information from text
        return self._extract_cars_from_text(result_text)
    
    def _extract_cars_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract car information from text when JSON parsing fails"""
        cars = []
        # This is a simplified extraction - in a real implementation, 
        # you'd use more sophisticated NLP techniques
        if "Nexon EV" in text:
            cars.append({
                "id": "car_001",
                "make": "Tata",
                "model": "Nexon EV",
                "price": 1400000,
                "fuel_type": "Electric"
            })
        if "ZS EV" in text:
            cars.append({
                "id": "car_002", 
                "make": "MG",
                "model": "ZS EV",
                "price": 1350000,
                "fuel_type": "Electric"
            })
        if "Kona Electric" in text:
            cars.append({
                "id": "car_003",
                "make": "Hyundai",
                "model": "Kona Electric", 
                "price": 1450000,
                "fuel_type": "Electric"
            })
        return cars
    
    def _get_market_position(self, car: Dict[str, Any]) -> str:
        """Get market position for a car"""
        positions = {
            "Tata Nexon EV": "Market leader in affordable EV segment",
            "MG ZS EV": "Premium tech-focused EV with longest range",
            "Hyundai Kona Electric": "Premium EV with global pedigree"
        }
        car_name = f"{car['make']} {car['model']}"
        return positions.get(car_name, "Competitive player in segment")
    
    def _get_value_proposition(self, car: Dict[str, Any]) -> str:
        """Get value proposition for a car"""
        propositions = {
            "Tata Nexon EV": "Best value for money with proven reliability",
            "MG ZS EV": "Premium features and technology at competitive price",
            "Hyundai Kona Electric": "Premium experience with comprehensive warranty"
        }
        car_name = f"{car['make']} {car['model']}"
        return propositions.get(car_name, "Good value in its segment")
    
    def _get_target_audience(self, car: Dict[str, Any]) -> str:
        """Get target audience for a car"""
        audiences = {
            "Tata Nexon EV": "First-time EV buyers, budget-conscious families",
            "MG ZS EV": "Tech enthusiasts, young professionals",
            "Hyundai Kona Electric": "Premium buyers, brand-conscious customers"
        }
        car_name = f"{car['make']} {car['model']}"
        return audiences.get(car_name, "General car buyers")
    
    def _generate_comparison_recommendations(self, cars: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate recommendations based on car comparison"""
        if not cars:
            return {}
        
        recommendations = {}
        
        # Best value recommendation
        cheapest = min(cars, key=lambda x: x["price"])
        recommendations["best_value"] = f"{cheapest['make']} {cheapest['model']} offers the best value at ₹{cheapest['price']//100000}L"
        
        # Best rated recommendation
        highest_rated = max(cars, key=lambda x: x["rating"])
        recommendations["highest_rated"] = f"{highest_rated['make']} {highest_rated['model']} has the highest rating of {highest_rated['rating']}/5"
        
        # Feature recommendation
        if any(car.get("fuel_type") == "Electric" for car in cars):
            recommendations["eco_friendly"] = "All these electric vehicles qualify for government subsidies and have zero emissions"
        
        return recommendations