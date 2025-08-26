from typing import Dict, List, Any
import math

class LoanAgent:
    def __init__(self):
        self.name = "Loan Agent"
        self.lenders = self._initialize_lenders()
    
    async def process(self, input_data: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main processing method for loan agent"""
        cars = input_data.get("cars", [])
        criteria = input_data.get("criteria", {})
        
        financing_options = await self.generate_financing_options(cars, criteria)
        recommendation = self.generate_financing_recommendation(financing_options)
        
        return {
            **input_data,
            "financing_options": financing_options,
            "action": "financing_analysis",
            "summary": f"Generated financing options for {len(cars)} vehicles across {len(self.lenders)} lenders",
            "financing_recommendation": recommendation
        }
    
    async def generate_financing_options(self, cars: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate financing options for each car"""
        financing_options = []
        
        for car in cars:
            car_financing = {
                "car_id": car["id"],
                "car_name": f"{car['make']} {car['model']}",
                "car_price": car.get("market_value", car["price"]),
                "loan_options": self.calculate_loan_options(car),
                "eligibility_check": self.perform_eligibility_check(car),
                "subsidies": self.check_subsidies(car),
                "total_cost_analysis": self.calculate_total_cost(car)
            }
            financing_options.append(car_financing)
        
        return financing_options
    
    def calculate_loan_options(self, car: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate loan options from different lenders"""
        loan_amount = car.get("market_value", car["price"])
        loan_options = []
        
        for lender in self.lenders:
            # Calculate down payment (typically 10-20%)
            down_payment_percent = lender.get("min_down_payment", 0.15)
            down_payment = loan_amount * down_payment_percent
            principal_amount = loan_amount - down_payment
            
            # Calculate EMI
            emi = self.calculate_emi(principal_amount, lender["interest_rate"], lender["tenure"])
            total_payment = emi * lender["tenure"]
            total_interest = total_payment - principal_amount
            
            loan_option = {
                "lender_name": lender["name"],
                "interest_rate": lender["interest_rate"],
                "tenure_months": lender["tenure"],
                "tenure_years": lender["tenure"] // 12,
                "max_loan_amount": lender["max_loan_amount"],
                "down_payment": round(down_payment),
                "loan_amount": round(principal_amount),
                "emi": round(emi),
                "total_payment": round(total_payment),
                "total_interest": round(total_interest),
                "processing_fee": lender["processing_fee"],
                "special_offers": self.get_special_offers(lender, car),
                "eligibility_score": self.calculate_eligibility_score(lender, car)
            }
            loan_options.append(loan_option)
        
        # Sort by EMI (ascending)
        loan_options.sort(key=lambda x: x["emi"])
        return loan_options
    
    def calculate_emi(self, principal: float, annual_rate: float, tenure_months: int) -> float:
        """Calculate EMI using standard formula"""
        monthly_rate = annual_rate / (12 * 100)
        if monthly_rate == 0:
            return principal / tenure_months
        
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
              ((1 + monthly_rate) ** tenure_months - 1)
        return emi
    
    def perform_eligibility_check(self, car: Dict[str, Any]) -> Dict[str, Any]:
        """Perform loan eligibility check"""
        car_price = car.get("market_value", car["price"])
        
        # Calculate required income (EMI should not exceed 40% of income)
        min_emi = min([self.calculate_emi(car_price * 0.8, 9.0, 84) for _ in range(1)])
        required_monthly_income = min_emi / 0.4
        required_annual_income = required_monthly_income * 12
        
        return {
            "status": "pre_approved",
            "required_monthly_income": round(required_monthly_income),
            "required_annual_income": round(required_annual_income),
            "credit_score_required": 650,
            "employment_type": ["Salaried", "Self-employed", "Business"],
            "documents_needed": [
                "Income proof (3 months salary slips/ITR)",
                "Bank statements (6 months)",
                "Identity proof (Aadhar/PAN)",
                "Address proof",
                "Car quotation/proforma invoice",
                "Employment certificate"
            ],
            "processing_time": "24-48 hours",
            "approval_probability": "85%"
        }
    
    def check_subsidies(self, car: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check available subsidies and incentives"""
        subsidies = []
        
        # Electric vehicle subsidies
        if car["fuel_type"] == "Electric":
            subsidies.append({
                "name": "FAME II Central Subsidy",
                "amount": 150000,
                "description": "Central government incentive for electric vehicles",
                "eligibility": "All EVs under ₹15L ex-showroom price",
                "claim_process": "Dealer will adjust at time of purchase"
            })
            
            # State-specific subsidies
            if car["location"] == "Delhi":
                subsidies.append({
                    "name": "Delhi EV Policy Incentive",
                    "amount": 30000,
                    "description": "Additional Delhi state subsidy for EVs",
                    "eligibility": "Delhi registration required",
                    "claim_process": "Apply online after vehicle registration"
                })
            elif car["location"] == "Maharashtra":
                subsidies.append({
                    "name": "Maharashtra EV Policy",
                    "amount": 25000,
                    "description": "Maharashtra state EV incentive",
                    "eligibility": "Maharashtra registration required",
                    "claim_process": "Apply through state transport department"
                })
            
            # Corporate tax benefits
            subsidies.append({
                "name": "Income Tax Benefit",
                "amount": 150000,
                "description": "Additional tax deduction under Section 80EEB",
                "eligibility": "For loan taken for EV purchase",
                "claim_process": "Claim during ITR filing"
            })
        
        # CNG subsidies
        elif car["fuel_type"] == "CNG":
            subsidies.append({
                "name": "CNG Conversion Subsidy",
                "amount": 20000,
                "description": "Subsidy for CNG kit installation",
                "eligibility": "Factory-fitted CNG vehicles",
                "claim_process": "Dealer adjustment"
            })
        
        return subsidies
    
    def calculate_total_cost(self, car: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate total cost of ownership"""
        car_price = car.get("market_value", car["price"])
        
        # Get the best loan option (lowest EMI)
        loan_options = self.calculate_loan_options(car)
        best_loan = min(loan_options, key=lambda x: x["emi"]) if loan_options else None
        
        if not best_loan:
            return {"error": "No loan options available"}
        
        # Calculate 5-year ownership costs
        ownership_costs = {
            "car_price": car_price,
            "down_payment": best_loan["down_payment"],
            "total_loan_payment": best_loan["total_payment"],
            "insurance_5_years": self.calculate_insurance_cost(car, 5),
            "maintenance_5_years": self.calculate_maintenance_cost(car, 5),
            "fuel_cost_5_years": self.calculate_fuel_cost(car, 5),
            "registration_charges": 50000,
            "depreciation_5_years": round(car_price * 0.4)  # 40% depreciation
        }
        
        total_cost = sum([
            ownership_costs["total_loan_payment"],
            ownership_costs["insurance_5_years"],
            ownership_costs["maintenance_5_years"],
            ownership_costs["fuel_cost_5_years"],
            ownership_costs["registration_charges"]
        ])
        
        ownership_costs["total_5_year_cost"] = total_cost
        ownership_costs["monthly_average"] = round(total_cost / 60)  # 5 years = 60 months
        
        return ownership_costs
    
    def calculate_insurance_cost(self, car: Dict[str, Any], years: int) -> int:
        """Calculate insurance cost over specified years"""
        car_price = car.get("market_value", car["price"])
        annual_premium = car_price * 0.03  # 3% of car value
        
        # Premium decreases each year due to depreciation
        total_premium = 0
        for year in range(years):
            yearly_premium = annual_premium * (0.95 ** year)  # 5% reduction each year
            total_premium += yearly_premium
        
        return round(total_premium)
    
    def calculate_maintenance_cost(self, car: Dict[str, Any], years: int) -> int:
        """Calculate maintenance cost over specified years"""
        base_maintenance = {
            "Electric": 15000,
            "Petrol": 25000,
            "Diesel": 30000,
            "CNG": 28000
        }
        
        annual_cost = base_maintenance.get(car["fuel_type"], 25000)
        
        # Maintenance cost increases each year
        total_cost = 0
        for year in range(years):
            yearly_cost = annual_cost * (1.1 ** year)  # 10% increase each year
            total_cost += yearly_cost
        
        return round(total_cost)
    
    def calculate_fuel_cost(self, car: Dict[str, Any], years: int) -> int:
        """Calculate fuel/charging cost over specified years"""
        annual_km = 12000  # Average annual driving
        
        cost_per_km = {
            "Electric": 1.5,  # ₹1.5 per km for electricity
            "Petrol": 6.0,    # ₹6 per km for petrol
            "Diesel": 5.5,    # ₹5.5 per km for diesel
            "CNG": 3.5        # ₹3.5 per km for CNG
        }
        
        per_km_cost = cost_per_km.get(car["fuel_type"], 6.0)
        annual_fuel_cost = annual_km * per_km_cost
        
        # Fuel prices increase over time
        total_cost = 0
        for year in range(years):
            yearly_cost = annual_fuel_cost * (1.05 ** year)  # 5% annual increase
            total_cost += yearly_cost
        
        return round(total_cost)
    
    def get_special_offers(self, lender: Dict[str, Any], car: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get special offers from lenders"""
        offers = []
        
        # EV-specific offers
        if car["fuel_type"] == "Electric":
            offers.append({
                "title": "Green Car Loan",
                "benefit": "0.5% interest rate reduction",
                "description": "Special rate for eco-friendly vehicles",
                "validity": "Limited time offer"
            })
        
        # Lender-specific offers
        if lender["name"] == "HDFC Bank":
            offers.append({
                "title": "Pre-approved Customer Benefit",
                "benefit": "Zero processing fee",
                "description": "For existing HDFC Bank customers",
                "validity": "Ongoing"
            })
        elif lender["name"] == "ICICI Bank":
            offers.append({
                "title": "Salary Account Holder",
                "benefit": "0.25% rate reduction",
                "description": "For ICICI salary account holders",
                "validity": "Ongoing"
            })
        
        # Festival offers (seasonal)
        offers.append({
            "title": "Festival Special",
            "benefit": "Cashback up to ₹10,000",
            "description": "Special festival season offer",
            "validity": "Till month end"
        })
        
        return offers
    
    def calculate_eligibility_score(self, lender: Dict[str, Any], car: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate eligibility score for the loan"""
        # Mock eligibility scoring
        base_score = 75
        
        # Adjust based on car price
        car_price = car.get("market_value", car["price"])
        if car_price < 1000000:
            base_score += 10
        elif car_price > 2000000:
            base_score -= 5
        
        # Adjust based on fuel type
        if car["fuel_type"] == "Electric":
            base_score += 5  # Banks prefer EVs
        
        return {
            "score": min(base_score, 95),
            "rating": "High" if base_score > 80 else "Medium" if base_score > 60 else "Low",
            "approval_probability": f"{min(base_score, 95)}%"
        }
    
    def generate_financing_recommendation(self, financing_options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate overall financing recommendation"""
        if not financing_options:
            return {"error": "No financing options available"}
        
        # Find best deals across all cars
        all_loans = []
        for car_option in financing_options:
            for loan in car_option["loan_options"]:
                all_loans.append({
                    **loan,
                    "car_name": car_option["car_name"],
                    "car_id": car_option["car_id"]
                })
        
        # Best EMI option
        best_emi = min(all_loans, key=lambda x: x["emi"])
        
        # Best interest rate option
        best_rate = min(all_loans, key=lambda x: x["interest_rate"])
        
        # Best total cost option
        best_total = min(all_loans, key=lambda x: x["total_payment"])
        
        return {
            "best_emi_option": {
                "car": best_emi["car_name"],
                "lender": best_emi["lender_name"],
                "emi": best_emi["emi"],
                "reason": "Lowest monthly payment"
            },
            "best_rate_option": {
                "car": best_rate["car_name"],
                "lender": best_rate["lender_name"],
                "rate": best_rate["interest_rate"],
                "reason": "Lowest interest rate"
            },
            "best_total_cost": {
                "car": best_total["car_name"],
                "lender": best_total["lender_name"],
                "total": best_total["total_payment"],
                "reason": "Lowest total payment"
            },
            "tips": [
                "Compare total interest paid, not just EMI",
                "Check for prepayment penalties and charges",
                "Consider loan tenure vs total interest cost",
                "Negotiate processing fees and other charges",
                "Maintain good credit score for better rates"
            ],
            "next_steps": [
                "Choose preferred loan option",
                "Submit loan application with documents",
                "Complete KYC and verification process",
                "Get loan sanction letter",
                "Coordinate with dealer for disbursement"
            ]
        }
    
    def _initialize_lenders(self) -> List[Dict[str, Any]]:
        """Initialize lender database"""
        return [
            {
                "name": "HDFC Bank",
                "interest_rate": 8.5,
                "tenure": 84,  # 7 years
                "max_loan_amount": 5000000,
                "processing_fee": 3500,
                "min_credit_score": 650,
                "min_down_payment": 0.15
            },
            {
                "name": "ICICI Bank",
                "interest_rate": 8.75,
                "tenure": 84,
                "max_loan_amount": 4500000,
                "processing_fee": 2500,
                "min_credit_score": 650,
                "min_down_payment": 0.15
            },
            {
                "name": "Axis Bank",
                "interest_rate": 9.0,
                "tenure": 72,  # 6 years
                "max_loan_amount": 4000000,
                "processing_fee": 3000,
                "min_credit_score": 700,
                "min_down_payment": 0.20
            },
            {
                "name": "Tata Capital",
                "interest_rate": 9.25,
                "tenure": 84,
                "max_loan_amount": 3500000,
                "processing_fee": 2000,
                "min_credit_score": 600,
                "min_down_payment": 0.15
            },
            {
                "name": "Mahindra Finance",
                "interest_rate": 9.5,
                "tenure": 72,
                "max_loan_amount": 3000000,
                "processing_fee": 2500,
                "min_credit_score": 600,
                "min_down_payment": 0.20
            }
        ]