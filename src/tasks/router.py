from fastapi import APIRouter, Depends, Request
from fastapi.background import BackgroundTasks
from src.auth.base_config import current_user
from src.pages.base.router import templates
from src.tasks.tasks import send_email_report_dashboard

router = APIRouter(
    prefix='/report',
    tags=['Report']
    )


@router.get('/dashboards')
async def get_dashboard_report_email(request: Request, background_tasks: BackgroundTasks, user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username, user.email) # this is for celery+redis+flower (or without flower)
    # background_tasks.add_task(
    #     send_email_report_dashboard, user.username, user.email
    # ) # this is default fastapi background task function
    return templates.TemplateResponse('base.html',
                                      {'request': request})
