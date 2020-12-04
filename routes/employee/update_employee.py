from fastapi import APIRouter

employee_router = APIRouter()

employee_router.post('/update/employee/{username}')
