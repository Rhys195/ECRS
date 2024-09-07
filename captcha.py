def generate_captcha_text(length=6):
    # Generate random text
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    # Convert text to list and scramble
    text_list = list(text)
    random.shuffle(text_list)
    scrambled_text = ''.join(text_list)
    return scrambled_text


def create_captcha_image(text, width=200, height=60):
    # Create a new image with specified width and height
    image = Image.new('RGB', (width, height), color=(255, 255, 255))

    # Initialize drawing context
    draw = ImageDraw.Draw(image)

    # Load a custom font with a specific size
    font_size = 30  # Adjust font size as needed
    font = ImageFont.truetype("arial.ttf", font_size)

    # Calculate text size to center it
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    # Draw the text onto the image
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    # Distorted text
    for i, char in enumerate(text):
        x_offset = random.randint(-5, 5)
        y_offset = random.randint(-5, 5)
        draw.text((text_x + x_offset, text_y + y_offset), char, font=font, fill=(0, 0, 0))
        text_x += font.getsize(char)[0]

    # Add noise
    for _ in range(50):  # Number of noise points
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill=(0, 0, 0))

    return image


@app.route('/generate_captcha_image')
def generate_captcha():
    captcha_text = generate_captcha_text()
    width, height = 200, 60
    image = create_captcha_image(captcha_text, width, height)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    # Store CAPTCHA text in session
    session['captcha_text'] = captcha_text

    return send_file(image_bytes, mimetype='image/png')


@app.route('/verify_captcha', methods=['POST'])
def verify_captcha():
    user_input = request.form.get('captcha')
    stored_captcha_text = session.get('captcha_text')
    if user_input == stored_captcha_text:
        return jsonify({"status": "success", "message": "CAPTCHA verified"})
    else:
        return jsonify({"status": "error", "message": "Incorrect CAPTCHA"})
