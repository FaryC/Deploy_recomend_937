
import streamlit as st
import pickle

# Load the SVD model and data
with open('65130701937recommendation_movie_svd.pkl', 'rb') as file:
    svd_model, movie_ratings, movies = pickle.load(file)

# Define a function to get top movie recommendations for a given user
def get_recommendations(user_id, num_recommendations=10):
    rated_user_movies = movie_ratings[movie_ratings['userId'] == user_id]['movieId'].values
    unrated_movies = movies[~movies['movieId'].isin(rated_user_movies)]['movieId']
    pred_rating = [svd_model.predict(user_id, movie_id) for movie_id in unrated_movies]
    sorted_predictions = sorted(pred_rating, key=lambda x: x.est, reverse=True)
    top_recommendations = sorted_predictions[:num_recommendations]
    
    # Create a list of movie titles and estimated ratings
    recommendations = []
    for recommendation in top_recommendations:
        movie_title = movies[movies['movieId'] == recommendation.iid]['title'].values[0]
        recommendations.append(f"{movie_title} (Estimated Rating: {recommendation.est:.2f})")
    return recommendations

# Streamlit App Interface
st.title("Movie Recommendation System")

# User Input
user_id = st.number_input("Enter User ID:", min_value=1, step=1)

# Button to get recommendations
if st.button("Get Recommendations"):
    recommendations = get_recommendations(user_id)
    if recommendations:
        st.subheader(f"Top 10 Movie Recommendations for User {user_id}:")
        for movie in recommendations:
            st.write(movie)
    else:
        st.write("No recommendations available for this user.")

