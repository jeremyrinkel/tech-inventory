import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# --- Inventory Data ---
tech_store = {
    "Laptop Pro": ("Laptop", 999.99),
    "Gaming Mouse": ("Accessory", 49.99),
    "4K Monitor": ("Monitor", 299.99),
    "Mechanical Keyboard": ("Accessory", 89.99)
}

# --- HTML Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Tech Store Inventory</title>
    <style>
        body { font-family: Arial; margin: 30px; background-color: #f2f2f2; }
        table { width: 70%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border-bottom: 1px solid #ccc; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        input, select { padding: 8px; margin: 5px; }
        button { padding: 8px 12px; background-color: #2196F3; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #0b7dda; }
    </style>
</head>
<body>
    <h1>🖥️ Tech Store Inventory</h1>

    <form action="/add" method="POST">
        <input name="name" placeholder="Product Name" required>
        <input name="category" placeholder="Category" required>
        <input name="price" placeholder="Price" type="number" step="0.01" required>
        <button type="submit">Add Product</button>
    </form>

    <form action="/search" method="GET">
        <input name="query" placeholder="Search Product">
        <button type="submit">Find</button>
    </form>

    {% if message %}
    <p><strong>{{ message }}</strong></p>
    {% endif %}

    <table>
        <tr><th>Product</th><th>Category</th><th>Price</th></tr>
        {% for name, (category, price) in tech_store.items() %}
        <tr><td>{{ name }}</td><td>{{ category }}</td><td>${{ "%.2f"|format(price) }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, tech_store=tech_store, message=None)

@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"]
    category = request.form["category"]
    price = float(request.form["price"])
    tech_store[name] = (category, price)
    return redirect("/")

@app.route("/search")
def search_product():
    query = request.args.get("query", "")
    if query in tech_store:
        category, price = tech_store[query]
        message = f"{query} is a {category} and costs ${price:.2f}."
    else:
        message = f"Product '{query}' not found."
    return render_template_string(HTML_TEMPLATE, tech_store=tech_store, message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
