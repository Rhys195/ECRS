@app.route('/products_by_category', methods=['POST'])
def get_products_by_category():
    selected_categories = request.json.get('categories', [])

    # Assuming `train_data` is your DataFrame loaded from the CSV
    train_data = pd.read_csv("models/clean_data.csv")

    # Filter products by selected categories
    filtered_products = train_data[train_data['Category'].isin(selected_categories)]

    # Shuffle the filtered products
    shuffled_products = filtered_products.sample(frac=1).reset_index(drop=True)

    # Select relevant columns to send back to the frontend
    products = shuffled_products[
        ['ID', 'Rating', 'ReviewCount', 'Category', 'Brand', 'Name', 'ImageURL', 'Description', 'Tags',
         'Price']].to_dict(orient='records')

    return jsonify(products)
