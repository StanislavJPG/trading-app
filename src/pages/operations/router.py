from fastapi import APIRouter, Request, Depends

from src.pages.base.router import templates
from src.auth.base_config import current_user
from src.operations.router import get_specific_operations


router = APIRouter(
    prefix='/operations',
    tags=['Operations page']
)


@router.get('/search')
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


@router.get('/buy')
def get_add_operations_page(request: Request, current_user=Depends(current_user)):
    return templates.TemplateResponse('operations_create.html',
                                      {'request': request, 'current_user': current_user})
