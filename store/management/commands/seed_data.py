from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from store.models import Category, Product


CATEGORIES = [
    ("Electronics", "⚡"),
    ("Smartphones", "📱"),
    ("Laptops", "💻"),
    ("Audio", "🎧"),
    ("Home Appliances", "🏠"),
    ("Fashion", "👗"),
    ("Books", "📚"),
    ("Sports", "🏃"),
]

PRODUCTS = [
    # Electronics & Gadgets
    {"name": "Apple Vision Pro 2", "category": "Electronics", "our_price": 279900, "amazon_price": 299900, "flipkart_price": 295000,
     "brand": "Apple", "rating": 4.9, "reviews_count": 1820, "stock": 5, "eco_rating": 84,
     "image_url": "https://images.unsplash.com/photo-1707923485746-81ad1dbfec31?w=500",
     "amazon_url": "https://www.amazon.in/s?k=apple+vision+pro",
     "flipkart_url": "https://www.flipkart.com/search?q=apple+vision+pro",
     "description": "Revolutionary spatial computer that seamlessly blends digital content with your physical space. Featuring Dual-micro-OLED displays with 23 million pixels, M2 and R1 chips, and spatial audio.",
     "ai_summary": "The cutting-edge of mixed reality. Visual fidelity is unrivaled, and hand-eye tracking feels like magic. Best pricing available here vs retail.",
     "tags": "apple vision pro spatial computer mixed reality vr ar headset gadgets", "is_featured": True, "is_ai_recommended": True},

    {"name": "Sony PlayStation 5 Pro", "category": "Electronics", "our_price": 64990, "amazon_price": 69990, "flipkart_price": 68500,
     "brand": "Sony", "rating": 4.8, "reviews_count": 8920, "stock": 15, "eco_rating": 79,
     "image_url": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=600",
     "amazon_url": "https://www.amazon.in/s?k=playstation+5+pro",
     "flipkart_url": "https://www.flipkart.com/search?q=playstation+5+pro",
     "description": "Experience enhanced graphical performance with advanced ray tracing, sharp image clarity for your 4K TV, and high frame rate gameplay. 2TB SSD.",
     "ai_summary": "The ultimate console gaming experience. Upgraded GPU provides PC-like graphics with console convenience. Significant price drop in our store.",
     "tags": "sony playstation ps5 pro console gaming hardware", "is_featured": True},

    {"name": "Fujifilm X100VI Digital Camera", "category": "Electronics", "our_price": 169990, "amazon_price": 179990, "flipkart_price": 175000,
     "brand": "Fujifilm", "rating": 4.7, "reviews_count": 3410, "stock": 4, "eco_rating": 82,
     "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600",
     "amazon_url": "https://www.amazon.in/s?k=fujifilm+x100vi",
     "flipkart_url": "https://www.flipkart.com/search?q=fujifilm+x100vi",
     "description": "Ultra-portable premium compact camera featuring a high-resolution 40.2MP X-Trans CMOS 5 HR sensor, X-Processor 5, and 5-axis in-body image stabilization.",
     "ai_summary": "Extremely popular retro creator camera. Built-in film simulations produce gorgeous, print-ready shots instantly. High demand, get it while in stock.",
     "tags": "fujifilm camera photography retro x100vi digital mirrorless", "is_ai_recommended": True},

    {"name": "EcoFlow Delta 3 Power Station", "category": "Electronics", "our_price": 89900, "amazon_price": 99900, "flipkart_price": 95000,
     "brand": "EcoFlow", "rating": 4.9, "reviews_count": 520, "stock": 10, "eco_rating": 96,
     "image_url": "https://images.unsplash.com/photo-1605901309584-818e25960a8f?w=600",
     "amazon_url": "https://www.amazon.in/s?k=ecoflow+delta",
     "flipkart_url": "https://www.flipkart.com/search?q=ecoflow+delta",
     "description": "Ultra-fast charging solar generator / backup battery for home power failures or outdoor camping. Clean, green power source with zero emissions.",
     "ai_summary": "Incredible emergency solar battery storage. Generates zero noise and zero emissions. Highest sustainability score in our electronics catalog.",
     "tags": "solar generator ecoflow battery power station backup camping green", "is_featured": True},

    {"name": "Oura Ring Gen 4", "category": "Electronics", "our_price": 34900, "amazon_price": 39900, "flipkart_price": 38500,
     "brand": "Oura", "rating": 4.6, "reviews_count": 1205, "stock": 15, "eco_rating": 91,
     "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=500",
     "amazon_url": "https://www.amazon.in/s?k=oura+ring",
     "flipkart_url": "https://www.flipkart.com/search?q=oura+ring",
     "description": "Sleek, screen-free health tracking smart ring. Monitor your sleep stages, resting heart rate, blood oxygen levels, and daily activity levels in a durable titanium chassis.",
     "ai_summary": "Minimalist biometric tracking ring. Titanium structure is extremely durable and lightweight. A fantastic screen-free alternative to traditional smartwatches.",
     "tags": "oura ring smart ring tracker biometrics health fitness wearable"},

    # Smartphones
    {"name": "iPhone 17 Pro Max", "category": "Smartphones", "our_price": 139900, "amazon_price": 159900, "flipkart_price": 156900,
     "brand": "Apple", "rating": 4.9, "reviews_count": 4920, "stock": 20, "eco_rating": 89,
     "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600",
     "amazon_url": "https://www.amazon.in/s?k=iphone+17+pro+max",
     "flipkart_url": "https://www.flipkart.com/search?q=iphone+17+pro+max",
     "description": "A19 Pro chip with advanced neural engine, lighter titanium body with ultra-thin bezels, futuristic 48MP triple-lens system with 10x optical zoom, and 120Hz ProMotion display.",
     "ai_summary": "Apple's absolute best. The A19 Pro chip handles local AI models with ease, and the titanium chassis feels exceptionally premium. Save ₹20,000.",
     "tags": "apple iphone smartphone flagship ios camera titanium mobile", "is_featured": True, "is_ai_recommended": True},

    {"name": "Samsung Galaxy S26 Ultra", "category": "Smartphones", "our_price": 114900, "amazon_price": 129990, "flipkart_price": 127900,
     "brand": "Samsung", "rating": 4.8, "reviews_count": 6780, "stock": 25, "eco_rating": 87,
     "image_url": "/static/images/s26_ultra.png",
     "amazon_url": "https://www.amazon.in/s?k=galaxy+s26+ultra",
     "flipkart_url": "https://www.flipkart.com/search?q=galaxy+s26+ultra",
     "description": "Next-generation Galaxy AI powerhouse. Equipped with Snapdragon 8 Gen 5, 200MP Main Camera, integrated S-Pen, and a flat 6.8\" Dynamic AMOLED 2X display.",
     "ai_summary": "Top Android smartphone of the year. Powerful zoom lens and Galaxy AI features make productivity simple. Highly recommended.",
     "tags": "samsung galaxy s26 ultra smartphone flagship android mobile s-pen", "is_featured": True},

    {"name": "Nothing Phone (3a) AI", "category": "Smartphones", "our_price": 21999, "amazon_price": 25999, "flipkart_price": 24900,
     "brand": "Nothing", "rating": 4.5, "reviews_count": 12030, "stock": 50, "eco_rating": 90,
     "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600",
     "amazon_url": "https://www.amazon.in/s?k=nothing+phone+2",
     "flipkart_url": "https://www.flipkart.com/search?q=nothing+phone+2",
     "description": "Unique semi-transparent back design with Glyph Interface. Mediated Dimensity 7300, 50MP dual cameras, and clean Nothing OS with integrated AI widgets.",
     "ai_summary": "Most stylish mid-range phone. Transparent design turns heads, and Glyph lights are actually useful. Best deal on the market.",
     "tags": "nothing phone glyph transparent android smartphone budget", "is_ai_recommended": True},

    # Laptops
    {"name": "MacBook Pro 14\" (M5 Pro)", "category": "Laptops", "our_price": 179900, "amazon_price": 199900, "flipkart_price": 196000,
     "brand": "Apple", "rating": 4.9, "reviews_count": 2150, "stock": 10, "eco_rating": 94,
     "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600",
     "amazon_url": "https://www.amazon.in/s?k=macbook+pro+m3+pro",
     "flipkart_url": "https://www.flipkart.com/search?q=macbook+pro+m3+pro",
     "description": "Apple M5 Pro chip, 16-core CPU, 40-core GPU, 24GB Unified Memory, 512GB SSD. Liquid Retina XDR display, 22-hour battery life.",
     "ai_summary": "Unbelievable processing power. M5 Pro handles video editing and software compilation without breaking a sweat. Incredible battery life.",
     "tags": "apple macbook pro laptop creative workstation m5 macos", "is_featured": True, "is_ai_recommended": True},

    {"name": "ASUS ROG Zephyrus G16", "category": "Laptops", "our_price": 189900, "amazon_price": 209900, "flipkart_price": 205000,
     "brand": "ASUS", "rating": 4.7, "reviews_count": 890, "stock": 8, "eco_rating": 83,
     "image_url": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=500",
     "amazon_url": "https://www.amazon.in/s?k=rog+zephyrus+g16",
     "flipkart_url": "https://www.flipkart.com/search?q=rog+zephyrus+g16",
     "description": "Stunning ultra-thin premium gaming laptop with 16\" Nebula OLED 240Hz screen, Intel Core Ultra 9, RTX 4080 GPU, and CNC aluminum chassis.",
     "ai_summary": "The gold standard for thin gaming laptops. Nebula OLED screen offers rich colors, and RTX 4080 handles heavy machine learning or gaming.",
     "tags": "asus laptop gaming laptop oled rtx intel rog portable creator"},

    {"name": "ASUS ROG Ally X", "category": "Laptops", "our_price": 63990, "amazon_price": 69990, "flipkart_price": 68900,
     "brand": "ASUS", "rating": 4.6, "reviews_count": 4310, "stock": 18, "eco_rating": 79,
     "image_url": "https://images.unsplash.com/photo-1605901309584-818e25960a8f?w=600",
     "amazon_url": "https://www.amazon.in/s?k=rog+ally+x",
     "flipkart_url": "https://www.flipkart.com/search?q=rog+ally+x",
     "description": "Premium Windows handheld gaming console. Powered by AMD Ryzen Z1 Extreme, 24GB LPDDR5X RAM, 1TB SSD, 80Wh double capacity battery, and 7\" 120Hz display.",
     "ai_summary": "Best handheld gaming PC. 80Wh battery solves the battery issues of prior handhelds, and 24GB RAM keeps gameplay smooth.",
     "tags": "asus rog ally console handheld windows gaming hardware", "is_featured": True},

    # Audio
    {"name": "Sony WH-1000XM6 Ultimate", "category": "Audio", "our_price": 27990, "amazon_price": 32990, "flipkart_price": 31500,
     "brand": "Sony", "rating": 4.8, "reviews_count": 5210, "stock": 30, "eco_rating": 85,
     "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600",
     "amazon_url": "https://www.amazon.in/s?k=sony+wh1000xm5",
     "flipkart_url": "https://www.flipkart.com/search?q=sony+wh1000xm5",
     "description": "Next-generation noise cancellation powered by Dual V2 processors. High-resolution LDAC audio, smart adaptive ambient sound, and 40-hour battery life.",
     "ai_summary": "The master class of ANC. Drowns out engine and background office noise perfectly. Best-in-class comfort and battery life.",
     "tags": "sony headphones wireless noise cancelling over ear audio bluetooth", "is_featured": True, "is_ai_recommended": True},

    {"name": "Bose QuietComfort Ultra Earbuds", "category": "Audio", "our_price": 21990, "amazon_price": 25900, "flipkart_price": 24800,
     "brand": "Bose", "rating": 4.7, "reviews_count": 3980, "stock": 40, "eco_rating": 82,
     "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600",
     "amazon_url": "https://www.amazon.in/s?k=bose+quietcomfort+ultra+earbuds",
     "flipkart_url": "https://www.flipkart.com/search?q=bose+quietcomfort+ultra+earbuds",
     "description": "World-class active noise cancellation with CustomTune audio profiling. Breakthrough immersive spatial audio, customizable touch controls, IPX4 rating.",
     "ai_summary": "Top choice for comfort and in-ear noise cancellation. Immersive Audio spatial setting adds a wide soundstage.",
     "tags": "bose quietcomfort earbuds noise cancelling audio wireless tws", "is_ai_recommended": True},

    {"name": "Nothing Ear (a) transparent", "category": "Audio", "our_price": 7999, "amazon_price": 9999, "flipkart_price": 8999,
     "brand": "Nothing", "rating": 4.5, "reviews_count": 6720, "stock": 100, "eco_rating": 90,
     "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500",
     "amazon_url": "https://www.amazon.in/s?k=nothing+ear",
     "flipkart_url": "https://www.flipkart.com/search?q=nothing+ear",
     "description": "Eye-catching transparent housing with powerful Smart Active Noise Cancellation up to 45dB. Featuring 11mm ceramic drivers and LDAC Hi-Res Audio.",
     "ai_summary": "Superb styling and great sound performance. Transparent look matches the Nothing OS design philosophy. Environmentally friendly packaging.",
     "tags": "nothing ear transparent tws wireless earbuds noise cancelling audio"},

    # Home Appliances
    {"name": "Dyson 360 Vis Nav Robot Vacuum", "category": "Home Appliances", "our_price": 79900, "amazon_price": 89900, "flipkart_price": 87500,
     "brand": "Dyson", "rating": 4.6, "reviews_count": 920, "stock": 8, "eco_rating": 86,
     "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600",
     "amazon_url": "https://www.amazon.in/s?k=dyson+vacuum",
     "flipkart_url": "https://www.flipkart.com/search?q=dyson+vacuum",
     "description": "Dyson's most powerful robot vacuum with 360-degree vision, HEPA filtration, and D-shape design to reach corner-to-corner dust.",
     "ai_summary": "Insane suction power for a robot vacuum. D-shape design cleans corners far better than round robot cleaners. Significant discount vs retail.",
     "tags": "dyson robot vacuum cleaner automated smart home appliance", "is_featured": True},

    {"name": "Dyson Airwrap Multi-Styler", "category": "Home Appliances", "our_price": 45900, "amazon_price": 49900, "flipkart_price": 48500,
     "brand": "Dyson", "rating": 4.8, "reviews_count": 3450, "stock": 12, "eco_rating": 88,
     "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500",
     "amazon_url": "https://www.amazon.in/s?k=dyson+airwrap",
     "flipkart_url": "https://www.flipkart.com/search?q=dyson+airwrap",
     "description": "Next-generation hair styler using the Coanda effect to curl, shape, and smooth hair without extreme heat damage. Includes redesigned barrels and brushes.",
     "ai_summary": "Premium styling tool that preserves hair health. Smart heat sensor prevents thermal damage, meaning healthier long-term hair. Highly popular.",
     "tags": "dyson airwrap hair styler health care beauty appliances"},

    # Fashion
    {"name": "Nike Air Max Dn 'All Day'", "category": "Fashion", "our_price": 14995, "amazon_price": 16995, "flipkart_price": 16500,
     "brand": "Nike", "rating": 4.7, "reviews_count": 2150, "stock": 60, "eco_rating": 76,
     "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
     "amazon_url": "https://www.amazon.in/s?k=nike+air+max+shoes",
     "flipkart_url": "https://www.flipkart.com/search?q=nike+air+max+shoes",
     "description": "Features Nike's futuristic Dynamic Air unit system with dual-pressure tubes, creating a reactive sensation with every step. Sleek modern design.",
     "ai_summary": "Highly comfortable, modern lifestyle sneakers. The Dynamic Air bubble shifts pressure as you walk for unmatched heel-to-toe comfort.",
     "tags": "nike air max shoes sneakers footwear fashion clothing premium"},

    # Books
    {"name": "Clear Habit Journal", "category": "Books", "our_price": 1199, "amazon_price": 1499, "flipkart_price": 1399,
     "brand": "Baronfig", "rating": 4.8, "reviews_count": 14320, "stock": 100, "eco_rating": 98,
     "image_url": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=600",
     "amazon_url": "https://www.amazon.in/s?k=clear+habit+journal",
     "flipkart_url": "https://www.flipkart.com/search?q=clear+habit+journal",
     "description": "The official journal designed by James Clear, author of Atomic Habits. A beautiful notebook configured to help you build positive habits.",
     "ai_summary": "Perfect physical companion to Atomic Habits. Premium paper quality and habit tracking layout make journaling simple and productive.",
     "tags": "book journal habit atomic habits james clear notebook planner", "is_featured": True}
]


class Command(BaseCommand):
    help = 'Seed database with demo products for NexCart AI platform'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding NexCart AI database...')

        # Clear existing data to ensure a fresh modern catalog
        self.stdout.write('Clearing old categories and products...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexcart.ai', 'admin123')
            self.stdout.write('[OK] Superuser: admin / admin123')

        # Create categories
        cat_map = {}
        for name, icon in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                slug=slugify(name),
                defaults={'name': name, 'icon': icon}
            )
            cat_map[name] = cat
        self.stdout.write(f'[OK] {len(CATEGORIES)} categories created')

        # Create products
        count = 0
        for p in PRODUCTS:
            cat = cat_map.get(p.pop('category'))
            if not cat:
                continue
            Product.objects.get_or_create(
                name=p['name'],
                defaults={**p, 'category': cat}
            )
            count += 1

        self.stdout.write(f'[OK] {count} products seeded')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('   Admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('   Store: http://127.0.0.1:8000/')
        self.stdout.write('   Login: admin / admin123')
