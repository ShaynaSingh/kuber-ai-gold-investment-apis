# 🪙 Kuber AI Gold Investment APIs

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

A complete implementation of Kuber AI workflow for gold investments with two main APIs that detect gold investment queries, provide intelligent responses, and handle digital gold purchases.

## 🚀 Live Demo

**Base URL:** `https://your-app-name.herokuapp.com`

## 📊 Features

- ✅ **Smart Gold Query Detection** - AI detects gold investment related questions
- ✅ **Contextual Responses** - Provides relevant facts about gold investment
- ✅ **User Nudging** - Encourages digital gold purchase after information
- ✅ **Complete Purchase Flow** - From inquiry to successful purchase
- ✅ **Database Integration** - User and transaction management
- ✅ **Portfolio Tracking** - Investment summary and performance
- ✅ **RESTful APIs** - Clean, well-documented endpoints

## 🔧 API Endpoints

### 1. Chat API - Gold Investment Detection
```bash
POST /api/chat
```
**Request:**
```json
{
  "message": "What are the benefits of investing in gold?",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "query_type": "gold_investment",
  "ai_response": {
    "category": "Benefits of Gold Investment",
    "answer": "Gold is considered a hedge against inflation...",
    "nudge": "🌟 Ready to start your gold investment journey?",
    "can_purchase": true
  }
}
```

### 2. Purchase API - Digital Gold Purchase
```bash
POST /api/purchase-gold
```
**Request:**
```json
{
  "user_details": {
    "name": "Parag Kumar",
    "email": "parag@example.com",
    "phone": "+919876543210"
  },
  "amount_inr": 1000,
  "user_id": "user123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "🎉 Your digital gold purchase completed!",
  "purchase_details": {
    "amount_invested": "₹1,000.00",
    "gold_purchased": "0.1575 grams"
  },
  "portfolio_summary": {
    "total_gold_holdings": "0.1575 grams",
    "total_amount_invested": "₹1,000.00"
  }
}
```

## 🧪 Testing

### Quick Test Commands

**Test Chat API:**
```bash
curl -X POST https://your-app-name.herokuapp.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How to invest in gold?", "user_id": "test_user"}'
```

**Test Purchase API:**
```bash
curl -X POST https://your-app-name.herokuapp.com/api/purchase-gold \
  -H "Content-Type: application/json" \
  -d '{
    "user_details": {
      "name": "Test User",
      "email": "test@example.com",
      "phone": "+919999999999"
    },
    "amount_inr": 500,
    "user_id": "test_user"
  }'
```

## 🏗️ Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/kuber-ai-gold-investment-apis.git
cd kuber-ai-gold-investment-apis
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Access the API:**
- Local: `http://localhost:5000`
- API Documentation: `http://localhost:5000/`

## 🌐 Deployment

### Heroku (Recommended)
```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Open app
heroku open
```

### Railway
1. Connect your GitHub repository to [Railway](https://railway.app)
2. Configure build settings
3. Deploy automatically

### Render
1. Connect GitHub to [Render](https://render.com)
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`

## 🗄️ Database Schema

### Users Table
- `id` - Unique user identifier
- `name` - User's full name
- `email` - Email address
- `phone` - Phone number
- `created_at` - Registration timestamp

### Gold Purchases Table
- `id` - Purchase transaction ID
- `user_id` - Reference to user
- `amount_inr` - Investment amount in INR
- `gold_weight_grams` - Gold purchased in grams
- `gold_price_per_gram` - Price at purchase time
- `purchase_date` - Transaction timestamp
- `status` - Purchase status

## 🎯 Kuber AI Workflow Match

| Step | Kuber AI | Our Implementation |
|------|----------|-------------------|
| 1 | User asks gold question | Chat API detects gold queries |
| 2 | AI provides information | Contextual facts about gold |
| 3 | AI suggests purchase | Nudge message with CTA |
| 4 | User proceeds to buy | Purchase API handles transaction |
| 5 | Purchase confirmation | Success message + portfolio |
| 6 | Database entry | User and purchase data stored |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Parag Kumar** - Chief Technologist at Simplify Money

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: support@example.com

---

⭐ **Star this repo if it helped you!**
