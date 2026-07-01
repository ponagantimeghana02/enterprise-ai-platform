from fastapi import APIRouter, Depends
from backend.database.db import User
from backend.authentication.auth import get_current_user

router = APIRouter(tags=["HR and Finance Mock Endpoints"])

@router.get("/hr/leave-policies")
def get_leave_policies(current_user: User = Depends(get_current_user)):
    return {"message": "Success: You have accessed Leave Policies", "user": current_user.email}

@router.get("/hr/onboarding")
def get_onboarding(current_user: User = Depends(get_current_user)):
    return {"message": "Success: You have accessed Onboarding", "user": current_user.email}

@router.get("/hr/hr-documents")
def get_hr_documents(current_user: User = Depends(get_current_user)):
    return {"message": "Success: You have accessed HR Documents", "user": current_user.email}

@router.get("/payroll")
def get_payroll(current_user: User = Depends(get_current_user)):
    return {"message": "Success: You have accessed Payroll module", "user": current_user.email}

@router.get("/finance")
def get_finance(current_user: User = Depends(get_current_user)):
    return {"message": "Success: You have accessed Finance module", "user": current_user.email}
