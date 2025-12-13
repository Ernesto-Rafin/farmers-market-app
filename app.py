from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "market.db"

def get_db():
    return sqlite3.connect(DB)

@app.route("/")
def index():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    markets = conn.execute("SELECT * FROM markets").fetchall()
    conn.close()
    return render_template("markets.html", markets=markets)

@app.route("/market/<int:market_id>")
def market_detail(market_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row

    market = conn.execute(
        "SELECT * FROM markets WHERE id = ?", (market_id,)
    ).fetchone()

    products = conn.execute("""
        SELECT products.id, products.name, products.price
        FROM products
        JOIN vendors ON products.vendor_id = vendors.id
        WHERE vendors.market_id = ?
    """, (market_id,)).fetchall()

    conn.close()
    return render_template(
        "market_detail.html",
        market=market,
        products=products
    )

@app.route("/preorder", methods=["POST"])
def preorder():
    product_id = request.form["product_id"]
    quantity = request.form["quantity"]

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN")
        cursor.execute(
            "INSERT INTO orders (product_id, quantity) VALUES (?, ?)",
            (product_id, quantity)
        )
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()

    return render_template("success.html")

@app.route("/search")
def search():
    query = request.args.get("q", "")

    conn = get_db()
    conn.row_factory = sqlite3.Row

    products = conn.execute("""
        SELECT products.name, products.price
        FROM products
        WHERE products.name LIKE ?
    """, (f"%{query}%",)).fetchall()

    conn.close()
    return render_template("search.html", products=products, query=query)

if __name__ == "__main__":
    app.run(debug=True)
