import json
import numpy as np
import tensorflow as tf
from util.config import settings

def train_model(new_model_id):
    # Load the reviews from the JSON file
    with open("data_sets/reviews.json", "r") as f:
        reviews = json.load(f)
        
    # Convert the reviews to a numpy array
    ratings = np.array([review["rating"] for review in reviews])
    novel_ids = np.array([review["novel_id"] for review in reviews])
    user_ids = np.array([review["user_id"] for review in reviews])

    # Define the number of unique novels and users
    num_novels = np.max(novel_ids) + 1
    num_users = np.max(user_ids) + 1

    # Split the data into training and testing sets
    num_samples = len(ratings)
    indices = np.arange(num_samples)
    np.random.shuffle(indices)
    train_indices = indices[:int(0.8 * num_samples)]
    test_indices = indices[int(0.8 * num_samples):]
    train_ratings = ratings[train_indices]
    train_novel_ids = novel_ids[train_indices]
    train_user_ids = user_ids[train_indices]
    test_ratings = ratings[test_indices]
    test_novel_ids = novel_ids[test_indices]
    test_user_ids = user_ids[test_indices]

    # Define the TensorFlow model
    novel_input = tf.keras.layers.Input(shape=(1, ))
    novel_embedding = tf.keras.layers.Embedding(num_novels, 16)(novel_input)
    novel_vec = tf.keras.layers.Flatten()(novel_embedding)

    user_input = tf.keras.layers.Input(shape=(1, ))
    user_embedding = tf.keras.layers.Embedding(num_users, 16)(user_input)
    user_vec = tf.keras.layers.Flatten()(user_embedding)

    concat = tf.keras.layers.concatenate([novel_vec, user_vec])
    dense1 = tf.keras.layers.Dense(128, activation="relu")(concat)
    dense2 = tf.keras.layers.Dense(64, activation="relu")(dense1)
    dense3 = tf.keras.layers.Dense(32, activation="relu")(dense2)
    output = tf.keras.layers.Dense(1)(dense3)

    model = tf.keras.models.Model(inputs=[novel_input, user_input], outputs=output)

    # Compile and fit the model
    model.compile(optimizer="adam", loss="mse")


    # Define the TensorBoard callback
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir="logs",
        histogram_freq=1,
        write_graph=True,
        write_images=True
    )

    # Define the threshold for the minimum acceptable loss value
    min_loss = settings.MIN_LOSS
    
    
    # The neural network in the code is a type of collaborative filtering model 
    # called a matrix factorization model. 
    # It consists of two embedding layers (one for the novels and one for the users) 
    # and several fully connected (dense) layers that combine the embeddings to make a prediction. 
    # This type of model is commonly used for recommendation systems.
    while True:
        history = model.fit([train_novel_ids, train_user_ids],
                            train_ratings,
                            epochs=settings.EPOCHS,
                            batch_size=settings.BATCH_SIZE,
                            validation_split=0.2,
                            callbacks=[tensorboard_callback])
        
        train_loss = history.history['loss'][-1]
        if train_loss < min_loss:
            break

    model.save(f"models/recommendation_model_v{new_model_id}.h5")

    # Evaluate the model on the testing set
    test_loss = model.evaluate([test_novel_ids, test_user_ids], test_ratings)
    print("Test loss:", test_loss)

    threshold = 3.5
    predicted_ratings = model.predict([test_novel_ids, test_user_ids])
    predicted_labels = (predicted_ratings >= threshold).astype(int)
    true_labels = (test_ratings >= threshold).astype(int)

    # Calculate precision and recall
    tp = np.sum(np.logical_and(predicted_labels == 1, true_labels == 1))
    fp = np.sum(np.logical_and(predicted_labels == 1, true_labels == 0))
    tn = np.sum(np.logical_and(predicted_labels == 0, true_labels == 0))
    fn = np.sum(np.logical_and(predicted_labels == 0, true_labels == 1))

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    print("Precision:", precision)
    print("Recall:", recall)
