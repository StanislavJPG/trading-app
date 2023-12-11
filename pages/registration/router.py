from fastapi import APIRouter, Request

from app.pages.base.router import templates

router = APIRouter(
    tags=['Registration page']
)


@router.get('/registration')
def registration_user(request: Request):
    return templates.TemplateResponse(
        'registration.html',
        context={
            'request': request
        }
    )
