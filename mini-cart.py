@app.route('/cart_items')
def cart_items():
    user_id = session.get('user_id')

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    items_with_details = []

    for item in cart_items:
        product_details = product_lookup.get(item.product_name, {})
        price_row = train_data[train_data['Name'] == item.product_name]
        price = int(price_row['Price'].values[0]) if not price_row.empty else 0  # Convert to int

        image_urls = product_details.get('ImageURL', '/static/images/placeholder.png')
        image_urls = image_urls.split('|')

        items_with_details.append({
            'product_name': item.product_name,
            'quantity': item.quantity,
            'image_urls': image_urls,
            'price': price
        })

    total_price = sum(int(item['price']) * int(item['quantity']) for item in items_with_details)  # Ensure types are int

    return jsonify({'cart_items': items_with_details, 'total_price': total_price})
