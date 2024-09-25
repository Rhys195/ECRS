@app.route("/cbr", methods=['POST'])
def cbr():
    if request.method == 'POST':
        prod = request.form.get('prod')
        nbr_str = request.form.get('nbr', '')

        try:
            nbr = int(nbr_str) if nbr_str else 8
        except ValueError:
            nbr = 10

        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)

        # Load data for categorized products
        df = pd.read_csv('models/clean_data.csv')
        categories = df['Category'].unique()
        categorized_products = {
            category: df[df['Category'] == category].head(10) for category in categories
        }

        if content_based_rec.empty:
            message = "No recommendations available for this product."
        else:
            message = None  # Set to None if there are recommendations

        cart_count = len(session.get('cart', {}))  # Check cart count from session for guest users

        return render_template(
            'search_results.html',
            message=message,
            content_based_rec=content_based_rec,  # Always pass this
            truncate=truncate,
            user=session.get('username'),
            cart_count=cart_count,
            categorized_products=categorized_products,
        )
