@app.route('/cart')
def cart():
    user_id = session.get('user_id')
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    # Prepare item details including image URLs
    items_with_details = []
    for item in cart_items:
        product_details = product_lookup.get(item.product_name, {})
        image_url = product_details.get('ImageURL', '/static/images/placeholder.png')
        price = random.choice([40, 50, 60, 70, 100, 122, 106, 50, 30, 50])  # Adjust this to your actual price logic
        items_with_details.append({
            'product_name': item.product_name,
            'quantity': item.quantity,
            'image_url': image_url,
            'price': price
        })

    # Calculate total price
    total_price = sum(item['price'] * item['quantity'] for item in items_with_details)

    return render_template('cart.html', cart_items=items_with_details, total_price=total_price)

@app.route('/remove_from_cart/<string:product_name>', methods=['POST'])
def remove_from_cart(product_name):
    user_id = session.get('user_id')
    cart_item = CartItem.query.filter_by(user_id=user_id, product_name=product_name).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash(f'{product_name} has been removed from your cart.', 'success')
    else:
        flash(f'{product_name} is not in your cart.', 'warning')

    return redirect(url_for('cart'))


@app.route('/update_cart_quantity/<string:product_name>', methods=['POST'])
def update_cart_quantity(product_name):
    user_id = session.get('user_id')
    cart_item = CartItem.query.filter_by(user_id=user_id, product_name=product_name).first()

    action = request.form.get('action')

    if cart_item:
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                flash(f'Cannot reduce {product_name} quantity below 1.', 'warning')
        db.session.commit()
        flash(f'{product_name} quantity has been updated.', 'success')
    else:
        flash(f'{product_name} is not in your cart.', 'warning')

    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    # Implement checkout functionality
    return render_template('checkout.html', cart_items=session.get('cart', {}))
