import json

new_data = {'name': 'John', 'age': 30}

def add_new_novel(novel_data):
    
    try:
        data = json.loads(novel_data)
        
        with open('data_sets/novels.json', "r") as r:
            existing_data = json.load(r)
            
            # append new data to existing list
            existing_data.append(data)
            
            with open('data_sets/novels.json', "w") as w:
                json.dump(existing_data, w, indent=4)

        return True
    
    except:
        return False
        
        
def add_new_review(review_data):
    
    try:
        data = json.loads(review_data)
        
        with open('data_sets/reviews.json', "r") as r:
            existing_data = json.load(r)
            
            # append new data to existing list
            existing_data.append(data)
            
            with open('data_sets/reviews.json', "w") as w:
                json.dump(existing_data, w, indent=4)

        return True
    
    except:
        return False