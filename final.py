import streamlit as st
import pandas as pd
import random

anime_data = pd.read_csv('new_dataset.csv')

# Title of the web app
st.title('Anime Recommendation System')

genre_mapping = {
    1: 'Romance',
    2: 'Action',
    3: 'Supernatural',
    4: 'Sports',
    5: 'Adventure',
    6: 'Comedy',     
    7: 'Mystery',   
}


st.write('Choose a genre:')
col1, col2, col3 = st.columns(3)  
col4, col5, col6 = st.columns(3)  

# Create a list to store containers
containers = [col1.empty(), col2.empty(), col3.empty(), col4.empty(), col5.empty(), col6.empty()]

# Initialize selected_genre outside the loop
selected_genre = None

# Iterate over the first 6 genres
for code, genres in list(genre_mapping.items())[:6]:
    index = code - 1
    with containers[index]:
        button_clicked = st.button(genres, key=f"genre_button_{code}")
        if button_clicked:
            selected_genre = genres  

def get_unique_indices(all_indices, shown_indices, num_recommendations=2):
    remaining_indices = set(all_indices) - set(shown_indices)
    unique_indices = random.sample(list(remaining_indices), min(num_recommendations, len(remaining_indices)))
    return unique_indices

if selected_genre:
    st.header(f'Top Rated Anime in the {selected_genre} Genre')

    genre_anime = anime_data[anime_data['genres'].str.contains(selected_genre, case=False, na=False)]

    
    all_indices = list(genre_anime.index)
    shown_indices = st.session_state.get('shown_indices', [])

    remaining_indices = get_unique_indices(all_indices, shown_indices, num_recommendations=2)

    if not remaining_indices:
        shown_indices = []

    shown_indices.extend(remaining_indices)

    st.session_state.shown_indices = shown_indices


    for selected_index in remaining_indices:
        for _, top_anime in genre_anime.loc[[selected_index]].iterrows():
            st.write(f"**Title:** {top_anime['title']}")
            st.write(f"**Type:** {top_anime['type']}")
            st.write(f"**Score:** {top_anime['score']}")
            st.image(top_anime['main_picture'], caption='Anime Image', use_column_width=True)
            st.write(f"**Trailer Link:** [{top_anime['title']} Trailer]({top_anime['trailer_url']})")
            st.write('---')  # Add a horizontal line between recommendations

    #  User Quotes
    user_quote = st.text_input('Share your favorite anime quote:')
    if user_quote:
        st.success(f'Thanks for sharing! Your quote: "{user_quote}"')




# Styling ----------------------------------------------------------------------------------------------------------

st.sidebar.title('About')
st.sidebar.info(
    "This is a simple anime recommendation system built with Streamlit.\n\n"
    "Feel free to explore different genres and discover new anime!\n\n"
    "Created by Anmol Deol"
)

# ----------------------------------------------------------------------------------------------------------
anime_quotes = [
    "It’s not the face that makes someone a monster; it’s the choices they make with their lives.",
    "The only ones who should kill are those who are prepared to be killed!",
    "No one knows what the future holds. That’s why its potential is infinite.",
    "When you have to save someone, they’re usually in a scary situation. So isn’t it scarier to think no one will come to save you?",
    "The world is not beautiful, and that, in a way, lends it a sort of beauty.",
]

st.sidebar.header('Anime Quote of the Day')
st.sidebar.write(random.choice(anime_quotes))
