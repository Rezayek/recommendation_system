import json
import random

# Load the novels from the JSON file
with open("data_sets/novels.json", "r") as f:
    novels = json.load(f)

# Define a list of genders and ages for the reviewers
genders = ["male", "female", "non-binary"]
ages = range(14, 70)

# Define the range of possible ratings
ratings = range(1, 6)

# Define the number of reviews to generate
num_reviews = 50

# Generate a list of random reviews
reviews = []
for i in range(0, num_reviews):
    # Select a random novel
    novel = novels[i]
    
    
    for j in range(0, random.randint(100,5000)):
        # Generate a random user ID
        user_id = j  + 1
        
        # Select a random gender and age for the reviewer
        gender = random.choice(genders)
        age = random.choice(ages)
        
        # Generate a random rating for the novel
        rating = random.choice(ratings)
        
        # Create a new review object and add it to the list of reviews
        review = {
            "user_id": user_id,
            # "gender": gender,
            # "age": age,
            "novel_id": novel["id"],
            # "novel_title": novel["title"],
            # "novel_tags": novel["tags"],
            "rating": rating
        }
        reviews.append(review)

# Save the reviews to a JSON file
with open("data_sets/reviews.json", "w") as f:
    json.dump(reviews, f, indent=4)
