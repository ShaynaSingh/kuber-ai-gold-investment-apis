from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import json
import re
import requests
from typing import Dict, Any
import uuid
import os

app = Flask(__name__)

# Configuration
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'gold_investments.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('gold_investments.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Gold purchases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gold_purchases (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            amount_inr REAL NOT NULL,
            gold_weight_grams REAL NOT NULL,
            gold_price_per_gram REAL NOT NULL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'completed',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Gold investment knowledge base
GOLD_FACTS = {
    "benefits": [
        "Gold is considered a hedge against inflation and economic uncertainty.",
        "Digital gold allows fractional ownership starting from as low as ₹1.",
        "Gold has historically maintained its value over long periods.",
        "It provides portfolio diversification and reduces overall risk."
    ],
    "digital_gold": [
        "Digital gold is backed by 24K 999.9 pure gold stored in secure vaults.",
        "You can buy, sell, and accumulate digital gold anytime through mobile apps.",
        "No storage concerns, making charges, or security issues with digital gold.",
        "Instant liquidity - convert digital gold to cash within minutes."
    ],
    "investment_tips": [
        "Start small with SIP (Systematic Investment Plan) in gold for regular accumulation.",
        "Gold should typically be 5-10% of your total investment portfolio.",
        "Best time to buy gold is during festivals or market corrections.",
        "Digital gold offers better convenience compared to physical gold."
    ]
}

# Current gold price (in real implementation, fetch from API)
CURRENT_GOLD_PRICE_PER_GRAM = 6350.00  # ₹ per gram

def get_current_gold_price():
    """Get current gold price - in real implementation, fetch from external API"""
    # Simulate slight price variations
    import random
    variation = random.uniform(-50, 50)
    return round(CURRENT_GOLD_PRICE_PER_GRAM + variation, 2)

def is_gold_investment_query(user_message: str) -> bool:
    """Check if user query is related to gold investment"""
    gold_keywords = [
        'gold', 'investment', 'digital gold', 'buy gold', 'gold price',
        'invest in gold', 'gold purchase', 'gold investment', 'precious metals',
        'hedge against inflation', 'gold market', 'gold rates', 'bullion'
    ]
    
    user_message_lower = user_message.lower()
    return any(keyword in user_message_lower for keyword in gold_keywords)

def generate_gold_investment_response(user_message: str) -> Dict[str, Any]:
    """Generate appropriate response for gold investment queries"""
    user_message_lower = user_message.lower()
    
    # Determine the type of query and respond accordingly
    if any(word in user_message_lower for word in ['benefit', 'advantage', 'why']):
        fact = GOLD_FACTS['benefits'][0]
        category = "Benefits of Gold Investment"
    elif any(word in user_message_lower for word in ['digital', 'online', 'app']):
        fact = GOLD_FACTS['digital_gold'][0]
        category = "Digital Gold Investment"
    elif any(word in user_message_lower for word in ['tip', 'advice', 'how', 'start']):
        fact = GOLD_FACTS['investment_tips'][0]
        category = "Gold Investment Tips"
    elif any(word in user_message_lower for word in ['price', 'rate', 'cost']):
        current_price = get_current_gold_price()
        fact = f"Current gold price is ₹{current_price} per gram. Gold prices fluctuate based on market conditions, global economic factors, and demand-supply dynamics."
        category = "Gold Price Information"
    else:
        fact = GOLD_FACTS['benefits'][1]  # Default response
        category = "Gold Investment Information"
    
    return {
        "category": category,
        "fact": fact,
        "nudge": "🌟 Ready to start your gold investment journey? You can purchase digital gold through Simplify Money app starting from just ₹1! Would you like to make a purchase now?",
        "current_price": get_current_gold_price()
    }

# API 1: LLM Interaction and Gold Query Detection
@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """
    First API: Interacts with user, detects gold investment queries,
    and provides appropriate responses with nudges
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400
        
        # Check if the query is related to gold investment
        is_gold_query = is_gold_investment_query(user_message)
        
        if is_gold_query:
            # Generate gold investment response
            gold_response = generate_gold_investment_response(user_message)
            
            response = {
                "user_id": user_id,
                "query_type": "gold_investment",
                "user_message": user_message,
                "ai_response": {
                    "category": gold_response["category"],
                    "answer": gold_response["fact"],
                    "nudge": gold_response["nudge"],
                    "current_gold_price": gold_response["current_price"],
                    "can_purchase": True,
                    "purchase_api_endpoint": "/api/purchase-gold"
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Non-gold investment query
            response = {
                "user_id": user_id,
                "query_type": "general",
                "user_message": user_message,
                "ai_response": {
                    "answer": "I'm specialized in helping with gold investment queries. For the best investment advice regarding gold, feel free to ask about gold prices, benefits of gold investment, digital gold, or how to start investing in gold!",
                    "suggestion": "Try asking: 'What are the benefits of investing in gold?' or 'What is digital gold?'",
                    "can_purchase": False
                },
                "timestamp": datetime.now().isoformat()
            }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API 2: Digital Gold Purchase
@app.route('/api/purchase-gold', methods=['POST'])
def purchase_digital_gold():
    """
    Second API: Handles digital gold purchase process
    """
    try:
        data = request.get_json()
        
        # Extract user and purchase details
        user_details = data.get('user_details', {})
        purchase_amount = float(data.get('amount_inr', 0))
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        # Validate input
        if purchase_amount <= 0:
            return jsonify({
                "error": "Purchase amount must be greater than 0"
            }), 400
        
        if not user_details.get('name') or not user_details.get('email'):
            return jsonify({
                "error": "User name and email are required"
            }), 400
        
        # Get current gold price
        current_gold_price = get_current_gold_price()
        gold_weight = round(purchase_amount / current_gold_price, 4)
        
        # Database operations
        conn = sqlite3.connect('gold_investments.db')
        cursor = conn.cursor()
        
        # Insert or update user
        cursor.execute('''
            INSERT OR REPLACE INTO users (id, name, email, phone)
            VALUES (?, ?, ?, ?)
        ''', (
            user_id,
            user_details.get('name'),
            user_details.get('email'),
            user_details.get('phone', '')
        ))
        
        # Create purchase record
        purchase_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO gold_purchases 
            (id, user_id, amount_inr, gold_weight_grams, gold_price_per_gram, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            purchase_id,
            user_id,
            purchase_amount,
            gold_weight,
            current_gold_price,
            'completed'
        ))
        
        conn.commit()
        
        # Get user's total gold holdings
        cursor.execute('''
            SELECT SUM(gold_weight_grams), SUM(amount_inr), COUNT(*)
            FROM gold_purchases 
            WHERE user_id = ? AND status = 'completed'
        ''', (user_id,))
        
        total_gold, total_invested, total_purchases = cursor.fetchone()
        conn.close()
        
        # Prepare success response
        response = {
            "purchase_id": purchase_id,
            "user_id": user_id,
            "status": "success",
            "message": "🎉 Congratulations! Your digital gold purchase has been completed successfully.",
            "purchase_details": {
                "amount_invested": f"₹{purchase_amount:,.2f}",
                "gold_purchased": f"{gold_weight} grams",
                "price_per_gram": f"₹{current_gold_price:,.2f}",
                "purchase_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "portfolio_summary": {
                "total_gold_holdings": f"{total_gold:.4f} grams",
                "total_amount_invested": f"₹{total_invested:,.2f}",
                "number_of_purchases": total_purchases,
                "current_portfolio_value": f"₹{total_gold * current_gold_price:,.2f}"
            },
            "next_steps": [
                "Your digital gold is securely stored in insured vaults",
                "You can track your investment in the portfolio section",
                "Sell anytime with instant liquidity",
                "Consider setting up SIP for regular gold accumulation"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except ValueError:
        return jsonify({
            "error": "Invalid amount format"
        }), 400
    except Exception as e:
        return jsonify({
            "error": f"Purchase failed: {str(e)}"
        }), 500

# Utility endpoints
@app.route('/api/gold-price', methods=['GET'])
def get_gold_price():
    """Get current gold price"""
    return jsonify({
        "current_price_per_gram": get_current_gold_price(),
        "currency": "INR",
        "last_updated": datetime.now().isoformat()
    })

@app.route('/api/user/<user_id>/portfolio', methods=['GET'])
def get_user_portfolio(user_id):
    """Get user's gold investment portfolio"""
    try:
        conn = sqlite3.connect('gold_investments.db')
        cursor = conn.cursor()
        
        # Get user details
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get purchase history
        cursor.execute('''
            SELECT * FROM gold_purchases 
            WHERE user_id = ? 
            ORDER BY purchase_date DESC
        ''', (user_id,))
        
        purchases = cursor.fetchall()
        conn.close()
        
        # Calculate portfolio summary
        total_gold = sum(p[3] for p in purchases if p[6] == 'completed')  # gold_weight_grams
        total_invested = sum(p[2] for p in purchases if p[6] == 'completed')  # amount_inr
        current_price = get_current_gold_price()
        current_value = total_gold * current_price
        
        return jsonify({
            "user_id": user_id,
            "user_name": user[1],
            "portfolio_summary": {
                "total_gold_grams": round(total_gold, 4),
                "total_invested": round(total_invested, 2),
                "current_value": round(current_value, 2),
                "profit_loss": round(current_value - total_invested, 2),
                "profit_loss_percentage": round(((current_value - total_invested) / total_invested * 100), 2) if total_invested > 0 else 0
            },
            "purchase_history": [
                {
                    "purchase_id": p[0],
                    "amount": p[2],
                    "gold_grams": p[3],
                    "price_per_gram": p[4],
                    "date": p[5],
                    "status": p[6]
                } for p in purchases
            ]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "message": "🚀 Kuber AI Gold Investment APIs",
        "description": "Replicating Kuber AI workflow for gold investments",
        "endpoints": {
            "POST /api/chat": "Chat with AI about gold investments",
            "POST /api/purchase-gold": "Purchase digital gold",
            "GET /api/gold-price": "Get current gold price",
            "GET /api/user/<user_id>/portfolio": "Get user portfolio",
            "GET /api/health": "Health check"
        },
        "example_usage": {
            "chat": "curl -X POST /api/chat -H 'Content-Type: application/json' -d '{\"message\":\"What are benefits of gold investment?\"}'",
            "purchase": "curl -X POST /api/purchase-gold -H 'Content-Type: application/json' -d '{\"user_details\":{\"name\":\"John\",\"email\":\"john@example.com\"},\"amount_inr\":1000}'"
        }
    })

# Initialize database on startup
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)