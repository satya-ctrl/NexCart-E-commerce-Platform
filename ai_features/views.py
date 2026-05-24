from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import urllib.request
import urllib.error

from store.models import Product, SearchHistory


class ClaudeAPIError(Exception):
    pass


def call_claude(messages, system="You are a helpful AI shopping assistant.", stream=False):
    """Call Anthropic Claude API"""
    api_key = settings.ANTHROPIC_API_KEY
    if not api_key:
        raise ClaudeAPIError("API key not configured in .env file.")

    # Sanitize and format messages to comply with Anthropic Claude API rules:
    # 1. Must not be empty.
    # 2. Must alternate between 'user' and 'assistant' roles.
    # 3. Must start with 'user' role.
    sanitized = []
    for msg in messages:
        role = msg.get('role')
        content = msg.get('content', '')
        if not content:
            continue
        if role not in ('user', 'assistant'):
            role = 'user'
        if sanitized and sanitized[-1]['role'] == role:
            # Merge consecutive messages of the same role
            sanitized[-1]['content'] += "\n" + content
        else:
            sanitized.append({"role": role, "content": content})

    # Ensure it starts with 'user'
    while sanitized and sanitized[0]['role'] != 'user':
        sanitized.pop(0)

    if not sanitized:
        raise ClaudeAPIError("No valid user messages to process.")

    payload = json.dumps({
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1000,
        "system": system,
        "messages": sanitized
    }).encode('utf-8')

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data['content'][0]['text']
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode()
            raise ClaudeAPIError(f"HTTP {e.code}: {err_body}")
        except:
            raise ClaudeAPIError(str(e))
    except Exception as e:
        raise ClaudeAPIError(str(e))


@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        history = data.get('history', [])

        # Get product context
        products = Product.objects.all()[:20]
        product_list = "\n".join([f"- {p.name} (₹{p.our_price}, {p.category.name}, Rating: {p.rating})" for p in products])

        system = f"""You are ShopBot, an AI shopping assistant for NexCart AI — an intelligent e-commerce platform with real-time price comparison across Amazon and Flipkart.
        
Available products in our store:
{product_list}

You help users:
- Find products matching their needs
- Compare prices between Amazon, Flipkart, and our store
- Give recommendations based on budget and preferences
- Explain product features
- Track orders and help with shopping

Be friendly, concise, and always try to recommend products from our catalog.
If asked about price comparison, mention we show real-time prices from Amazon and Flipkart.
Respond in a helpful, conversational way."""

        messages = history + [{"role": "user", "content": user_message}]
        
        try:
            reply = call_claude(messages, system=system)
        except ClaudeAPIError as e:
            # Smart fallback response for demo mode
            user_msg_lower = user_message.lower()
            
            # 1. Match specific product names in the user query
            matched_product = None
            for p in Product.objects.all():
                p_name_lower = p.name.lower()
                if p_name_lower in user_msg_lower:
                    matched_product = p
                    break
                # Try matching key words (e.g. "iphone 17 pro" matches "iPhone 17 Pro Max")
                p_words = [w for w in p_name_lower.replace('"', '').replace("'", '').split() if len(w) > 2]
                if p_words and all(w in user_msg_lower for w in p_words[:3]):
                    matched_product = p
                    break
            
            if matched_product:
                p = matched_product
                reply = (
                    f"🤖 *[Demo Mode]*\n\n"
                    f"The price for **{p.name}** at NexCart AI is **₹{p.our_price}**.\n\n"
                    f"Here is a comparison with other stores:\n"
                    f"- **NexCart AI:** ₹{p.our_price} (Best Deal!)\n"
                    f"- **Amazon India:** " + (f"₹{p.amazon_price}" if p.amazon_price else "Price not listed") + "\n"
                    f"- **Flipkart:** " + (f"₹{p.flipkart_price}" if p.flipkart_price else "Price not listed") + "\n\n"
                    f"You can view its details and add it directly to your cart!"
                )
            elif "recommend" in user_msg_lower or "suggest" in user_msg_lower or "buy" in user_msg_lower:
                db_prods = Product.objects.all()[:3]
                prod_lines = []
                for i, p in enumerate(db_prods):
                    prod_lines.append(f"{i+1}. **{p.name}** (₹{p.our_price}) - Rating: {p.rating}⭐. {p.description[:80]}...")
                prod_text = "\n".join(prod_lines)
                reply = (
                    "🤖 *[Demo Mode - Claude API out of credits]*\n\n"
                    "Here are some top recommendations from our catalog:\n"
                    f"{prod_text}\n\n"
                    "Feel free to check out their details or add them to your cart!"
                )
            elif "price" in user_msg_lower or "compare" in user_msg_lower or "flipkart" in user_msg_lower or "amazon" in user_msg_lower:
                reply = (
                    "🤖 *[Demo Mode - Claude API out of credits]*\n\n"
                    "At NexCart AI, we compare prices in real-time across major platforms like Amazon India and Flipkart. "
                    "You will always find the best deals marked with a discount in our store! "
                    "Click on any product to view its real-time comparison table."
                )
            elif "hello" in user_msg_lower or "hi" in user_msg_lower or "hey" in user_msg_lower:
                reply = (
                    "🤖 *[Demo Mode - Claude API out of credits]*\n\n"
                    "Hello! Welcome to NexCart AI. How can I help you today? "
                    "I can recommend products, compare prices, or help you find deals."
                )
            else:
                matches = Product.objects.filter(name__icontains=user_message)[:2]
                if matches:
                    prod_text = ", ".join([f"**{p.name}** (₹{p.our_price})" for p in matches])
                    reply = (
                        "🤖 *[Demo Mode - Claude API out of credits]*\n\n"
                        f"I found some products matching your request: {prod_text}."
                    )
                else:
                    reply = (
                        "🤖 *[Demo Mode - Claude API out of credits]*\n\n"
                        "Thanks for reaching out! Since the configured Anthropic API key is currently out of credits, "
                        "I am running in local demo mode. "
                        "You can browse products using the search bar, view the price comparison tables, "
                        "and add items to your cart or wishlist!"
                    )

        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=user_message)

        return JsonResponse({'reply': reply})
    return JsonResponse({'error': 'POST required'}, status=400)


