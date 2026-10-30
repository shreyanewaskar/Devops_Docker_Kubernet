
from flask import Flask, jsonify, render_template_string
import socket

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudCart | Online Shopping</title>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
          rel="stylesheet">

    <style>
        :root {
            --primary: #5b4bdb;
            --primary-dark: #4535c4;
            --background: #f7f8fc;
            --text: #202033;
            --muted: #77778b;
            --white: #ffffff;
            --border: #ececf3;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--background);
            color: var(--text);
        }

        button, input {
            font-family: inherit;
        }

        button {
            cursor: pointer;
        }

        .navbar {
            background: white;
            padding: 20px 7%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            font-size: 25px;
            font-weight: 800;
            color: var(--primary);
            letter-spacing: -1px;
        }

        .logo span {
            color: var(--text);
        }

        .nav-links {
            display: flex;
            gap: 30px;
            list-style: none;
        }

        .nav-links a {
            text-decoration: none;
            color: #55556a;
            font-size: 14px;
            font-weight: 500;
        }

        .nav-links a:hover {
            color: var(--primary);
        }

        .cart-btn {
            background: #f0edff;
            color: var(--primary);
            border: none;
            padding: 12px 18px;
            border-radius: 12px;
            font-weight: 700;
        }

        .hero {
            margin: 35px 7%;
            padding: 55px;
            border-radius: 28px;
            background: linear-gradient(120deg, #e8e4ff, #f5efff);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 30px;
            overflow: hidden;
        }

        .hero-content {
            max-width: 520px;
        }

        .tag {
            display: inline-block;
            background: #ffffffb8;
            color: var(--primary);
            padding: 8px 14px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 20px;
        }

        .hero h1 {
            font-size: clamp(32px, 4vw, 52px);
            line-height: 1.15;
            letter-spacing: -2px;
            margin-bottom: 18px;
        }

        .hero h1 span {
            color: var(--primary);
        }

        .hero p {
            color: #68677e;
            line-height: 1.8;
            margin-bottom: 25px;
        }

        .primary-btn {
            display: inline-block;
            background: var(--primary);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 700;
            transition: 0.2s;
        }

        .primary-btn:hover {
            background: var(--primary-dark);
            transform: translateY(-2px);
        }

        .hero-visual {
            font-size: 150px;
            filter: drop-shadow(0 20px 20px #7d69d333);
        }

        .section {
            margin: 55px 7%;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            gap: 20px;
        }

        .section-header h2 {
            font-size: 27px;
            letter-spacing: -1px;
        }

        .section-header p {
            color: var(--muted);
            font-size: 13px;
            margin-top: 8px;
        }

        .search-box {
            padding: 13px 16px;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: white;
            width: 230px;
            outline: none;
        }

        .search-box:focus {
            border-color: var(--primary);
        }

        .categories {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 28px;
        }

        .category-btn {
            background: white;
            border: 1px solid var(--border);
            padding: 11px 20px;
            border-radius: 30px;
            color: #656579;
            font-size: 13px;
            font-weight: 600;
        }

        .category-btn.active,
        .category-btn:hover {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        .products {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 22px;
        }

        .product-card {
            background: white;
            border: 1px solid var(--border);
            border-radius: 20px;
            overflow: hidden;
            transition: 0.25s;
        }

        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px #29205a0d;
        }

        .product-image {
            height: 210px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 90px;
            position: relative;
        }

        .product-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .product-image .discount {
            position: absolute;
            top: 15px;
            left: 15px;
            background: #ffffffdd;
            color: #e45d66;
            padding: 7px 10px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 800;
        }

        .product-info {
            padding: 18px;
        }

        .product-category {
            font-size: 11px;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
        }

        .product-info h3 {
            font-size: 15px;
            margin: 9px 0;
        }

        .rating {
            color: #f5a623;
            font-size: 12px;
            margin-bottom: 13px;
        }

        .price-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }

        .price {
            font-size: 18px;
            font-weight: 800;
        }

        .add-btn {
            width: 38px;
            height: 38px;
            border-radius: 12px;
            border: none;
            background: #f0edff;
            color: var(--primary);
            font-size: 23px;
            font-weight: 600;
        }

        .add-btn:hover {
            background: var(--primary);
            color: white;
        }

        .benefits {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 60px 7%;
        }

        .benefit {
            background: white;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 25px;
            display: flex;
            gap: 18px;
            align-items: center;
        }

        .benefit-icon {
            font-size: 30px;
        }

        .benefit h3 {
            font-size: 14px;
            margin-bottom: 7px;
        }

        .benefit p {
            font-size: 12px;
            color: var(--muted);
        }

        footer {
            background: #222139;
            color: white;
            padding: 35px 7%;
            text-align: center;
        }

        footer p {
            color: #b8b7c9;
            font-size: 13px;
            margin-top: 12px;
        }

        .toast {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: #24223d;
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 10px 30px #0002;
            opacity: 0;
            transform: translateY(20px);
            transition: 0.3s;
            z-index: 200;
        }

        .toast.show {
            opacity: 1;
            transform: translateY(0);
        }

        @media (max-width: 1000px) {
            .products {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .hero-visual {
                font-size: 100px;
            }
        }

        @media (max-width: 650px) {
            .navbar {
                padding: 18px 5%;
            }

            .nav-links {
                display: none;
            }

            .hero {
                margin: 20px 5%;
                padding: 30px;
            }

            .hero-visual {
                display: none;
            }

            .section {
                margin: 40px 5%;
            }

            .section-header {
                align-items: flex-start;
                flex-direction: column;
            }

            .search-box {
                width: 100%;
            }

            .products {
                grid-template-columns: 1fr;
            }

            .product-image {
                height: 240px;
            }

            .benefits {
                grid-template-columns: 1fr;
                margin: 40px 5%;
            }
        }
    </style>
</head>

<body>

    <nav class="navbar">
        <div class="logo">Cloud<span>Cart.</span></div>

        <ul class="nav-links">
            <li><a href="#">Home</a></li>
            <li><a href="#products">Shop</a></li>
            <li><a href="#benefits">About</a></li>
        </ul>

        <button class="cart-btn">
            🛒 Cart <span id="cart-count">0</span>
        </button>
    </nav>

    <section class="hero">
        <div class="hero-content">
            <div class="tag">✨ NEW COLLECTION 2026</div>

            <h1>
                Upgrade your<br>
                lifestyle with <span>CloudCart.</span>
            </h1>

            <p>
                Discover products you'll love. Shop the latest
                electronics, fashion and lifestyle essentials
                at amazing prices.
            </p>

            <a href="#products" class="primary-btn">
                Explore Products →
            </a>
        </div>

        <div class="hero-visual">🛍️</div>
    </section>

    <section class="section" id="products">
        <div class="section-header">
            <div>
                <h2>Featured Products</h2>
                <p>Handpicked essentials for your everyday life.</p>
            </div>

            <input
                type="text"
                id="search"
                class="search-box"
                placeholder="Search products..."
            >
        </div>

        <div class="categories">
            <button class="category-btn active" data-category="All">All Products</button>
            <button class="category-btn" data-category="Electronics">Electronics</button>
            <button class="category-btn" data-category="Fashion">Fashion</button>
            <button class="category-btn" data-category="Lifestyle">Lifestyle</button>
        </div>

        <div class="products" id="product-list"></div>
    </section>

    <section class="benefits" id="benefits">
        <div class="benefit">
            <div class="benefit-icon">🚚</div>
            <div>
                <h3>Free Shipping</h3>
                <p>On orders above ₹999</p>
            </div>
        </div>

        <div class="benefit">
            <div class="benefit-icon">🔒</div>
            <div>
                <h3>Secure Payments</h3>
                <p>Your transactions are safe with us</p>
            </div>
        </div>

        <div class="benefit">
            <div class="benefit-icon">💝</div>
            <div>
                <h3>Easy Returns</h3>
                <p>Hassle-free 7-day returns</p>
            </div>
        </div>
    </section>

    <footer>
        <div class="logo">CloudCart.</div>
        <p>
            A Cloud Native E-Commerce Demo Application
        </p>
        <p>
            Powered by Flask, Docker and Kubernetes
        </p>
        <p>
            Container Host: {{ hostname }}
        </p>
    </footer>

    <div class="toast" id="toast">
        Product added to cart!
    </div>

    <script>
        const products = [
            {
                id: 1,
                name: "Wireless Headphones",
                category: "Electronics",
                price: 2499,
                rating: "★★★★★",
                emoji: "🎧",
                color: "#f0edff",
                discount: "20% OFF"
            },
            {
                id: 2,
                name: "Smart Watch",
                category: "Electronics",
                price: 3999,
                rating: "★★★★★",
                emoji: "⌚",
                color: "#e8f4ff",
                discount: "15% OFF"
            },
            {
                id: 3,
                name: "Classic Sneakers",
                category: "Fashion",
                price: 2999,
                rating: "★★★★☆",
                emoji: "👟",
                color: "#fff0e7",
                discount: "30% OFF"
            },
            {
                id: 4,
                name: "Premium Backpack",
                category: "Lifestyle",
                price: 1899,
                rating: "★★★★★",
                emoji: "🎒",
                color: "#e9f8ed",
                discount: "10% OFF"
            },
            {
                id: 5,
                name: "Minimalist Camera",
                category: "Electronics",
                price: 8499,
                rating: "★★★★★",
                emoji: "📷",
                color: "#fceafa",
                discount: "25% OFF"
            },
            {
                id: 6,
                name: "Everyday Hoodie",
                category: "Fashion",
                price: 1599,
                rating: "★★★★☆",
                emoji: "👕",
                color: "#fff5d9",
                discount: "20% OFF"
            },
            {
                id: 7,
                name: "Coffee Essentials",
                category: "Lifestyle",
                price: 999,
                rating: "★★★★★",
                emoji: "☕",
                color: "#f6e8dd",
                discount: "10% OFF"
            },
            {
                id: 8,
                name: "Portable Speaker",
                category: "Electronics",
                price: 2199,
                rating: "★★★★★",
                emoji: "🔊",
                color: "#e4f6f5",
                discount: "15% OFF"
            }
        ];

        let cartCount = 0;
        let selectedCategory = "All";

        const productList = document.getElementById("product-list");
        const cartCounter = document.getElementById("cart-count");
        const searchInput = document.getElementById("search");

        function renderProducts() {
            const searchText = searchInput.value.toLowerCase();

            const filteredProducts = products.filter(product => {
                const matchesCategory =
                    selectedCategory === "All" ||
                    product.category === selectedCategory;

                const matchesSearch =
                    product.name.toLowerCase().includes(searchText);

                return matchesCategory && matchesSearch;
            });

            productList.innerHTML = filteredProducts.map(product => `
                <div class="product-card">
                    <div
                        class="product-image"
                        style="background: ${product.color}"
                    >
                        <span class="discount">${product.discount}</span>
                        ${product.emoji}
                    </div>

                    <div class="product-info">
                        <div class="product-category">
                            ${product.category}
                        </div>

                        <h3>${product.name}</h3>

                        <div class="rating">
                            ${product.rating}
                        </div>

                        <div class="price-row">
                            <div class="price">
                                ₹${product.price.toLocaleString("en-IN")}
                            </div>

                            <button
                                class="add-btn"
                                onclick="addToCart(${product.id})"
                                aria-label="Add ${product.name} to cart"
                            >
                                +
                            </button>
                        </div>
                    </div>
                </div>
            `).join("");

            if (filteredProducts.length === 0) {
                productList.innerHTML = `
                    <p>No products found. Try another search.</p>
                `;
            }
        }

        function addToCart(productId) {
            const product = products.find(p => p.id === productId);

            cartCount++;
            cartCounter.textContent = cartCount;

            showToast(product.name + " added to cart!");
        }

        let toastTimer;

        function showToast(message) {
            const toast = document.getElementById("toast");

            toast.textContent = message;
            toast.classList.add("show");

            clearTimeout(toastTimer);

            toastTimer = setTimeout(() => {
                toast.classList.remove("show");
            }, 2200);
        }

        document.querySelectorAll(".category-btn").forEach(button => {
            button.addEventListener("click", () => {
                document.querySelectorAll(".category-btn")
                    .forEach(btn => btn.classList.remove("active"));

                button.classList.add("active");

                selectedCategory = button.dataset.category;

                renderProducts();
            });
        });

        searchInput.addEventListener("input", renderProducts);

        renderProducts();
    </script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        hostname=socket.gethostname()
    )

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "CloudCart",
        "hostname": socket.gethostname()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
