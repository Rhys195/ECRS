@app.route('/categories')
def get_categories():
    # Read the CSV file
    train_data = pd.read_csv("models/clean_data.csv")

    # Extract unique categories
    categories = train_data['Category'].unique().tolist()

    return jsonify(categories)
