import schedule
import time
import threading
import Get_SteamGames
import Send_Message


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every().day.at("1:00").do(run_threaded, Get_SteamGames.main)
schedule.every().day.at("8:00").do(run_threaded, Send_Message.main)


while True:
    schedule.run_pending()
    time.sleep(1)
