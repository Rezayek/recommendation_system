import numpy as np
import tensorflow as tf
import json


def recomendation(user_id, new_model_id):
    
    # Load the model from the file
    model = tf.keras.models.load_model(f"models/recommendation_model_v{new_model_id}.h5")

    #load novels
    with open("data_sets/novels.json", "r") as f:
        novels = json.load(f)

    # Make predictions for a new user and novel
    
    result = []
    
    novels_len = len(novels) + 1

    for i in range(1, novels_len):
        predicted_rating = model.predict([np.array([i]), np.array([user_id])])
        result.append({"user_id": user_id, "novel_id":i, "predicted_rating":  round(predicted_rating[0][0])})
    
    def remove_low_rating(rating):
        if(rating["predicted_rating"] <= 2):
            return False
        else:
            return True
    
    def return_novel_id(rating):
        return rating["novel_id"]
    
    recomended_novel_id = list(map(return_novel_id, filter(remove_low_rating, result)))
    
    tags = []
    
    def search(tag_name):
        
        if len(tags) == 0:
            return {"result": False, "index":0}
        
        for tag in tags:
            if tag['tag'] == tag_name:
                return {"result": True, "index": tags.index(tag) }
        return {"result": False, "index":0}
    
    def generate_commun_tags(novel_id):
        
        for tag in novels[novel_id]["tags"]:
            
            search_result = search(tag)
            
            if search_result["result"]:
                index = search_result["index"]
                tags[index]["occ_number"] = tags[index]["occ_number"] + 1
                if novel_id not in tags[index]["novels_id"]:
                    tags[index]["novels_id"].append(novel_id)
                    
            else: 
                tags.append({"tag": tag, "occ_number": 1, "novels_id":[novel_id]})   
                       
    for id in recomended_novel_id:
        
        generate_commun_tags(id - 1)
        
    return sorted(tags, key=lambda d: d['occ_number'], reverse=True)[0:4]
    
    
    
              

