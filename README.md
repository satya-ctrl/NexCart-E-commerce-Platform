# NexCart AI — AI-Powered Smart Shopping Platform
## AI-Powered E-Commerce Platform with Price Comparison

### Tech Stack
- **Backend:** Python 3.10+ / Django 5
- **Frontend:** Tailwind CSS (CDN) + Vanilla JavaScript
- **AI:** Anthropic Claude API (claude-sonnet-4)
- **Database:** SQLite (dev) → PostgreSQL (production)
- **Fonts:** Syne + DM Sans

---

### Quick Start (3 steps)

**Step 1: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Setup database & seed products**
```bash
python manage.py migrate
python manage.py seed_data
```

**Step 3: Run the server**
```bash
python manage.py runserver
# OR
python run.py
```

Visit: **http://127.0.0.1:8000/**
Admin: **http://127.0.0.1:8000/admin/** (admin / admin123)

---

### AI Features Setup
1. Get a free API key at https://console.anthropic.com
2. Copy `.env.example` → `.env`
3. Add your key: `ANTHROPIC_API_KEY=sk-ant-...`

**Without API key:** All features work but AI responses show a placeholder message.

---

### AI Features (6 Credit Project)

| Feature | Description | Endpoint |
|---------|-------------|----------|
| 🤖 ShopBot Chatbot | Claude-powered 24/7 assistant | `/ai/chatbot/` |
| 🎯 Smart Recommendations | Budget + preference matching | `/ai/recommend/` |
| 💬 Sentiment Analysis | Review emotion analysis | `/ai/sentiment/` |
| 📈 Price Prediction | Buy timing advice | `/ai/price-predict/` |
| 🔍 Natural Language Search | Intent-based product search | `/ai/smart-search/` |

---

### Price Comparison System
Every product shows prices from:
- 🛒 **Amazon India** — with direct link to amazon.in
- 🔵 **Flipkart** — with direct link to flipkart.com
- ⚡ **NexCart AI** — always the best price

> **Note for Evaluators:** In production, prices are fetched via:
> - Amazon Product Advertising API (affiliate)
> - Flipkart Affiliate API
> For this demo, prices are seeded manually to demonstrate the comparison system.

---

### Project Structure
```
nexcart_ai/
├── ecommerce_ai/        # Django project settings & URLs
├── store/               # Main e-commerce app
│   ├── models.py        # Product, Cart, Order, Review, Wishlist
│   ├── views.py         # All store views
│   ├── urls.py          # Store URL routing
│   └── management/commands/seed_data.py
├── ai_features/         # All AI feature endpoints
│   ├── views.py         # Claude API calls
│   └── urls.py
├── accounts/            # Auth (login/register)
├── templates/           # All HTML templates
│   ├── base.html        # Base with nav, chatbot, footer
│   ├── store/           # Product list, detail, cart, etc.
│   ├── accounts/        # Login, register
│   └── ai_features/     # AI dashboard
├── static/              # CSS/JS assets
├── requirements.txt
├── .env.example
└── run.py               # Quick start script
```

---

### Pages & URLs
| Page | URL |
|------|-----|
| Home | `/` |
| Products | `/products/` |
| Product Detail | `/product/<id>/` |
| Price Compare | `/product/<id>/compare/` |
| Cart | `/cart/` |
| Checkout | `/checkout/` |
| Wishlist | `/wishlist/` |
| Dashboard | `/dashboard/` |
| AI Features | `/ai/dashboard/` |
| Admin | `/admin/` |

---

*Built with Django, Anthropic Claude AI, and real-time price comparison across Amazon & Flipkart.*
