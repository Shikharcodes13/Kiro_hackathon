from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

class QueryRequest(BaseModel):
    query: str = Field(..., description="User query to process")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Additional context")
    user_id: Optional[str] = Field(default=None, description="User identifier")

class AgentTrace(BaseModel):
    agent: str
    timestamp: str
    action: str
    output: str

class AgentResponse(BaseModel):
    session_id: str
    result: Dict[str, Any]
    agent_trace: List[AgentTrace]
    success: bool
    error: Optional[str] = None

class Car(BaseModel):
    id: str
    make: str
    model: str
    year: int
    price: int
    fuel_type: str
    location: str
    rating: float
    features: List[str]
    market_value: Optional[int] = None
    price_analysis: Optional[Dict[str, Any]] = None
    deal_score: Optional[Dict[str, str]] = None

class SearchCriteria(BaseModel):
    max_price: Optional[int] = None
    fuel_type: Optional[str] = None
    location: Optional[str] = None
    make: Optional[str] = None
    year_min: Optional[int] = None

class LoanOption(BaseModel):
    lender_name: str
    interest_rate: float
    tenure: int
    down_payment: int
    loan_amount: int
    emi: int
    total_payment: int
    processing_fee: int
    special_offers: List[Dict[str, str]]

class FinancingOptions(BaseModel):
    car_id: str
    car_name: str
    loan_options: List[LoanOption]
    eligibility_check: Dict[str, Any]
    subsidies: List[Dict[str, Any]]

class MarketInsight(BaseModel):
    type: str
    title: str
    content: str
    impact: str

class AgentCapability(BaseModel):
    name: str
    description: str
    capabilities: List[str]
    status: str = "active"