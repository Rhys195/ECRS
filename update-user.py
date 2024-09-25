@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"status": "error", "message": "User not found"}), 404

    return jsonify({
        "status": "success",
        "profile_pic": url_for('static', filename='profile_pics/' + user.profile_pic),
        "username": user.username
    }), 200


@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"status": "error", "message": "User not found"}), 400

    response_data = {}

    # Handle profile picture change (if applicable)
    if 'profilePic' in request.files:
        profile_pic = request.files['profilePic']
        if profile_pic:
            filename = save_profile_pic(profile_pic, user_id=user_id)
            if filename is None:
                return jsonify({"status": "error", "message": "Failed to upload profile picture"}), 500
            session['profile_pic'] = filename
            new_profile_pic_url = url_for('static', filename='profile_pics/' + filename)
            response_data['new_profile_pic'] = new_profile_pic_url

    # Handle username change
    new_username = request.form.get('username')
    if new_username and new_username != user.username:
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            return jsonify({"status": "error", "message": "Username already exists"}), 400

        user.username = new_username
        session['username'] = new_username
        response_data['new_username'] = new_username

    # Handle password change
    current_password = request.form.get('currentPassword')
    new_password = request.form.get('newPassword')

    if current_password and new_password:
        # Verify the current password
        if not check_password_hash(user.password, current_password):
            return jsonify({"status": "error", "message": "Current password is incorrect"}), 400

        # Ensure the new password is different
        if check_password_hash(user.password, new_password):
            return jsonify({"status": "error", "message": "New password cannot be the same as the old password"}), 400

        # Update the password
        user.password = generate_password_hash(new_password)
        session.clear()  # Clear session after password update
        db.session.commit()  # Commit changes to the database
        return jsonify({"status": "success", "message": "Password changed, please log in again"}), 200

    # If we reach this point, commit all changes
    db.session.commit()

    return jsonify({"status": "success", "message": "Profile updated successfully", **response_data}), 200
