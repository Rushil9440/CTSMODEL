import schedule
import time
from db_operations import get_all_data
from send_email import send_email
import threading


def query_data_and_send_email():
    records = get_all_data()

    counter = 0
    for record in records:
        if record['email']:
            send_email(record)  
            counter+=1
    return counter


def job():
    result = query_data_and_send_email()
    print(f"Emails sent out: {result}")

    # To schedule daily emails:
    # schedule.every().day.at("07:00").do(job) 

    #schedule.every(1).minute.do(job)
job_id=schedule.every(30).seconds.do(job)
print("FSDF",job_id)

def  run_scheduler():
    while True:
        schedule.run_pending()
        print("RUNNING!!!!!!")
        time.sleep(1)        

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()