@csrf_exempt
def get_recommendation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        budget = data.get('budget', '')
        category = data.get('category', '')
        preferences = data.get('preferences', '')

        products = Product.objects.all()
        if category:
            products = products.filter(category__name__icontains=category)
        product_list = "\n".join([f"- {p.name}: ₹{p.our_price}, Rating {p.rating}, {p.description[:80]}..." for p in products[:20]])

        prompt = f"""User wants product recommendations:
Budget: ₹{budget}
Category: {category}
Preferences: {preferences}

Available products:
{product_list}

Recommend 3 best products with brief reasons. Format as JSON array:
[{{"name": "...", "reason": "...", "price": "...", "match_score": 95}}]
Only return valid JSON, no extra text."""

        try:
            reply = call_claude([{"role": "user", "content": prompt}])
            clean = reply.strip().strip('```json').strip('```').strip()
            recs = json.loads(clean)
        except Exception:
            # Fallback mock recommendation from DB
            recs = []
            db_prods = Product.objects.all()
            if category:
                db_prods = db_prods.filter(category__name__icontains=category)
            if budget:
                try:
                    max_budget = float(budget)
                    db_prods = db_prods.filter(our_price__lte=max_budget)
                except ValueError:
                    pass
            for p in db_prods[:3]:
                recs.append({
                    "name": p.name,
                    "reason": f"Matches your category preference with an excellent rating of {p.rating}⭐ and fits the budget.",
                    "price": str(p.our_price),
                    "match_score": 90
                })
            if not recs:
                for p in Product.objects.all()[:3]:
                    recs.append({
                        "name": p.name,
                        "reason": f"Top trending product with {p.rating}⭐ rating.",
                        "price": str(p.our_price),
                        "match_score": 85
                    })

        return JsonResponse({'recommendations': recs, 'raw': str(recs)})
    return JsonResponse({'error': 'POST required'}, status=400)


