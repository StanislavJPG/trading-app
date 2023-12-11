import re

import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.operations.models import Operations
from app.src.operations.schemas import OperationCreate
from app.src.database import get_async_session

router = APIRouter(
    prefix='/operations',
    tags=['Operations']
)


@router.get('')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operations).where(Operations.type == operation_type).limit(10)
        result = await session.scalars(query)
        return {
            'status': 'success',
            'body': result.all()
        }
    except Exception:
        raise HTTPException(status_code=500,
                            detail={'status': 'Error',
                                    'body': 'Please, tell us about this error.'})


@router.post('')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        statement = insert(Operations).values(**new_operation.model_dump())
        await session.execute(statement)
        await session.commit()
        return {'status': 'success',
                'body': new_operation}
    except sqlalchemy.exc.IntegrityError:
        matches = re.findall(r'id=(\d*)', str(new_operation))
        raise HTTPException(status_code=500,
                            detail={'status': 'Error',
                                    'body': f'id {matches[0]} already exists'})

