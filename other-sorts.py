@app.route('/products_by_rating', methods=['POST'])
def get_products_by_rating():
    request_data = request.json

    selected_rating = request_data.get('rating', None)

    if selected_rating is None:
        return jsonify([])

    try:
        # Load data from CSV
        train_data = pd.read_csv("models/clean_data.csv")
    except Exception:
        return jsonify([])

    # Convert selected rating to float for comparison
    try:
        selected_rating = float(selected_rating)
    except ValueError:
        return jsonify([])

    # Filter products by selected rating
    filtered_products = train_data[train_data['Rating'] == selected_rating]

    # Shuffle the filtered products
    shuffled_products = filtered_products.sample(frac=1).reset_index(drop=True)

    # Prepare products data
    products = shuffled_products[[
        'ID', 'Rating', 'ReviewCount', 'Category', 'Brand', 'Name', 'ImageURL', 'Description', 'Tags', 'Price'
    ]].to_dict(orient='records')

    return jsonify(products)


@app.route('/products_by_sort', methods=['GET'])
def get_products_by_sort():
    criteria = request.args.get('criteria', None)
    order = request.args.get('order', 'asc')

    valid_criteria = ['Price', 'Rating', 'Popularity']
    if criteria not in valid_criteria:
        print(f'Invalid criteria: {criteria}')
        return jsonify([])

    if order not in ['asc', 'desc']:
        print(f'Invalid order: {order}')
        return jsonify([])

    try:
        # Load data from CSV
        train_data = pd.read_csv("models/clean_data.csv")

        # Check if the criteria column exists in the DataFrame
        if criteria not in train_data.columns:
            print(f'Criteria column not found in CSV: {criteria}')
            return jsonify([])

        # Sort products by the selected criteria and order
        sorted_products = train_data.sort_values(by=criteria, ascending=(order == 'asc'))

        # Select and format the desired columns
        products = sorted_products[['ID', 'Rating', 'ReviewCount', 'Category', 'Brand', 'Name', 'ImageURL', 'Description', 'Tags', 'Price']].to_dict(orient='records')

        return jsonify(products)
    except Exception as e:
        print('Error loading or sorting CSV file:', e)
        return jsonify([])
