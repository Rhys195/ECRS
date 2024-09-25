def save_profile_pic(file, user_id=None):
    # Generate a unique filename using UUID
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Ensure the upload directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    try:
        # Save the file to the specified directory
        file.save(filepath)
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

    # If user_id is provided, update the user's profile picture in the database
    if user_id:
        user = User.query.get(user_id)
        if user:
            try:
                # Update the profile_pic field with the generated filename
                user.profile_pic = filename
                db.session.commit()
            except Exception as e:
                print(f"Error updating user profile picture in database: {e}")
                return None

    return filename  # Return the generated filename

