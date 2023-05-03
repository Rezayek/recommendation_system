import random
import json

# Define a list of potential tags
potential_tags = ['fantasy', 'adventure', 'romance', 'action', 'magic', 'comedy', 'drama', 'isekai', 'reincarnation', 'cultivation', 'villain protagonist', 'female protagonist', 'game elements', 'virtual reality', 'harem', 'martial arts', 'supernatural', 'science fiction', 'horror', 'mystery']


# Define the number of lists to generate
num_lists = 50

# Define the minimum and maximum number of tags per list
min_tags = 5
max_tags = 15

# Load the existing data from the JSON file
with open('data_sets/novels.json', 'r') as f:
    data = json.load(f)

# Generate the lists of tags and update the corresponding novels in the data
for i in range(num_lists):
    # Choose a random number of tags for this list
    num_tags = random.randint(min_tags, max_tags)
    # Choose that many tags at random from the potential_tags list
    tags = random.sample(potential_tags, num_tags)
    # Update the corresponding novel in the data with the new tags
    data[i]['tags'] = tags

# Write the updated data back to the JSON file
with open('data_sets/novels.json', 'w') as f:
    json.dump(data, f, indent=2)