@app.route('/product/<product_name>')
def product_page(product_name):
    # Load data from clean_data.csv
    try:
        clean_data = pd.read_csv('models/clean_data.csv')
    except Exception as e:
        flash(f'Error loading product data: {str(e)}', 'danger')
        return redirect(url_for('index'))

    product_name = unquote(product_name)

    # Find the product by name in the dataset
    matching_products_clean = clean_data[clean_data['Name'].str.contains(product_name, case=False, na=False, regex=False)]

    if not matching_products_clean.empty:
        product = matching_products_clean.iloc[0]
    else:
        flash('Product not found.', 'danger')
        return redirect(url_for('index'))

    # Split the 'ImageURL' into a list if it contains multiple URLs
    product_images = [url.strip() for url in product['ImageURL'].split('|')]

    product_price = product['Price']
    product_rating = product['Rating']

    # Fetch related products using content-based recommendations
    related_products_df = content_based_recommendations(clean_data, product['Name'])

    # Convert the related products DataFrame to a list of dictionaries
    related_products = related_products_df.to_dict(orient='records') if not related_products_df.empty else []

    return render_template(
        'product.html',
        product=product,
        product_images=product_images,
        product_price=product_price,
        product_description=product['Description'],
        related_products=related_products,product_rating=product_rating, truncate=truncate
    )
