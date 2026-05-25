from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from store.models import Category, Product


CATEGORIES = [
    ("Clothing & Apparel", "fas fa-tshirt"),
    ("Footwear", "fas fa-shoe-prints"),
    ("Makeup & Cosmetics", "fas fa-magic"),
    ("Fashion Accessories", "fas fa-glasses"),
    ("Electronics", "fas fa-bolt"),
    ("Smartphones", "fas fa-mobile-alt"),
    ("Laptops", "fas fa-laptop"),
    ("Audio", "fas fa-headphones"),
]

PRODUCTS = [
    # Clothing & Apparel
    {
        "name": "Zara Summer Floral A-Line Dress",
        "category": "Clothing & Apparel",
        "our_price": 3990,
        "amazon_price": 4500,
        "flipkart_price": 4400,
        "brand": "Zara",
        "rating": 4.7,
        "reviews_count": 850,
        "stock": 25,
        "eco_rating": 82,
        "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600",
        "amazon_url": "https://www.amazon.in/s?k=zara+floral+dress",
        "flipkart_url": "https://www.flipkart.com/search?q=zara+floral+dress",
        "description": "A lightweight, highly breathable summer dress featuring a beautiful vibrant floral print, an elegant V-neckline, and a flowy A-line silhouette. Perfect for casual day outings, brunches, or beach parties.",
        "ai_summary": "Review sentiment for this item is 92% Positive, with buyers highly praising the fabric softness and premium look. A perfect choice for hot summer afternoons; fits true to size but consider sizing up if you prefer a looser waist fit.",
        "tags": "clothing apparel dress floral summer wear womens fashion zara green blue",
        "is_featured": True,
        "is_ai_recommended": True
    },
    {
        "name": "Levi's 511 Slim Fit Stretch Jeans",
        "category": "Clothing & Apparel",
        "our_price": 2599,
        "amazon_price": 3299,
        "flipkart_price": 3199,
        "brand": "Levi's",
        "rating": 4.5,
        "reviews_count": 3400,
        "stock": 45,
        "eco_rating": 88,
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=600",
        "amazon_url": "https://www.amazon.in/s?k=levis+511+jeans",
        "flipkart_url": "https://www.flipkart.com/search?q=levis+511+jeans",
        "description": "Classic Levi's 511 slim fit jeans designed with modern stretch denim technology. Features a slim cut from the hip to ankle, durable double-stitched seams, and five-pocket styling.",
        "ai_summary": "Review sentiment is 89% Positive. Buyers love the classic blue wash and comfortable stretch, though a few recommend ordering one size up as they run slightly snug in the thighs.",
        "tags": "clothing apparel jeans slim fit mens fashion denim levis blue pants",
        "is_featured": True
    },
    {
        "name": "H&M Classic Cotton Bomber Jacket",
        "category": "Clothing & Apparel",
        "our_price": 2999,
        "amazon_price": 3499,
        "flipkart_price": 3499,
        "brand": "H&M",
        "rating": 4.4,
        "reviews_count": 920,
        "stock": 30,
        "eco_rating": 80,
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600",
        "amazon_url": "https://www.amazon.in/s?k=hm+bomber+jacket",
        "flipkart_url": "https://www.flipkart.com/search?q=hm+bomber+jacket",
        "description": "Sleek, lightweight bomber jacket in woven cotton fabric. Rib-knitted collar, front zipper, side pockets, and soft interior lining make this a versatile, comfortable layer.",
        "ai_summary": "Review sentiment is 86% Positive. Customers praise the stylish design and clean finish, noting it is great for layering over light t-shirts during mild winter or autumn months.",
        "tags": "clothing apparel jacket bomber winter wear mens fashion hm casual",
        "is_ai_recommended": True
    },
    {
        "name": "Fabindia Indigo Handblock Printed Kurta",
        "category": "Clothing & Apparel",
        "our_price": 1890,
        "amazon_price": 2200,
        "flipkart_price": 2150,
        "brand": "Fabindia",
        "rating": 4.6,
        "reviews_count": 1150,
        "stock": 18,
        "eco_rating": 95,
        "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600",
        "amazon_url": "https://www.amazon.in/s?k=fabindia+indigo+kurta",
        "flipkart_url": "https://www.flipkart.com/search?q=fabindia+indigo+kurta",
        "description": "Beautiful ethnic handblock printed cotton kurta in deep indigo dyes. Featuring traditional Indian artisan motifs, a mandarin collar, and regular comfortable fit.",
        "ai_summary": "Review sentiment is 94% Positive. Customers absolutely adore the handblock printing and authentic indigo color. Highly breathable, perfect for hot weather.",
        "tags": "clothing apparel kurta ethnic wear womens fashion fabindia blue cotton"
    },

    # Footwear
    {
        "name": "Adidas Ultraboost Light Sneakers",
        "category": "Footwear",
        "our_price": 14999,
        "amazon_price": 18999,
        "flipkart_price": 17999,
        "brand": "Adidas",
        "rating": 4.8,
        "reviews_count": 2100,
        "stock": 15,
        "eco_rating": 89,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
        "amazon_url": "https://www.amazon.in/s?k=adidas+ultraboost+light",
        "flipkart_url": "https://www.flipkart.com/search?q=adidas+ultraboost+light",
        "description": "High-performance running sneakers featuring next-generation Light Boost cushioning, a Primeknit+ breathable upper, and Continental™ Rubber outsole for superior grip in dry and wet conditions.",
        "ai_summary": "Review sentiment is 95% Positive. Buyers rave about the springy energy return and cloud-like comfort, making it worth every rupee. Suggest sizing up by half a size for wide feet.",
        "tags": "footwear sneakers running shoes adidas sports fashion premium red black",
        "is_featured": True,
        "is_ai_recommended": True
    },
    {
        "name": "Clarks Leather Formal Derby Shoes",
        "category": "Footwear",
        "our_price": 5999,
        "amazon_price": 7999,
        "flipkart_price": 7499,
        "brand": "Clarks",
        "rating": 4.5,
        "reviews_count": 580,
        "stock": 20,
        "eco_rating": 77,
        "image_url": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=600",
        "amazon_url": "https://www.amazon.in/s?k=clarks+derby+shoes+leather",
        "flipkart_url": "https://www.flipkart.com/search?q=clarks+derby+shoes+leather",
        "description": "Premium full-grain leather formal derby shoes. Engineered with Clarks OrthoLite® footbed technology for superior shock absorption and moisture management, finished with clean minimal stitch lines.",
        "ai_summary": "Review sentiment is 88% Positive. Buyers love the genuine leather texture and comfort during long office hours. Takes about 2-3 days to fully break in.",
        "tags": "footwear formal shoes derby leather clarks mens fashion black brown"
    },
    {
        "name": "Steve Madden Classic Stiletto Heels",
        "category": "Footwear",
        "our_price": 6999,
        "amazon_price": 8999,
        "flipkart_price": 8499,
        "brand": "Steve Madden",
        "rating": 4.3,
        "reviews_count": 480,
        "stock": 12,
        "eco_rating": 72,
        "image_url": "https://images.unsplash.com/photo-1596702994230-a8859a852233?w=600",
        "brand": "Steve Madden",
        "amazon_url": "https://www.amazon.in/s?k=steve+madden+stiletto+heels",
        "flipkart_url": "https://www.flipkart.com/search?q=steve+madden+stiletto+heels",
        "description": "Glamorous and elegant strappy stiletto heels featuring a premium sleek upper, a supportive ankle strap, and a 4-inch heel designed to turn heads at any evening event.",
        "ai_summary": "Review sentiment is 83% Positive. Extremely elegant design that pairs beautifully with dresses. Some buyers recommend adding gel insoles for extra comfort during prolonged standing.",
        "tags": "footwear heels stilettos steve madden womens fashion party pink gold"
    },
    {
        "name": "Birkenstock Arizona Suede Leather Sandals",
        "category": "Footwear",
        "our_price": 8990,
        "amazon_price": 10990,
        "flipkart_price": 10490,
        "brand": "Birkenstock",
        "rating": 4.7,
        "reviews_count": 1890,
        "stock": 22,
        "eco_rating": 92,
        "image_url": "https://images.unsplash.com/photo-1603487226258-20b5797018e0?w=600",
        "amazon_url": "https://www.amazon.in/s?k=birkenstock+arizona+leather",
        "flipkart_url": "https://www.flipkart.com/search?q=birkenstock+arizona+leather",
        "description": "The classic, legendary two-strap slide with adjustable metal pin buckles. Featuring a contoured cork-latex footbed that mimics the shape of a healthy foot for orthotic support.",
        "ai_summary": "Review sentiment is 94% Positive. Acclaimed for resolving arch and back pain over time. The footbed naturally molds to your foot within two weeks of wearing.",
        "tags": "footwear sandals flats birkenstock casual comfort unisex cork",
        "is_ai_recommended": True
    },

    # Makeup & Cosmetics
    {
        "name": "M.A.C Retro Matte Lipstick (Ruby Woo)",
        "category": "Makeup & Cosmetics",
        "our_price": 1950,
        "amazon_price": 2300,
        "flipkart_price": 2250,
        "brand": "M.A.C",
        "rating": 4.8,
        "reviews_count": 5120,
        "stock": 60,
        "eco_rating": 81,
        "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=600",
        "amazon_url": "https://www.amazon.in/s?k=mac+retro+matte+ruby+woo",
        "flipkart_url": "https://www.flipkart.com/search?q=mac+retro+matte+ruby+woo",
        "description": "The iconic, ultra-matte red lipstick that made M.A.C famous. Features intense color payoff, a completely matte finish, and long-wearing formula that lasts up to 12 hours.",
        "ai_summary": "Review sentiment is 96% Positive. Widely praised as the 'perfect red' for all skin tones. Can feel a bit dry, so buyers recommend moisturizing lips with a balm before application.",
        "tags": "makeup cosmetics lipstick ruby woo mac beauty grooming red matte",
        "is_featured": True
    },
    {
        "name": "Maybelline Fit Me Matte Foundation",
        "category": "Makeup & Cosmetics",
        "our_price": 499,
        "amazon_price": 699,
        "flipkart_price": 649,
        "brand": "Maybelline",
        "rating": 4.4,
        "reviews_count": 14200,
        "stock": 120,
        "eco_rating": 78,
        "image_url": "https://images.unsplash.com/photo-1631730359575-38e4755d772b?w=600",
        "amazon_url": "https://www.amazon.in/s?k=maybelline+fit+me+foundation",
        "flipkart_url": "https://www.flipkart.com/search?q=maybelline+fit+me+foundation",
        "description": "This lightweight foundation mattifies the skin and refines pores for a completely natural, seamless matte finish. Contains micro-powders to absorb shine and control oil.",
        "ai_summary": "Review sentiment is 88% Positive. Highly appreciated for oil control and buildable medium coverage. Great price-to-quality ratio; use a damp sponge for a skin-like finish.",
        "tags": "makeup cosmetics foundation matte maybelline beauty face liquid",
        "is_ai_recommended": True
    },
    {
        "name": "The Ordinary Niacinamide 10% + Zinc 1% Serum",
        "category": "Makeup & Cosmetics",
        "our_price": 599,
        "amazon_price": 850,
        "flipkart_price": 799,
        "brand": "The Ordinary",
        "rating": 4.6,
        "reviews_count": 9400,
        "stock": 80,
        "eco_rating": 96,
        "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600",
        "amazon_url": "https://www.amazon.in/s?k=the+ordinary+niacinamide",
        "flipkart_url": "https://www.flipkart.com/search?q=the+ordinary+niacinamide",
        "description": "A high-strength vitamin and mineral blemish formula that regulates sebum production, visibly tightens enlarged pores, and brightens uneven skin tone.",
        "ai_summary": "Review sentiment is 91% Positive. Buyers love how it clears active breakouts and reduces acne scarring. Safe for sensitive skin, but patch-testing is advised.",
        "tags": "makeup cosmetics skincare serum niacinamide ordinary beauty zinc face",
        "is_featured": True
    },
    {
        "name": "Urban Decay Naked3 Eyeshadow Palette",
        "category": "Makeup & Cosmetics",
        "our_price": 4499,
        "amazon_price": 5500,
        "flipkart_price": 5300,
        "brand": "Urban Decay",
        "rating": 4.7,
        "reviews_count": 2350,
        "stock": 14,
        "eco_rating": 83,
        "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600",
        "amazon_url": "https://www.amazon.in/s?k=urban+decay+naked+3+palette",
        "flipkart_url": "https://www.flipkart.com/search?q=urban+decay+naked+3+palette",
        "description": "Featuring 12 rose-hued neutral eyeshadow shades ranging from pale shimmery pinks to deep metallic bronzes. High-pigment, ultra-blendable, and long-lasting palette.",
        "ai_summary": "Review sentiment is 93% Positive. Buyers praise the beautiful rose tones and lack of fallout during blending. Ideal for both daily neutral looks and glam night eyes.",
        "tags": "makeup cosmetics palette eyeshadow urban decay beauty eyes rose bronze"
    },

    # Fashion Accessories
    {
        "name": "Fossil Gen 6 Hybrid Smartwatch",
        "category": "Fashion Accessories",
        "our_price": 15995,
        "amazon_price": 18995,
        "flipkart_price": 18495,
        "brand": "Fossil",
        "rating": 4.5,
        "reviews_count": 1200,
        "stock": 18,
        "eco_rating": 88,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600",
        "amazon_url": "https://www.amazon.in/s?k=fossil+gen+6+hybrid",
        "flipkart_url": "https://www.flipkart.com/search?q=fossil+gen+6+hybrid",
        "description": "Combines classic analog design with digital utility. Always-on display, heart rate and SpO2 tracking, physical watch hands, and an incredible 2-week battery life.",
        "ai_summary": "Review sentiment is 87% Positive. Buyers love the classic mechanical look coupled with smart fitness metrics, avoiding the need to recharge every night.",
        "tags": "accessories watches smartwatch fossil mens womens fashion black classic",
        "is_featured": True,
        "is_ai_recommended": True
    },
    {
        "name": "Ray-Ban Classic Wayfarer Sunglasses",
        "category": "Fashion Accessories",
        "our_price": 7490,
        "amazon_price": 9990,
        "flipkart_price": 9490,
        "brand": "Ray-Ban",
        "rating": 4.7,
        "reviews_count": 3120,
        "stock": 25,
        "eco_rating": 84,
        "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600",
        "amazon_url": "https://www.amazon.in/s?k=ray+ban+wayfarer+classic",
        "flipkart_url": "https://www.flipkart.com/search?q=ray+ban+wayfarer+classic",
        "description": "The most recognizable style in the history of sunglasses. Featuring a durable glossy black acetate frame and high-quality polarized G-15 green lenses.",
        "ai_summary": "Review sentiment is 95% Positive. Buyers praise the excellent UV protection and classic look that complements any face shape. Lifetime durability.",
        "tags": "accessories sunglasses wayfarer ray-ban polarized eye wear black fashion"
    },
    {
        "name": "Michael Kors Saffiano Leather Tote Bag",
        "category": "Fashion Accessories",
        "our_price": 12999,
        "amazon_price": 16999,
        "flipkart_price": 15999,
        "brand": "Michael Kors",
        "rating": 4.6,
        "reviews_count": 780,
        "stock": 10,
        "eco_rating": 80,
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600",
        "amazon_url": "https://www.amazon.in/s?k=michael+kors+tote+bag+leather",
        "flipkart_url": "https://www.flipkart.com/search?q=michael+kors+tote+bag+leather",
        "description": "Sophisticated Jet Set tote crafted from scratch-resistant Saffiano leather. Generous interior compartments, a top-zip closure, and gold-tone hardware accents.",
        "ai_summary": "Review sentiment is 91% Positive. Highly rated for its spaciousness and structural rigidity. A luxurious work or travel companion that stays clean easily.",
        "tags": "accessories bags tote hand bag michael kors womens fashion leather brown",
        "is_featured": True
    },
    {
        "name": "Tommy Hilfiger Reversible Leather Belt",
        "category": "Fashion Accessories",
        "our_price": 1899,
        "amazon_price": 2499,
        "flipkart_price": 2399,
        "brand": "Tommy Hilfiger",
        "rating": 4.4,
        "reviews_count": 2100,
        "stock": 40,
        "eco_rating": 83,
        "image_url": "https://images.unsplash.com/photo-1624224971170-2f84fed5eb5e?w=600",
        "amazon_url": "https://www.amazon.in/s?k=tommy+hilfiger+reversible+belt",
        "flipkart_url": "https://www.flipkart.com/search?q=tommy+hilfiger+reversible+belt",
        "description": "Crafted from 100% genuine leather, this belt features a reversible strap to switch between formal black and casual brown. Complete with a brushed metal buckle.",
        "ai_summary": "Review sentiment is 89% Positive. Customers appreciate the dual-style function and strong, high-quality buckle system. Makes a great gift.",
        "tags": "accessories belts leather tommy hilfiger mens fashion black brown reversible"
    },

    # Electronics & Gadgets
    {
        "name": "Apple Vision Pro 2",
        "category": "Electronics",
        "our_price": 279900,
        "amazon_price": 299900,
        "flipkart_price": 295000,
        "brand": "Apple",
        "rating": 4.9,
        "reviews_count": 1820,
        "stock": 5,
        "eco_rating": 84,
        "image_url": "https://images.unsplash.com/photo-1707923485746-81ad1dbfec31?w=500",
        "amazon_url": "https://www.amazon.in/s?k=apple+vision+pro",
        "flipkart_url": "https://www.flipkart.com/search?q=apple+vision+pro",
        "description": "Revolutionary spatial computer that seamlessly blends digital content with your physical space. Featuring Dual-micro-OLED displays with 23 million pixels, M2 and R1 chips, and spatial audio.",
        "ai_summary": "Review sentiment is 93% Positive. Buyers state visual quality is peerless and hand-tracking feels incredibly intuitive. Some mention the device weight is noticeable during long sessions.",
        "tags": "apple vision pro spatial computer mixed reality vr ar headset gadgets",
        "is_featured": True,
        "is_ai_recommended": True
    },

    # Smartphones
    {
        "name": "iPhone 17 Pro Max",
        "category": "Smartphones",
        "our_price": 139900,
        "amazon_price": 159900,
        "flipkart_price": 156900,
        "brand": "Apple",
        "rating": 4.9,
        "reviews_count": 4920,
        "stock": 20,
        "eco_rating": 89,
        "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600",
        "amazon_url": "https://www.amazon.in/s?k=iphone+17+pro+max",
        "flipkart_url": "https://www.flipkart.com/search?q=iphone+17+pro+max",
        "description": "A19 Pro chip with advanced neural engine, lighter titanium body with ultra-thin bezels, futuristic 48MP triple-lens system with 10x optical zoom, and 120Hz ProMotion display.",
        "ai_summary": "Review sentiment is 96% Positive. Appreciated for blazing fast AI processing and top-tier zoom photography. An exceptional flagship experience with ₹20,000 savings in our store.",
        "tags": "apple iphone smartphone flagship ios camera titanium mobile",
        "is_featured": True,
        "is_ai_recommended": True
    },

    # Laptops
    {
        "name": "MacBook Pro 14\" (M5 Pro)",
        "category": "Laptops",
        "our_price": 179900,
        "amazon_price": 199900,
        "flipkart_price": 196000,
        "brand": "Apple",
        "rating": 4.9,
        "reviews_count": 2150,
        "stock": 10,
        "eco_rating": 94,
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600",
        "amazon_url": "https://www.amazon.in/s?k=macbook+pro+m3+pro",
        "flipkart_url": "https://www.flipkart.com/search?q=macbook+pro+m3+pro",
        "description": "Apple M5 Pro chip, 16-core CPU, 40-core GPU, 24GB Unified Memory, 512GB SSD. Liquid Retina XDR display, 22-hour battery life.",
        "ai_summary": "Review sentiment is 97% Positive. Acclaimed for supreme compiler and video rendering performance. The 22-hour battery life is a game-changer.",
        "tags": "apple macbook pro laptop creative workstation m5 macos",
        "is_featured": True,
        "is_ai_recommended": True
    },

    # Audio
    {
        "name": "Sony WH-1000XM6 Ultimate ANC",
        "category": "Audio",
        "our_price": 27990,
        "amazon_price": 32990,
        "flipkart_price": 31500,
        "brand": "Sony",
        "rating": 4.8,
        "reviews_count": 5210,
        "stock": 30,
        "eco_rating": 85,
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600",
        "amazon_url": "https://www.amazon.in/s?k=sony+wh1000xm5",
        "flipkart_url": "https://www.flipkart.com/search?q=sony+wh1000xm5",
        "description": "Next-generation noise cancellation powered by Dual V2 processors. High-resolution LDAC audio, smart adaptive ambient sound, and 40-hour battery life.",
        "ai_summary": "Review sentiment is 94% Positive. Widely praised for class-leading active noise cancellation that effectively silence airplane cabin noises. Ergonomics are extremely soft.",
        "tags": "sony headphones wireless noise cancelling over ear audio bluetooth",
        "is_featured": True,
        "is_ai_recommended": True
    }
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

        # Generate 100 more dynamic products for testing
        self.stdout.write('Generating 100 additional products for a rich catalog...')
        import random

        brands_by_cat = {
            "Clothing & Apparel": ["Zara", "H&M", "Levi's", "Fabindia", "Roadster", "Allen Solly", "Nike", "Adidas", "Puma", "Tommy Hilfiger"],
            "Footwear": ["Nike", "Adidas", "Puma", "Clarks", "Birkenstock", "Steve Madden", "Reebok", "Woodland", "Bata", "Crocs"],
            "Makeup & Cosmetics": ["M.A.C", "Maybelline", "L'Oreal", "The Ordinary", "Clinique", "Lakme", "Nivea", "Forest Essentials", "Plum", "Mamaearth"],
            "Fashion Accessories": ["Ray-Ban", "Fossil", "Michael Kors", "Tommy Hilfiger", "Fastrack", "Casio", "Titan", "Baggit", "Caprese", "Wildhorn"],
            "Electronics": ["Sony", "Samsung", "Bose", "JBL", "Realme", "Xiaomi", "OnePlus", "Marshall", "Anker", "TP-Link"],
            "Smartphones": ["Apple", "Samsung", "OnePlus", "Google", "Xiaomi", "vivo", "OPPO", "Motorola", "Nothing", "Realme"],
            "Laptops": ["Dell", "HP", "Lenovo", "Apple", "Asus", "Acer", "MSI", "Microsoft", "Xiaomi", "Samsung"],
            "Audio": ["Sony", "Sennheiser", "Audio-Technica", "Bose", "JBL", "OnePlus", "Boat", "Jabra", "Shure", "Beyerdynamic"]
        }

        adjectives = ["Classic", "Breathable", "Premium", "Comfort", "Slim-Fit", "Organic", "Oversized", "Designer", "Textured", "Lightweight", "Durable", "Sleek", "Minimalist", "Waterproof", "High-Performance", "Eco-Friendly", "Smart", "Ultra", "Elite", "Modern"]

        nouns_by_cat = {
            "Clothing & Apparel": ["Cotton T-Shirt", "Summer Dress", "Denim Jeans", "Hooded Sweatshirt", "Slim Fit Chinos", "Linen Blazer", "Ethnic Kurti", "Woolen Cardigan", "Silk Saree", "Casual Shorts"],
            "Footwear": ["Running Sneakers", "Leather Oxford Shoes", "Formal Derby Shoes", "Casual Loafers", "Walking Shoes", "Suede Boots", "Comfort Sandals", "Sports Cleats", "High Heel Pumps"],
            "Makeup & Cosmetics": ["Matte Lipstick", "Hydrating Serum", "Liquid Foundation", "Waterproof Mascara", "Face Moisturizer", "Sunscreen SPF 50", "Exfoliating Scrub", "Clay Mask", "Eye Pencil"],
            "Fashion Accessories": ["Wayfarer Sunglasses", "Leather Wallet", "Smart Watch", "Reversible Belt", "Shoulder Tote Bag", "Metal Cuff Bracelet", "Silk Tie", "Travel Backpack", "Aviator Sunglasses"],
            "Electronics": ["Smart TV", "Wireless Charger", "Portable Bluetooth Speaker", "Action Camera", "Power Bank", "Smart Bulb", "Wi-Fi Router", "VR Headset", "Noise Cancelling Earbuds"],
            "Smartphones": ["Flagship 5G Phone", "Android Smartphone", "Pro Max Device", "Ultra Smartphone", "Foldable Phone", "Lite Mobile"],
            "Laptops": ["Slim Ultrabook", "Gaming Laptop", "Convertible 2-in-1", "Professional Workstation", "Student Laptop"],
            "Audio": ["Over-Ear Headphones", "True Wireless Earbuds", "Studio Monitor Headset", "Wireless Neckband", "Soundbar Speaker"]
        }

        unsplash_by_cat = {
            "Clothing & Apparel": [
                "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=600",
                "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600",
                "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=600",
                "https://images.unsplash.com/photo-1578932750294-f5075e85f44a?w=600",
                "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600"
            ],
            "Footwear": [
                "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=600",
                "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=600",
                "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600",
                "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600",
                "https://images.unsplash.com/photo-1512374382149-433853003064?w=600"
            ],
            "Makeup & Cosmetics": [
                "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600",
                "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=600",
                "https://images.unsplash.com/photo-1526045431048-f857369aba09?w=600",
                "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600",
                "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=600"
            ],
            "Fashion Accessories": [
                "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600",
                "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=600",
                "https://images.unsplash.com/photo-1509695507497-903c140c43b0?w=600",
                "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=600",
                "https://images.unsplash.com/photo-1611085583191-a3b1a30a8a3a?w=600"
            ],
            "Electronics": [
                "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=600",
                "https://images.unsplash.com/photo-1593340061790-1c02e1c944d1?w=600",
                "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600",
                "https://images.unsplash.com/photo-1588508065123-287b28e013da?w=600",
                "https://images.unsplash.com/photo-1555664424-778a1e5e1b48?w=600"
            ],
            "Smartphones": [
                "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600",
                "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=600",
                "https://images.unsplash.com/photo-1565849906461-0e443530e24c?w=600",
                "https://images.unsplash.com/photo-1605236453806-6ff36851218e?w=600",
                "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600"
            ],
            "Laptops": [
                "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600",
                "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600",
                "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=600",
                "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=600",
                "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=600"
            ],
            "Audio": [
                "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=600",
                "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600",
                "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=600",
                "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600",
                "https://images.unsplash.com/photo-1577174881658-0f30ed549adc?w=600"
            ]
        }

        price_ranges = {
            "Clothing & Apparel": (799, 4500),
            "Footwear": (1299, 12000),
            "Makeup & Cosmetics": (299, 3500),
            "Fashion Accessories": (499, 15000),
            "Electronics": (999, 35000),
            "Smartphones": (12000, 95000),
            "Laptops": (35000, 150000),
            "Audio": (999, 25000)
        }

        extra_count = 0
        attempts = 0
        target_extra = 100
        generated_names = set()

        while extra_count < target_extra and attempts < 1500:
            attempts += 1
            cat_name = random.choice(CATEGORIES)[0]
            cat_obj = cat_map.get(cat_name)
            if not cat_obj:
                continue

            brand = random.choice(brands_by_cat[cat_name])
            adj = random.choice(adjectives)
            noun = random.choice(nouns_by_cat[cat_name])
            p_name = f"{brand} {adj} {noun}"

            if p_name in generated_names or Product.objects.filter(name=p_name).exists():
                continue

            generated_names.add(p_name)
            
            min_p, max_p = price_ranges[cat_name]
            our_price = int(random.uniform(min_p, max_p))
            amazon_price = int(our_price * random.uniform(1.08, 1.25))
            flipkart_price = int(our_price * random.uniform(1.04, 1.18))
            
            discount = int(((amazon_price - our_price) / amazon_price) * 100)

            description = f"Experience the ultimate {noun.lower()} from {brand}. Crafted with {adj.lower()} design principles, this product brings premium quality and exceptional utility to your daily life. Features highly durable construction and eco-conscious design."
            ai_summary = f"Review sentiment is 90% Positive. Buyers love the {adj.lower()} design and reliable functionality. Highly recommended as a high-value purchase compared to market rates, saving you around {discount}% over other platforms."

            img_url = random.choice(unsplash_by_cat[cat_name])
            img_url += f"&sig={random.randint(1, 1000)}"

            tags = f"{cat_name.lower()} {brand.lower()} {adj.lower()} {noun.lower()} best quality value saving"

            Product.objects.create(
                name=p_name,
                category=cat_obj,
                our_price=our_price,
                amazon_price=amazon_price,
                flipkart_price=flipkart_price,
                amazon_url=f"https://www.amazon.in/s?k={p_name.replace(' ', '+')}",
                flipkart_url=f"https://www.flipkart.com/search?q={p_name.replace(' ', '+')}",
                image_url=img_url,
                rating=round(random.uniform(3.9, 4.9), 1),
                reviews_count=random.randint(30, 8500),
                stock=random.randint(10, 120),
                brand=brand,
                ai_summary=ai_summary,
                is_featured=random.choice([True, False, False, False]),
                is_ai_recommended=random.choice([True, False, False, False]),
                tags=tags,
                eco_rating=random.randint(65, 98)
            )
            extra_count += 1

        self.stdout.write(f'[OK] Generated {extra_count} additional dynamic products.')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('   Admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('   Store: http://127.0.0.1:8000/')
        self.stdout.write('   Login: admin / admin123')
