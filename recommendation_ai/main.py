from firebase_connector import FirebaseManager
from model_trainning import train_model
from prediction import recomendation
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from middleware_listenner.novels_listenner import run_novel_listener
from middleware_listenner.reviews_listenner import run_review_listener
from util.config import settings
import threading


def recommendation_service():
    
    conn = FirebaseManager()
    new_version = conn.get_model_previous_version()['model_version'] + 1
    train_model(new_version)
    result = recomendation(1, new_version)
    conn.add_new_doc(new_version, result)


def run_recommendation():
    
    print("[*] recommendation service : start.\n")
    # Start the recommendation service scheduler
    scheduler = BlockingScheduler()
    trigger = CronTrigger(day='*/30')
    scheduler.add_job(recommendation_service, trigger=trigger, misfire_grace_time= settings.ESTIMTED_WORK_DAY * 24 * 3600)
    scheduler.start()

if __name__ == "__main__":

    # # Start the novel listener in a separate thread
    novel_listener_thread = threading.Thread(target=run_novel_listener)
    novel_listener_thread.start()

    # Start the review listener in a separate thread
    review_listener_thread = threading.Thread(target=run_review_listener)
    review_listener_thread.start()
    
    # Start the recommendation service in a separate thread
    recommendation_thread = threading.Thread(target=run_recommendation)
    recommendation_thread.start()
    

    # Wait for the user to stop the threads
    while True:
        # Check for user input to stop the threads
        input_key = input("Press 'ctrl+shift+r' to stop the novel listener or 'ctrl+shift+n' to stop the review listener or 'ctrl+shift+c' to stop recommendation model\n")

        if input_key == "ctrl+shift+r":
            # Stop the novel listener thread
            novel_listener_thread.stop()
            print("shutdown novel listener\n")
            break

        elif input_key == "ctrl+shift+n":
            # Stop the review listener thread
            review_listener_thread.stop()
            print("shutdown novel review\n")
            break
        
        elif input_key == "ctrl+shift+c":
            # Stop the recommendation model thread
            review_listener_thread.stop()
            print("shutdown recommendation model\n")
            break
    
    novel_listener_thread.join()
    review_listener_thread.join()
    recommendation_thread.join()