
# Load synonyms from JSON file
def load_synonyms(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Load your synonyms
synonyms = load_synonyms('custom-json/synonyms.json')


def get_synonyms(search_term):
    matched_synonyms = []
    for key, values in synonyms.items():
        if search_term.lower() in key:
            matched_synonyms.extend(values)
    return matched_synonyms


def content_based_recommendations(train_data, item_name, top_n=10):
    item_name = item_name.lower().strip()

    # Get synonyms
    synonym_matches = get_synonyms(item_name)

    # Prepare a list to hold all matches
    matches = []

    # First, find brand matches
    brand_matches = train_data[train_data['Brand'].str.lower().str.contains(item_name, na=False)]
    for index, row in brand_matches.iterrows():
        matches.append((index, row['Name'], row['Brand'], 1.5))  # Higher weight for brand matches

    # Now, find name matches
    name_matches = train_data[train_data['Name'].str.lower().str.contains(item_name, na=False)]
    for index, row in name_matches.iterrows():
        matches.append((index, row['Name'], row['Brand'], 1.0))  # Regular weight for name matches

    # Check for synonyms in brand and name
    for synonym in synonym_matches:
        synonym_brand_matches = train_data[train_data['Brand'].str.lower().str.contains(synonym.lower(), na=False)]
        for index, row in synonym_brand_matches.iterrows():
            matches.append((index, row['Name'], row['Brand'], 1.2))  # Slightly higher weight for synonym brand matches

        synonym_name_matches = train_data[train_data['Name'].str.lower().str.contains(synonym.lower(), na=False)]
        for index, row in synonym_name_matches.iterrows():
            matches.append((index, row['Name'], row['Brand'], 1.0))  # Regular weight for synonym name matches

    # Sort matches based on the score (weights)
    matches.sort(key=lambda x: x[3], reverse=True)

    # Collect the top-n recommendations
    recommended_indices = [match[0] for match in matches[:top_n]]

    # Return the relevant details including 'Price'
    return train_data.iloc[recommended_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating', 'Price']]
