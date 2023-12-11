from fastapi import APIRouter, Request, Depends

from app.pages.base.router import templates
from app.src.auth.base_config import current_user
from app.src.operations.router import get_specific_operations


router = APIRouter(
    prefix='/operations',
    tags=['Operations page']
)


@router.get('/search', response_model=None)
def get_search_page(request: Request, current_user=Depends(current_user)):
    return templates.TemplateResponse('search.html',
                                      {'request': request, 'current_user': current_user})


@router.get('/search/{operation_type}')
def get_search_page(request: Request, operations=Depends(get_specific_operations),
                    current_user=Depends(current_user)):
    return templates.TemplateResponse('search.html',
                                      {'request': request, 'operations': operations['body'],
                                       'current_user': current_user})

@router.get('/send_report')
def get_report_email_page(request: Request, current_user=Depends(current_user)):
    return templates.TemplateResponse('reports_email.html',
                                      {'request': request, 'current_user': current_user})