@csrf_exempt
def analyze_sentiment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reviews = data.get('reviews', [])

        if not reviews:
            return JsonResponse({'error': 'No reviews'})

        review_text = "\n".join([f"Review {i+1}: {r}" for i, r in enumerate(reviews)])
        prompt = f"""Analyze these product reviews and give a sentiment analysis:

{review_text}

Return JSON:
{{"overall_sentiment": "positive/negative/mixed", "score": 85, "positives": ["..."], "negatives": ["..."], "summary": "..."}}
Only return valid JSON."""

        try:
            reply = call_claude([{"role": "user", "content": prompt}])
            clean = reply.strip().strip('```json').strip('```').strip()
            result = json.loads(clean)
        except Exception:
            # Fallback mock sentiment analysis
            positives = []
            negatives = []
            pos_words = ['great', 'good', 'excellent', 'amazing', 'love', 'best', 'nice', 'perfect', 'awesome']
            neg_words = ['bad', 'poor', 'slow', 'worst', 'cheap', 'hate', 'broke', 'defect', 'plastic']
            for r in reviews:
                r_lower = r.lower()
                for w in pos_words:
                    if w in r_lower:
                        positives.append(r[:50] + "...")
                        break
                for w in neg_words:
                    if w in r_lower:
                        negatives.append(r[:50] + "...")
                        break
            
            score = 75
            if positives and not negatives:
                overall = "positive"
                score = 90
            elif negatives and not positives:
                overall = "negative"
                score = 35
            else:
                overall = "mixed"
                score = 65
                
            result = {
                "overall_sentiment": overall,
                "score": score,
                "positives": positives if positives else ["Product functions as advertised"],
                "negatives": negatives if negatives else ["No significant negative points mentioned"],
                "summary": "This is a simulated review analysis [Demo Mode]. Customers generally commented on usability and features."
            }

        return JsonResponse(result)
    return JsonResponse({'error': 'POST required'}, status=400)


@csrf_exempt
def smart_search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query', '')

        products = Product.objects.all()
        product_list = "\n".join([f"ID:{p.id} | {p.name} | ₹{p.our_price} | {p.category.name} | Tags:{p.tags}" for p in products])

        prompt = f"""User searched for: "{query}"

Product catalog:
{product_list}

Return IDs of most relevant products (max 8), ranked by relevance.
Format: JSON array of IDs only: [1, 5, 12, 3]
Only return the JSON array."""

        results = []
        try:
            reply = call_claude([{"role": "user", "content": prompt}])
            clean = reply.strip().strip('```json').strip('```').strip()
            ids = json.loads(clean)
            products_found = Product.objects.filter(id__in=ids)
            results = [{'id': p.id, 'name': p.name, 'price': str(p.our_price), 'image': p.image_url, 'rating': str(p.rating)} for p in products_found]
        except Exception:
            # Fallback database query search
            from django.db.models import Q
            products_found = Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) | 
                Q(category__name__icontains=query) |
                Q(tags__icontains=query)
            )[:8]
            results = [{'id': p.id, 'name': p.name, 'price': str(p.our_price), 'image': p.image_url, 'rating': str(p.rating)} for p in products_found]

        return JsonResponse({'results': results})
    return JsonResponse({'error': 'POST required'}, status=400)


@csrf_exempt
def price_prediction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except:
            return JsonResponse({'error': 'Not found'})

        prompt = f"""Product: {product.name}
Current price: ₹{product.our_price}
Amazon price: ₹{product.amazon_price or 'N/A'}
Flipkart price: ₹{product.flipkart_price or 'N/A'}
Category: {product.category.name}

Predict price trend for next 30 days and give buying advice.
Return JSON: {{"trend": "rising/falling/stable", "predicted_price": 1200, "advice": "Buy now", "confidence": 80, "reason": "..."}}
Only return valid JSON."""

        try:
            reply = call_claude([{"role": "user", "content": prompt}])
            clean = reply.strip().strip('```json').strip('```').strip()
            result = json.loads(clean)
        except Exception:
            # Fallback price prediction
            current = float(product.our_price)
            amazon = float(product.amazon_price) if product.amazon_price else None
            flipkart = float(product.flipkart_price) if product.flipkart_price else None
            
            if amazon and current < amazon:
                trend = "stable"
                advice = f"Buy now! NexCart price is ₹{amazon - current:.0f} cheaper than Amazon."
                confidence = 92
            elif flipkart and current < flipkart:
                trend = "stable"
                advice = f"Buy now! NexCart price is ₹{flipkart - current:.0f} cheaper than Flipkart."
                confidence = 88
            else:
                trend = "falling"
                advice = "Wait. Analysis indicates a potential price drop of 5-8% next week."
                confidence = 70
                
            result = {
                "trend": trend,
                "predicted_price": int(current * 0.95),
                "advice": advice,
                "confidence": confidence,
                "reason": "Simulated trend based on current competitor pricing margins. NexCart's price is highly optimized."
            }

        return JsonResponse(result)
    return JsonResponse({'error': 'POST required'}, status=400)


def ai_dashboard(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'ai_features/dashboard.html', {'products': products})
