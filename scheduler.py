from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler():
    scheduler = BackgroundScheduler()

    # Exemplo futuro:
    # scheduler.add_job(sync_transacoes, "interval", hours=6)

    scheduler.start()