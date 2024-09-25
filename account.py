@app.route("/account", methods=['GET', 'POST'])
def account():
    if not session.get('user_id'):
        return redirect(url_for('index'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.password = generate_password_hash(password)

            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Profile updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'danger', 'message': 'Error updating profile: ' + str(e)}), 500

    return render_template('account.html', user=user)
