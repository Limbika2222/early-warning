from apscheduler.schedulers.background import (
    BackgroundScheduler,
)

from app.utils.database import (
    SessionLocal,
)

from app.services.anomaly_detection import (
    run_anomaly_detection,
)

# =====================================================
# JOB
# =====================================================

def anomaly_job():

    db = SessionLocal()

    try:

        print(
            "🚨 Running anomaly engine..."
        )

        run_anomaly_detection(db)

        print(
            "✅ Anomaly scan complete"
        )

    finally:

        db.close()

# =====================================================
# SCHEDULER
# =====================================================

scheduler = BackgroundScheduler()

scheduler.add_job(

    anomaly_job,

    trigger="interval",

    minutes=15,
)

# =====================================================
# START
# =====================================================

def start_scheduler():

    if not scheduler.running:

        scheduler.start()

        print(
            "✅ Scheduler started "
            "(15 minute interval)"
        )