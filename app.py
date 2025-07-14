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
        
        # Categorize the query
        category = financial_service.categorize_query(user_message)
        
        # Generate response based on category
        response = generate_response(user_message, category)
        
        return jsonify({
            "response": response,
            "category": category,
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_response(message: str, category: str) -> str:
    """Generate appropriate response based on category"""
    
    if category == 'budget':
        return "I can help you with budgeting! A popular approach is the 50/30/20 rule. What's your monthly income? I'll calculate a budget breakdown for you."
    
    elif category == 'savings':
        return "Great question about savings! Building an emergency fund is crucial. What are your monthly expenses? I can recommend how much you should save."
    
    elif category == 'investment':
        return "Investment advice coming up! Remember, investments carry risk. Are you looking for long-term growth or short-term gains? What's your risk tolerance?"
    
    elif category == 'debt':
        return "Let's tackle your debt situation! The debt avalanche method (pay highest interest first) or debt snowball (pay smallest balance first) are both effective. What type of debt are you dealing with?"
    
    else:
        return "Hello! I'm your personal finance advisor. I can help you with budgeting, savings, investments, and debt management. What financial topic would you like to discuss?"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)