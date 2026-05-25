from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from store.models import Category, Product


CATEGORIES = [
    ("Clothing & Apparel", "👗"),
    ("Footwear", "👟"),
    ("Makeup & Cosmetics", "💄"),
    ("Fashion Accessories", "🕶️"),
    ("Electronics", "⚡"),
    ("Smartphones", "📱"),
    ("Laptops", "💻"),
    ("Audio", "🎧"),
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
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('   Admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('   Store: http://127.0.0.1:8000/')
        self.stdout.write('   Login: admin / admin123')
