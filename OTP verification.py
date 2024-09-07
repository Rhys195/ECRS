def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

@app.route("/signup", methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # Verify CAPTCHA
    captcha_response = verify_captcha()  # Call to verify_captcha function
    if captcha_response.json['status'] != 'success':
        return jsonify({"status": "error", "message": "CAPTCHA verification failed"})
    hashed_password = generate_password_hash(password)
    otp = generate_otp()
    from modelstemp import TempUser
    temp_user = TempUser(username=username, email=email, password=hashed_password, otp=otp)
    db.session.add(temp_user)
    db.session.commit()

    msg = Message('Your OTP Code', sender='colleilili475@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is {otp}.'
    mail.send(msg)
    return jsonify({'status': 'success', 'message': 'Sign-up successful! Please check your email to verify your account.'})



@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    otp = request.form['otp']
    from modelstemp import TempUser
    temp_user = TempUser.query.filter_by(otp=otp).first()

    if temp_user:
        new_user = User(
            username=temp_user.username,
            email=temp_user.email,
            password=temp_user.password,
            is_verified=True,
            is_active=True
        )
        db.session.add(new_user)
        db.session.delete(temp_user)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Your account has been verified successfully!'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid OTP.'})
