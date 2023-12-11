from fastapi import APIRouter, Request, Depends

from src.pages.base.router import templates
from src.auth.base_config import current_user

router = APIRouter(
    tags=['Authorization page']
)


@router.get('/authorization')
def get_auth_page(request: Request):
    return templates.TemplateResponse(
        'authorization.html',
        context={
            'request': request
        }
    )


@router.get("/index", response_model=None)
def logout_page(
    request: Request, current_user=Depends(current_user)):

    return templates.TemplateResponse("logout.html", context={"request": request, "current_user": current_user})


# router.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["Auth"],
# )
#
# router.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["Auth"],
# )