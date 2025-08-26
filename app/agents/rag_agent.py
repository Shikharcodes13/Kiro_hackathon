from typing import Dict, List, Any
import json
import os

# LangChain imports with fallback handling
try:
    from langchain.agents import Tool, AgentExecutor, create_react_agent
    from langchain.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain.memory import ConversationBufferMemory
    from langchain.schema import Document
    from langchain.vectorstores import FAISS
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    print("LangChain not available, using fallback implementation")
    LANGCHAIN_AVAILABLE = False

class RagAgent:
    def __init__(self, llm_model: str = "gpt-3.5-turbo"):
        self.name = "RAG Agent"
        self.knowledge_base = self._initialize_knowledge_base()
        
        # Initialize LangChain components if available
        if LANGCHAIN_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.llm = ChatOpenAI(model=llm_model, temperature=0.1, api_key=api_key)
                self.embeddings = OpenAIEmbeddings(api_key=api_key)
                self.memory = ConversationBufferMemory(return_messages=True)
                self.vector_store = self._create_vector_store()
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
        """Enhance car data with knowledge base information"""
        cars = input_data.get("cars", [])
        criteria = input_data.get("criteria", {})
        
        # Try LangChain RAG first if available
        if self.agent_executor and self.llm:
            try:
                return await self._process_with_langchain_rag(input_data, params)
            except Exception as e:
                print(f"LangChain RAG processing failed: {e}, falling back to direct processing")
        
        # Fallback to direct processing
        enhanced_cars = await self.enhance_with_knowledge(cars, criteria)
        insights = self.generate_market_insights(enhanced_cars, criteria)
        
        return {
            **input_data,
            "cars": enhanced_cars,
            "action": "knowledge_enhancement",
            "summary": f"Enhanced {len(cars)} cars with market intelligence and expert insights",
            "insights": insights
        }
    
    async def enhance_with_knowledge(self, cars: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Enhance car data with knowledge base information"""
        enhanced_cars = []
        
        for car in cars:
            knowledge = self.get_car_knowledge(car)
            enhanced_car = {
                **car,
                "market_position": knowledge["market_position"],
                "expert_review": knowledge["expert_review"],
                "competitor_comparison": knowledge["competitor_comparison"],
                "resale_value": knowledge["resale_value"],
                "common_issues": knowledge["common_issues"],
                "best_features": knowledge["best_features"],
                "ownership_cost": knowledge.get("ownership_cost", {}),
                "safety_rating": knowledge.get("safety_rating", "Not rated")
            }
            enhanced_cars.append(enhanced_car)
        
        return enhanced_cars
    
    def get_car_knowledge(self, car: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve knowledge for specific car"""
        car_key = f"{car['make']}_{car['model']}".lower().replace(" ", "_")
        return self.knowledge_base.get(car_key, self.knowledge_base["default"])
    
    def generate_market_insights(self, cars: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate market insights based on search criteria and results"""
        insights = []
        
        # EV market insights
        if criteria.get("fuel_type") == "Electric":
            insights.append({
                "type": "market_trend",
                "title": "EV Market Growth",
                "content": "Electric vehicle sales in India grew 168% in 2023. Government subsidies make EVs 20-30% more affordable through FAME II scheme.",
                "impact": "positive",
                "relevance": "high"
            })
            
            insights.append({
                "type": "technology",
                "title": "Charging Infrastructure",
                "content": "India now has 12,000+ public charging stations with rapid expansion planned. Home charging solutions becoming more affordable.",
                "impact": "positive",
                "relevance": "high"
            })
        
        # Location-specific insights
        location = criteria.get("location")
        if location == "Delhi":
            insights.append({
                "type": "location_specific",
                "title": "Delhi EV Benefits",
                "content": "Delhi offers additional ₹30,000 subsidy for EVs, exemption from odd-even rule, and 1,800+ charging stations with 18,000 planned by 2024.",
                "impact": "positive",
                "relevance": "high"
            })
        elif location == "Mumbai":
            insights.append({
                "type": "location_specific", 
                "title": "Mumbai Market Dynamics",
                "content": "Mumbai has premium pricing but better financing options. Strong resale market and growing EV infrastructure.",
                "impact": "neutral",
                "relevance": "medium"
            })
        
        # Price segment insights
        if criteria.get("max_price"):
            max_price = criteria["max_price"]
            if max_price <= 1500000:  # Under 15L
                insights.append({
                    "type": "price_segment",
                    "title": "Compact EV Segment",
                    "content": "Most competitive EV segment with 5+ options. Expect 300-400km range and fast charging as standard.",
                    "impact": "positive",
                    "relevance": "high"
                })
        
        # Brand insights based on search results
        brands_found = list(set([car["make"] for car in cars]))
        if "Tata" in brands_found:
            insights.append({
                "type": "brand_insight",
                "title": "Tata Motors EV Leadership",
                "content": "Tata leads Indian EV market with 70% share. Strong after-sales network and proven reliability in Indian conditions.",
                "impact": "positive",
                "relevance": "high"
            })
        
        return insights
    
    def _initialize_knowledge_base(self) -> Dict[str, Dict[str, Any]]:
        """Initialize the knowledge base with car information"""
        return {
            "tata_nexon_ev": {
                "market_position": "Market leader in compact EV segment with 70% market share",
                "expert_review": "Best value for money EV with proven reliability and extensive service network",
                "competitor_comparison": "Better build quality than MG ZS EV, more affordable than Hyundai Kona Electric",
                "resale_value": "75% retention after 3 years (excellent for EV segment)",
                "common_issues": ["Software updates needed occasionally", "Charging port cover durability", "Infotainment lag"],
                "best_features": ["Zaptec fast charging technology", "JTP performance variant", "Proven ICE platform adaptation"],
                "ownership_cost": {
                    "maintenance_per_year": 15000,
                    "insurance_premium": 45000,
                    "charging_cost_per_km": 1.2
                },
                "safety_rating": "5-star Global NCAP"
            },
            "mg_zs_ev": {
                "market_position": "Premium compact EV focused on technology and features",
                "expert_review": "Best-in-class technology features with longest claimed range in segment",
                "competitor_comparison": "More tech features than Nexon EV, better range than Kona Electric, premium pricing",
                "resale_value": "70% retention after 3 years (good for premium EV)",
                "common_issues": ["Limited service network", "Software can be laggy", "Higher maintenance costs"],
                "best_features": ["AI voice assistant", "Largest touchscreen in segment", "419km ARAI range"],
                "ownership_cost": {
                    "maintenance_per_year": 18000,
                    "insurance_premium": 48000,
                    "charging_cost_per_km": 1.1
                },
                "safety_rating": "5-star ASEAN NCAP"
            },
            "hyundai_kona_electric": {
                "market_position": "Premium global EV with established international presence",
                "expert_review": "Most refined driving experience with premium interior and smooth ride quality",
                "competitor_comparison": "Most premium option but highest priced, better build quality than MG",
                "resale_value": "72% retention after 3 years (good, supported by brand value)",
                "common_issues": ["Higher maintenance costs", "Limited color options", "Premium parts pricing"],
                "best_features": ["Premium interior materials", "Smooth and quiet ride", "Comprehensive warranty coverage"],
                "ownership_cost": {
                    "maintenance_per_year": 22000,
                    "insurance_premium": 52000,
                    "charging_cost_per_km": 1.3
                },
                "safety_rating": "Not tested by Indian agencies"
            },
            "tata_harrier": {
                "market_position": "Premium SUV segment leader with strong brand presence",
                "expert_review": "Excellent build quality and road presence, ideal for highway driving",
                "competitor_comparison": "Better value than Mahindra XUV700, more premium than Jeep Compass",
                "resale_value": "68% retention after 3 years (good for diesel SUV)",
                "common_issues": ["Fuel efficiency could be better", "Rear seat space", "Infotainment responsiveness"],
                "best_features": ["Commanding road presence", "Premium interior", "Excellent ride quality"],
                "ownership_cost": {
                    "maintenance_per_year": 25000,
                    "insurance_premium": 55000,
                    "fuel_cost_per_km": 6.5
                },
                "safety_rating": "5-star Global NCAP"
            },
            "hyundai_creta": {
                "market_position": "Compact SUV segment leader with consistent sales performance",
                "expert_review": "Well-rounded package with good features, reliability, and resale value",
                "competitor_comparison": "Better features than Kia Seltos, more reliable than MG Hector",
                "resale_value": "78% retention after 3 years (excellent)",
                "common_issues": ["Road noise at high speeds", "Rear AC vents placement", "Touch controls sensitivity"],
                "best_features": ["Feature-rich cabin", "Smooth engine options", "Strong resale value"],
                "ownership_cost": {
                    "maintenance_per_year": 20000,
                    "insurance_premium": 42000,
                    "fuel_cost_per_km": 5.8
                },
                "safety_rating": "4-star Global NCAP"
            },
            "default": {
                "market_position": "Analyzing market position based on segment and competition...",
                "expert_review": "Gathering expert opinions and user feedback...",
                "competitor_comparison": "Comparing with similar vehicles in segment...",
                "resale_value": "Calculating resale projections based on brand and segment...",
                "common_issues": ["Gathering user feedback and reliability data..."],
                "best_features": ["Identifying key strengths and unique selling points..."],
                "ownership_cost": {
                    "maintenance_per_year": 20000,
                    "insurance_premium": 45000,
                    "fuel_cost_per_km": 5.0
                },
                "safety_rating": "Rating information being gathered..."
            }
        }    
def _create_vector_store(self):
        """Create vector store from knowledge base"""
        if not LANGCHAIN_AVAILABLE:
            return None
        
        try:
            # Convert knowledge base to documents
            documents = []
            for car_key, knowledge in self.knowledge_base.items():
                if car_key == "default":
                    continue
                
                # Create comprehensive document for each car
                content = f"""
                Car: {car_key.replace('_', ' ').title()}
                Market Position: {knowledge['market_position']}
                Expert Review: {knowledge['expert_review']}
                Competitor Comparison: {knowledge['competitor_comparison']}
                Resale Value: {knowledge['resale_value']}
                Common Issues: {', '.join(knowledge['common_issues'])}
                Best Features: {', '.join(knowledge['best_features'])}
                Safety Rating: {knowledge.get('safety_rating', 'Not rated')}
                Annual Maintenance Cost: ₹{knowledge.get('ownership_cost', {}).get('maintenance_per_year', 20000)}
                Insurance Premium: ₹{knowledge.get('ownership_cost', {}).get('insurance_premium', 45000)}
                """
                
                doc = Document(
                    page_content=content,
                    metadata={"car": car_key, "type": "car_knowledge"}
                )
                documents.append(doc)
            
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(documents)
            
            # Create vector store
            vector_store = FAISS.from_documents(splits, self.embeddings)
            return vector_store
            
        except Exception as e:
            print(f"Error creating vector store: {e}")
            return None
    
    def _create_langchain_tools(self) -> List:
        """Create LangChain tools for the RAG agent"""
        if not LANGCHAIN_AVAILABLE:
            return []
        
        return [
            Tool(
                name="search_knowledge_base",
                description="Search the automotive knowledge base for car information, market insights, and expert reviews",
                func=self._search_knowledge_base
            ),
            Tool(
                name="get_market_insights",
                description="Get market insights and trends for specific criteria or car segments",
                func=self._get_market_insights_tool
            ),
            Tool(
                name="compare_car_knowledge",
                description="Compare detailed knowledge between multiple cars including pros, cons, and market position",
                func=self._compare_car_knowledge
            ),
            Tool(
                name="get_ownership_costs",
                description="Get detailed ownership cost analysis for cars including maintenance, insurance, and running costs",
                func=self._get_ownership_costs
            )
        ]
    
    def _create_langchain_agent(self):
        """Create the LangChain agent with RAG capabilities"""
        if not LANGCHAIN_AVAILABLE or not self.llm:
            return None
        
        prompt = PromptTemplate.from_template("""
        You are an expert RAG (Retrieval-Augmented Generation) Agent specializing in automotive market intelligence for India. Your role is to:
        1. Enhance car information with comprehensive market knowledge
        2. Provide expert insights and market analysis
        3. Compare vehicles based on real-world data and user experiences
        4. Offer ownership cost analysis and long-term value assessments
        5. Share market trends and industry insights relevant to Indian automotive market
        
        You have access to a comprehensive knowledge base with:
        - Expert reviews and market positioning
        - Ownership costs and maintenance data
        - Safety ratings and reliability information
        - Market trends and competitive analysis
        - User feedback and common issues
        
        Tools available:
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
    
    async def _process_with_langchain_rag(self, input_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Process using LangChain RAG capabilities"""
        cars = input_data.get("cars", [])
        criteria = input_data.get("criteria", {})
        
        # Create query for the RAG agent
        car_names = [f"{car['make']} {car['model']}" for car in cars]
        query = f"Enhance the following cars with market intelligence and expert insights: {', '.join(car_names)}. "
        query += f"Search criteria: {json.dumps(criteria)}"
        
        # Process through LangChain agent
        result = await self.agent_executor.ainvoke({
            "input": query,
            "chat_history": self.memory.chat_memory.messages
        })
        
        # Enhance cars with traditional method as backup
        enhanced_cars = await self.enhance_with_knowledge(cars, criteria)
        
        # Generate insights using both RAG and traditional methods
        rag_insights = self._extract_insights_from_rag_result(result["output"])
        traditional_insights = self.generate_market_insights(enhanced_cars, criteria)
        
        # Combine insights
        all_insights = rag_insights + traditional_insights
        
        return {
            **input_data,
            "cars": enhanced_cars,
            "action": "langchain_rag_enhancement",
            "summary": f"Enhanced {len(cars)} cars using LangChain RAG with comprehensive market intelligence",
            "insights": all_insights,
            "rag_analysis": result["output"],
            "langchain_used": True
        }
    
    def _search_knowledge_base(self, query: str) -> str:
        """Tool function to search the knowledge base"""
        if self.vector_store:
            try:
                # Perform similarity search
                docs = self.vector_store.similarity_search(query, k=3)
                results = []
                for doc in docs:
                    results.append({
                        "content": doc.page_content,
                        "car": doc.metadata.get("car", "unknown")
                    })
                return json.dumps(results, indent=2)
            except Exception as e:
                return f"Error searching knowledge base: {str(e)}"
        else:
            # Fallback to simple text search
            results = []
            query_lower = query.lower()
            for car_key, knowledge in self.knowledge_base.items():
                if car_key == "default":
                    continue
                
                # Simple text matching
                car_text = f"{car_key} {knowledge['market_position']} {knowledge['expert_review']}".lower()
                if any(term in car_text for term in query_lower.split()):
                    results.append({
                        "car": car_key,
                        "knowledge": knowledge
                    })
            
            return json.dumps(results[:3], indent=2)
    
    def _get_market_insights_tool(self, criteria_str: str) -> str:
        """Tool function to get market insights"""
        try:
            criteria = json.loads(criteria_str) if isinstance(criteria_str, str) else {}
        except:
            criteria = {}
        
        insights = self.generate_market_insights([], criteria)
        return json.dumps(insights, indent=2)
    
    def _compare_car_knowledge(self, cars_json: str) -> str:
        """Tool function to compare car knowledge"""
        try:
            cars = json.loads(cars_json) if isinstance(cars_json, str) else []
            
            comparison = {}
            for car in cars:
                car_key = f"{car.get('make', '')}_{car.get('model', '')}".lower().replace(" ", "_")
                knowledge = self.knowledge_base.get(car_key, self.knowledge_base["default"])
                
                comparison[f"{car.get('make', '')} {car.get('model', '')}"] = {
                    "market_position": knowledge["market_position"],
                    "strengths": knowledge["best_features"],
                    "weaknesses": knowledge["common_issues"],
                    "resale_value": knowledge["resale_value"],
                    "ownership_cost": knowledge.get("ownership_cost", {}),
                    "safety_rating": knowledge.get("safety_rating", "Not rated")
                }
            
            return json.dumps(comparison, indent=2)
            
        except Exception as e:
            return f"Error comparing car knowledge: {str(e)}"
    
    def _get_ownership_costs(self, cars_json: str) -> str:
        """Tool function to get ownership cost analysis"""
        try:
            cars = json.loads(cars_json) if isinstance(cars_json, str) else []
            
            cost_analysis = {}
            for car in cars:
                car_key = f"{car.get('make', '')}_{car.get('model', '')}".lower().replace(" ", "_")
                knowledge = self.knowledge_base.get(car_key, self.knowledge_base["default"])
                ownership_cost = knowledge.get("ownership_cost", {})
                
                # Calculate 5-year total cost of ownership
                annual_maintenance = ownership_cost.get("maintenance_per_year", 20000)
                insurance_premium = ownership_cost.get("insurance_premium", 45000)
                
                # Estimate depreciation (assuming 15% first year, 12% subsequent years)
                car_price = car.get("price", 1500000)
                depreciation_5_years = car_price * 0.55  # Approximate 5-year depreciation
                
                total_5_year_cost = (annual_maintenance * 5) + (insurance_premium * 5) + depreciation_5_years
                
                cost_analysis[f"{car.get('make', '')} {car.get('model', '')}"] = {
                    "annual_maintenance": annual_maintenance,
                    "annual_insurance": insurance_premium,
                    "estimated_5_year_depreciation": depreciation_5_years,
                    "total_5_year_ownership_cost": total_5_year_cost,
                    "monthly_running_cost": (annual_maintenance + insurance_premium) / 12,
                    "cost_per_km": ownership_cost.get("fuel_cost_per_km", ownership_cost.get("charging_cost_per_km", 5.0))
                }
            
            return json.dumps(cost_analysis, indent=2)
            
        except Exception as e:
            return f"Error calculating ownership costs: {str(e)}"
    
    def _extract_insights_from_rag_result(self, rag_output: str) -> List[Dict[str, Any]]:
        """Extract insights from RAG agent output"""
        insights = []
        
        # Look for key insights in the RAG output
        if "market" in rag_output.lower():
            insights.append({
                "type": "rag_insight",
                "title": "RAG Market Analysis",
                "content": "Advanced market analysis performed using retrieval-augmented generation",
                "impact": "positive",
                "relevance": "high"
            })
        
        if "cost" in rag_output.lower() or "ownership" in rag_output.lower():
            insights.append({
                "type": "rag_insight",
                "title": "Ownership Cost Analysis",
                "content": "Comprehensive ownership cost analysis including hidden costs and long-term value",
                "impact": "neutral",
                "relevance": "high"
            })
        
        return insights