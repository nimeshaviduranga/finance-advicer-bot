from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.financial_service import FinancialService

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize financial service
financial_service = FinancialService()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Finance Advisor Bot is running!"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Extract numbers from message
        numbers = financial_service.extract_numbers(user_message)
        
        # Categorize the query
        category = financial_service.categorize_query(user_message)
        
        # Generate response based on category and numbers
        response = generate_response(user_message, category, numbers)
        
        return jsonify({
            "response": response,
            "category": category,
            "numbers_found": numbers,
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_response(message: str, category: str, numbers: list) -> str:
    """Generate appropriate response based on category and extracted numbers"""
    
    if category == 'budget':
        if len(numbers) >= 1:
            income = numbers[0]
            budget = financial_service.calculate_budget_50_30_20(income)
            return f"""Based on your income of ${income:,.2f}, here's your 50/30/20 budget breakdown:

💰 Needs (50%): ${budget['needs']:,.2f}
🎯 Wants (30%): ${budget['wants']:,.2f}
💵 Savings (20%): ${budget['savings']:,.2f}

This is a great starting point for managing your finances!"""
        else:
            return "I can help you with budgeting! Please tell me your monthly income. For example: 'My income is $5000'"
    
    elif category == 'savings':
        if len(numbers) >= 1:
            expenses = numbers[0]
            emergency = financial_service.calculate_emergency_fund(expenses)
            return f"""Based on your monthly expenses of ${expenses:,.2f}, here are your emergency fund targets:

🚨 Minimum (3 months): ${emergency['minimum']:,.2f}
✅ Recommended (6 months): ${emergency['recommended']:,.2f}
🏆 Ideal (12 months): ${emergency['ideal']:,.2f}

Start with the minimum and work your way up!"""
        else:
            return "Let's calculate your emergency fund! What are your monthly expenses? For example: 'My monthly expenses are $3000'"
    
    elif category == 'debt':
        if len(numbers) >= 3:
            balance, interest_rate, payment = numbers[0], numbers[1], numbers[2]
            result = financial_service.calculate_debt_payoff(balance, interest_rate, payment)
            
            if "error" in result:
                return f"❌ {result['error']}. Try increasing your monthly payment."
            
            return f"""Debt Payoff Analysis:
💳 Balance: ${balance:,.2f}
📈 Interest Rate: {interest_rate}%
💰 Monthly Payment: ${payment:,.2f}

⏰ Time to pay off: {result['years_to_payoff']} years ({result['months_to_payoff']} months)
💸 Total interest: ${result['total_interest']:,.2f}
💵 Total paid: ${result['total_paid']:,.2f}"""
        else:
            return "I can help with debt payoff! Please provide: balance, interest rate, and monthly payment. For example: 'I have $5000 debt at 18% interest, paying $200 monthly'"
    
    elif category == 'investment':
        if len(numbers) >= 3:
            principal, rate, years = numbers[0], numbers[1], int(numbers[2])
            result = financial_service.calculate_investment_growth(principal, rate, years)
            
            return f"""Investment Growth Projection:
💰 Initial Investment: ${result['initial_amount']:,.2f}
📈 Annual Return: {rate}%
⏰ Time Period: {years} years

🎯 Final Amount: ${result['final_amount']:,.2f}
📊 Total Growth: ${result['total_growth']:,.2f}

Remember: Past performance doesn't guarantee future results!"""
        else:
            return "Let's calculate investment growth! Please provide: amount, expected annual return, and years. For example: 'I want to invest $10000 at 7% return for 10 years'"
    
    else:
        return """Hello! I'm your personal finance advisor. I can help you with:

💰 **Budget Planning** - Tell me your income
💵 **Emergency Fund** - Tell me your monthly expenses  
💳 **Debt Payoff** - Provide balance, interest rate, and payment
📈 **Investment Growth** - Give me amount, return rate, and years

Just type your question with numbers and I'll calculate it for you!"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)