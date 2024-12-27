from apscheduler.schedulers.background import BackgroundScheduler


def run():
    pass
    # sched = BackgroundScheduler()
    # sched.add_job(scrap_gongo, 'cron', hour=3)
    # sched.add_job(scrap_gongo, trigger='date')
    # sched.start()


if __name__ == '__main__':
    run()
