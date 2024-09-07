<h3 align="left">Hybrid Recommendation System:</h3>

<h3 align="left">Overview:</h3>
This project implements a hybrid recommendation system that combines the strengths of multiple recommendation algorithms to provide personalized recommendations to users. The system integrates content-based filtering, collaborative filtering, and matrix factorization techniques to achieve high accuracy and diversity in its recommendations.

<h3 align="left">Features:</h3>
Hybrid Recommendation Algorithm: Combines content-based filtering, collaborative filtering, and matrix factorization to provide accurate and diverse recommendations.
Personalized Recommendations: Provides users with personalized recommendations based on their past behavior and preferences.
<h3 align="left">Scalability:</h3> Designed to handle large datasets and scale horizontally to meet the needs of growing user bases.
<h3 align="left">Flexibility:</h3> Allows for easy integration with various data sources and formats.

<h3 align="left">Getting Started:</h3>

<h3 align="left">Prerequisites:</h3>
Python 3.8+
NumPy
Pandas
SciPy
Scikit-learn
TensorFlow
Keras

<h3 align="left">Installation:</h3>
<h3 align="left">Clone the repository:</h3> git clone https://github.com/your-username/hybrid-recommendation-system.git
<h3 align="left">Install the required packages:</h3> pip install -r requirements.txt
<h3 align="left">Run the application:</h3> python app.py

<h3 align="left">Usage</h3>
Data Preparation
Prepare your dataset in CSV format with the following columns:
user_id: Unique identifier for each user.
item_id: Unique identifier for each item.
rating: Rating given by the user to the item.
Split your dataset into training and testing sets (e.g., 80% for training and 20% for testing).
Training the Model
Run the training script: python train.py --data_path=/path/to/your/dataset.csv
The model will be trained and saved to the models directory.
Making Predictions
Run the prediction script: python predict.py --user_id=123 --item_id=456
The script will output the predicted rating for the given user-item pair.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import NMF

class HybridRecommender:
    def __init__(self, num_factors=10, num_iterations=50):
        self.num_factors = num_factors
        self.num_iterations = num_iterations
        self.user_factors = None
        self.item_factors = None

    def fit(self, ratings):
        # Split ratings into training and testing sets
        train_ratings, test_ratings = train_test_split(ratings, test_size=0.2, random_state=42)

        # Create user-item matrix
        user_item_matrix = self.create_user_item_matrix(train_ratings)

        # Compute content-based filtering similarity matrix
        cbf_similarity_matrix = self.compute_cbf_similarity(user_item_matrix)

        # Compute collaborative filtering similarity matrix
        cf_similarity_matrix = self.compute_cf_similarity(user_item_matrix)

        # Compute matrix factorization
        self.user_factors, self.item_factors = self.compute_matrix_factorization(user_item_matrix)

        # Combine similarities using weighted average
        self.similarity_matrix = self.combine_similarities(cbf_similarity_matrix, cf_similarity_matrix)

        # Evaluate model on testing set
        self.evaluate_model(test_ratings)

    def create_user_item_matrix(self, ratings):
        # Create user-item matrix with ratings
        user_item_matrix = ratings.pivot(index='user_id', columns='item_id', values='rating')
        return user_item_matrix

    def compute_cbf_similarity(self, user_item_matrix):
        # Compute content-based filtering similarity matrix
        cbf_similarity_matrix = cosine_similarity(user_item_matrix.T)
        return cbf_similarity_matrix

    def compute_cf_similarity(self, user_item_matrix):
        # Compute collaborative filtering similarity matrix
        cf_similarity_matrix = cosine_similarity(user_item_matrix)
        return cf_similarity_matrix

    def compute_matrix_factorization(self, user_item_matrix):
        # Compute matrix factorization using NMF
        nmf = NMF(n_components=self.num_factors, max_iter=self.num_iterations)
        user_factors = nmf.fit_transform(user_item_matrix)
        item_factors = nmf.components_.T
        return user_factors, item_factors

    def combine_similarities(self, cbf_similarity_matrix, cf_similarity_matrix):
        # Combine similarities using weighted average
        similarity_matrix = 0.5 * cbf_similarity_matrix + 0.5 * cf_similarity_matrix
        return similarity_matrix

    def evaluate_model(self, test_ratings):
        # Evaluate model on testing set
        predicted_ratings = self.predict(test_ratings)
        mse = mean_squared_error(test_ratings['rating'], predicted_ratings)
        print(f'MSE: {mse:.4f}')

    def predict(self, ratings):
        # Make predictions for given ratings
        predicted_ratings = []
        for rating in ratings.itertuples():
            user_id = rating.user_id
            item_id = rating.item_id
            user_factor = self.user_factors[user_id]
            item_factor = self.item_factors[item_id]
            predicted_rating = user_factor.dot(item_factor)
            predicted_ratings.append(predicted_rating)
        return predicted_ratings

# Load ratings data
ratings = pd.read_csv('ratings.csv')

# Create hybrid recommender
recommender = HybridRecommender()

# Fit model to ratings data
recommender.fit(ratings)

# Make predictions for a given user-item pair
user_id = 123
item_id = 456
predicted_rating = recommender.predict(pd.DataFrame({'user_id': [user_id], 'item_id': [item_id]}))
print(f'Predicted rating: {predicted_rating:.4f}')

<h3 align="left">License</h3>
This project is licensed under the MIT License. See the LICENSE file for details.
