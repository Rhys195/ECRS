@app.route('/products_by_headline')
def get_products_by_headline():
    df = pd.read_csv('models/clean_data.csv')

    # Define 5 shopping-related headlines
    headlines = ["Best Sellers", "New Arrivals", "Top Rated", "Trending", "Discount Deals"]

    products_by_headline = {}

    # Randomly select products for each headline
    for headline in headlines:
        # Sample random products from the DataFrame
        num_products = 20  # Number of products to sample for each headline
        products = df.sample(n=min(len(df), num_products)).to_dict(orient='records')
        products_by_headline[headline] = products

    return jsonify(products_by_headline)
