@app.route('/send_forgot_password_otp', methods=['POST'])
def send_forgot_password_otp():
    email = request.form['email']
    username = request.form.get('username')  # get() method to handle cases where username might be missing

    # Query to check if the user exists
    user = User.query.filter_by(email=email).first()

    if user:
        otp = generate_otp()  # Assuming generate_otp is a function that generates OTP
        from modelstemp import TempUser
        # Set a default username and an empty password if not provided
        temp_user = TempUser(email=email, otp=otp, username=username or 'default_username', password='')
        db.session.add(temp_user)
        db.session.commit()

        # Send the OTP via email
        msg = Message('Your OTP Code', sender='colleilili475@gmail.com', recipients=[email])
        msg.body = f'Your OTP code is {otp}.'
        mail.send(msg)

        return jsonify({'status': 'success', 'message': 'OTP sent to your email!'})
    else:
        return jsonify({'status': 'error', 'message': 'Email not found!'})


@app.route('/verify_forgot_password_otp', methods=['POST'])
def verify_forgot_password_otp():
    otp = request.form['otp']

    from modelstemp import TempUser
    temp_user = TempUser.query.filter_by(otp=otp).first()

    if temp_user:
        # OTP is valid; return success status
        return jsonify({'status': 'success', 'message': 'OTP verified. Proceed to reset password.'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid OTP.'})


@app.route('/reset_password', methods=['POST'])
def reset_password():
    new_password = request.form.get('newPassword')
    otp = request.form.get('otp')  # OTP is sent along with the new password

    print(f"Received OTP: {otp}")  # Debugging line
    print(f"Received new password: {new_password}")
    # Validate the new password (example: check length and complexity)
    if len(new_password) < 8:  # Example condition
        flash('Password must be at least 8 characters long.', 'danger')
        return redirect(url_for('index'))

    # Validate OTP and find associated TempUser record
    from modelstemp import TempUser
    temp_user = TempUser.query.filter_by(otp=otp,).first()

    print(f"Received OTP: {otp}")
    print(f"TempUser found: {temp_user}")

    if temp_user:
        try:
            # Hash the new password
            hashed_password = generate_password_hash(new_password)
            print(f"Hashed password: {hashed_password}")

            # Find the actual user and update the password
            user = User.query.filter_by(email=temp_user.email).first()
            print(f"User found: {user}")

            if user:
                user.password = hashed_password
                db.session.commit()

                # Optionally remove TempUser record
                db.session.delete(temp_user)
                db.session.commit()

                # Flash a success message
                flash('Your password has been successfully reset.', 'success')

                # Redirect to the sign-in page or home page
                return redirect(url_for('index'))

            else:
                flash('User not found.', 'danger')
                return redirect(url_for('index'))

        except Exception as e:
            print(f"Error: {e}")  # Log the exception
            db.session.rollback()
            flash('An error occurred while resetting your password. Please try again.', 'danger')
            return redirect(url_for('index'))

    else:
        flash('Invalid OTP.', 'danger')
        return redirect(url_for('index'))