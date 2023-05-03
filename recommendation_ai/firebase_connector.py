import firebase_admin
from firebase_admin import credentials, firestore
from util.config import settings

def singleton(class_instance):
    instances = {}
    def get_instance(*args, **kwargs):
        if class_instance not in instances:
            instances[class_instance] = class_instance(*args, **kwargs)
        return instances[class_instance]
    return get_instance

@singleton
class FirebaseManager:
    
    def __init__(self):
        cred = credentials.Certificate(f"{settings.CRED_File}")
        firebase_admin.initialize_app(cred)
        firestore_db = firestore.client()
        self.collection = firestore_db.collection(u'Recommended_novels')
    
    def get_model_previous_version(self):
        return (self.collection.where('is_active', '==', True).get())[0].to_dict()
    
    def add_new_doc(self, model_version, new_recommendation):
        
        if model_version > 1:
            self.collection.document(f'recommendation_model_v{model_version - 1}').update({u'is_active': False})
        
        new_doc = self.collection.document(f'recommendation_model_v{model_version}')
        
        data_set = {
            'is_active': True,
            'model_version': model_version,
            'tag_1': new_recommendation[0]['tag'],
            'tag_1_novels_id': new_recommendation[0]['novels_id'],
            'tag_2': new_recommendation[1]['tag'],
            'tag_2_novels_id': new_recommendation[1]['novels_id'],
            'tag_3': new_recommendation[2]['tag'],
            'tag_3_novels_id': new_recommendation[2]['novels_id'],
            'tag_4': new_recommendation[3]['tag'],
            'tag_4_novels_id': new_recommendation[3]['novels_id'],
        }
        
        new_doc.set(data_set)
        
        return True
        
        