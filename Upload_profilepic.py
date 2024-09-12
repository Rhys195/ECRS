ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def save_profile_pic(file, user_id):
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # If user_id is provided, update the user's profile_pic in the database
    if user_id:
        user = User.query.get(user_id)
        user.profile_pic = filename
        db.session.commit()

    return filename
