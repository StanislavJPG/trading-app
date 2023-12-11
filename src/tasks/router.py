from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks
from app.src.auth.base_config import current_user
from app.src.tasks.tasks import send_email_report_dashboard

router = APIRouter(
    prefix='/report',
    tags=['Report']
    )


@router.get('/dashboards')
async def get_dashboard_report_email(background_tasks: BackgroundTasks, user=Depends(current_user)):
    # send_email_report_dashboard.delay(user.username) # this is for celery+redis+flower (or without flower)
    background_tasks.add_task(
        send_email_report_dashboard, user.username
    ) # this is default fastapi background task function
    return {
        'status': 200,
        'body': 'Your letter has been sent'
    }
