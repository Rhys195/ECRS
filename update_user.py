@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = session.get('user_id')
    if not user_id:
        flash('User not logged in.')
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found.')
        return redirect(url_for('index'))

    current_password = request.form.get('currentPassword')
    new_password = request.form.get('newPassword')
    username = request.form.get('username')

    if not check_password_hash(user.password, current_password):
        flash('Current password is incorrect.')
        return redirect(url_for('index'))

    if username:
        user.username = username

    if new_password:
        user.password = generate_password_hash(new_password)

    db.session.commit()
    flash('Profile updated successfully!')
    return redirect(url_for('index'))
