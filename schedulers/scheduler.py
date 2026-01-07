from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from trigger_agent import run_daily_analysis

scheduler = BlockingScheduler(timezone="Europe/Paris")


def daily_job():
    print(f"[{datetime.now()}] Daily run triggered")
    try:
        run_daily_analysis()
        print(f"[{datetime.now()}] Daily analysis completed")
    except Exception as e:
        print(f"[{datetime.now()}] Daily analysis failed: {e}")


scheduler.add_job(
    daily_job,
    trigger="cron",
    hour=10,
    minute=0,
)

if __name__ == "__main__":
    print("Scheduler started")
    scheduler.start()
