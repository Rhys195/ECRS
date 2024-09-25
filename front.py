@app.route("/")
def index():

    clean_data = pd.read_csv('models/clean_data.csv')

    # Sort by Rating and ReviewCount to get the top-rated products
    trending_products = clean_data.sort_values(by=['Rating', 'ReviewCount'], ascending=False).head(100)

    # Add random prices to each product (e.g., between $10 and $100)
    trending_products['random_price'] = [round(random.uniform(10, 100), 2) for _ in range(len(trending_products))]

    # Convert DataFrame to list of dictionaries for Jinja2
    trending_products_list = []
    for _, row in trending_products.iterrows():
        product = row.to_dict()
        product['ImageURLs'] = [url.strip() for url in product['ImageURL'].split('|')]
        trending_products_list.append(product)

    # Cart count from session
    cart_count = len(session.get('cart', {}))

    return render_template(
        'index.html',
        trending_products=trending_products_list,  # Pass list of dicts instead of DataFrame
        user=session.get('username'),
        cart_count=cart_count,
        truncate=truncate
    )
