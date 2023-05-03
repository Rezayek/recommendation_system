from firebase_connector import FirebaseManager
import pytest

@pytest.fixture()
def instance():
    return FirebaseManager()

@pytest.mark.parametrize("model_version, new_recommendation", [
    (2, [
        {'tag': 'supernatural', 'occ_number': 13, 'novels_id': tuple([1, 3, 4, 7, 8, 9, 10, 14, 17, 19, 29, 33, 36])},
        {'tag': 'horror', 'occ_number': 12, 'novels_id': tuple([1, 3, 7, 8, 9, 10, 14, 23, 29, 33, 37, 39])},
        {'tag': 'virtual reality', 'occ_number': 11, 'novels_id': tuple([1, 4, 7, 9, 10, 13, 19, 29, 31, 33, 36])},
        {'tag': 'magic', 'occ_number': 12, 'novels_id': tuple([3, 7, 8, 9, 10, 19, 23, 26, 29, 31, 33, 37])},
    ])
])
def test_firebase(instance,model_version, new_recommendation):
    
    res = instance.add_new_doc(model_version, new_recommendation)
    assert res == True
    
def test_previous(instance):
    prev = instance.get_model_previous_version()
    assert prev['is_active'] == True