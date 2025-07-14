import re
from typing import Dict, List, Tuple

class FinancialService:
    def __init__(self):
        self.categories = {
            'budget': ['budget', 'budgeting', 'spending', 'expenses', 'income'],
            'savings': ['save', 'saving', 'savings', 'emergency fund'],
            'investment': ['invest', 'investment', 'stocks', 'portfolio', 'returns'],
            'debt': ['debt', 'loan', 'credit', 'payment', 'payoff'],
            'general': ['help', 'advice', 'financial', 'money', 'finance']
        }
    
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
            'needs': income * 0.5,
            'wants': income * 0.3,
            'savings': income * 0.2
        }
    
    def calculate_emergency_fund(self, monthly_expenses: float) -> Dict:
        """Calculate emergency fund recommendations"""
        return {
            'minimum': monthly_expenses * 3,
            'recommended': monthly_expenses * 6,
            'ideal': monthly_expenses * 12
        }