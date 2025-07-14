import re
from typing import Dict, List, Tuple, Optional

class FinancialService:
    def __init__(self):
        self.categories = {
            'budget': ['budget', 'budgeting', 'spending', 'expenses', 'income'],
            'savings': ['save', 'saving', 'savings', 'emergency fund'],
            'investment': ['invest', 'investment', 'stocks', 'portfolio', 'returns'],
            'debt': ['debt', 'loan', 'credit', 'payment', 'payoff'],
            'general': ['help', 'advice', 'financial', 'money', 'finance']
        }
    
    def extract_numbers(self, text: str) -> List[float]:
        """Extract numbers from text"""
        # Find numbers with optional commas and decimals
        pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'
        matches = re.findall(pattern, text)
        return [float(match.replace(',', '')) for match in matches]
    
    def categorize_query(self, message: str) -> str:
        """Categorize user message into financial topics"""
        message_lower = message.lower()
        
        for category, keywords in self.categories.items():
            if any(keyword in message_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def calculate_budget_50_30_20(self, income: float) -> Dict:
        """Calculate 50/30/20 budget rule"""
        return {
            'needs': round(income * 0.5, 2),
            'wants': round(income * 0.3, 2),
            'savings': round(income * 0.2, 2),
            'total': round(income, 2)
        }
    
    def calculate_emergency_fund(self, monthly_expenses: float) -> Dict:
        """Calculate emergency fund recommendations"""
        return {
            'minimum': round(monthly_expenses * 3, 2),
            'recommended': round(monthly_expenses * 6, 2),
            'ideal': round(monthly_expenses * 12, 2)
        }
    
    def calculate_debt_payoff(self, balance: float, interest_rate: float, monthly_payment: float) -> Dict:
        """Calculate debt payoff time and total interest"""
        if monthly_payment <= (balance * interest_rate / 12 / 100):
            return {"error": "Monthly payment too low to pay off debt"}
        
        months = 0
        remaining = balance
        total_interest = 0
        
        while remaining > 0 and months < 600:  # Max 50 years
            interest_payment = remaining * (interest_rate / 12 / 100)
            principal_payment = min(monthly_payment - interest_payment, remaining)
            
            remaining -= principal_payment
            total_interest += interest_payment
            months += 1
        
        return {
            "months_to_payoff": months,
            "years_to_payoff": round(months / 12, 1),
            "total_interest": round(total_interest, 2),
            "total_paid": round(balance + total_interest, 2)
        }
    
    def calculate_investment_growth(self, principal: float, annual_rate: float, years: int) -> Dict:
        """Calculate compound interest growth"""
        final_amount = principal * (1 + annual_rate/100) ** years
        total_growth = final_amount - principal
        
        return {
            "initial_amount": round(principal, 2),
            "final_amount": round(final_amount, 2),
            "total_growth": round(total_growth, 2),
            "years": years
        }