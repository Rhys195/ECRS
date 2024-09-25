@app.route('/add_to_cart/<string:product_name>', methods=['POST'])
def add_to_cart(product_name):
    user_id = session.get('user_id')
    product_name = unquote(product_name)

    cart_item = CartItem.query.filter_by(user_id=user_id, product_name=product_name).first()

    if cart_item:
        cart_item.quantity += 1  # Increment quantity if item already in cart
    else:

        new_item = CartItem(user_id=user_id, product_name=product_name, quantity=1)
        db.session.add(new_item)

    db.session.commit()
    flash(f'{product_name} has been added to your cart.', 'success')
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    user_id = session.get('user_id')
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    # Prepare item details including image URLs
    items_with_details = []
    for item in cart_items:
        product_details = product_lookup.get(item.product_name, {})

        # Fetch price from the CSV based on the product name
        price_row = train_data[train_data['Name'] == item.product_name]
        price = price_row['Price'].values[0] if not price_row.empty else 0  # Default to 0 if no price found

        # Fetch image URLs
        image_urls = product_details.get('ImageURL', '/static/images/placeholder.png')
        image_urls = image_urls.split('|')  # Split the URLs if they are delimited by '|'

        items_with_details.append({
            'product_name':item.product_name,
            'quantity': item.quantity,
            'image_urls': image_urls,
            'price': price
        })

    # Calculate total price
    total_price = sum(item['price'] * item['quantity'] for item in items_with_details)

    return render_template('cart.html', cart_items=items_with_details, total_price=total_price,truncate=truncate)

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


@app.route('/remove_from_cart/<string:product_name>', methods=['POST'])
def remove_from_cart(product_name):
    product_name = unquote(product_name)
    print(f'Received product name: {product_name}')  # Log the product name received
    user_id = session.get('user_id')
    cart_item = CartItem.query.filter_by(user_id=user_id, product_name=product_name).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash(f'{product_name} has been removed from your cart.', 'success')
        return jsonify({'message': f'{product_name} has been removed from your cart.'}), 200
    else:
        flash(f'{product_name} is not in your cart.', 'warning')
        return jsonify({'error': f'{product_name} is not in your cart.'}), 404


@app.route('/update_cart_quantity/<string:product_name>', methods=['POST'])
def update_cart_quantity(product_name):
    product_name = unquote(product_name)
    user_id = session.get('user_id')

    cart_item = CartItem.query.filter_by(user_id=user_id, product_name=product_name).first()
    data = request.get_json()
    action = data.get('action')

    if cart_item:

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                return jsonify({'message': 'Cannot reduce quantity below 1.'}), 400

        db.session.commit()
        return jsonify({'message': f'{product_name} quantity has been updated.'}), 200
    else:
        return jsonify({'message': f'{product_name} is not in your cart.'}), 404


@app.route('/checkout')
def checkout():
    # Implement checkout functionality
    return render_template('checkout.html', cart_items=session.get('cart', {}))
