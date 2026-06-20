from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.repositories.category_repository import CategoryRepository
from app.services.auth_dependency import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return CategoryRepository(db).get_all()

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    repo = CategoryRepository(db)
    if repo.get_by_name(data.name):
        raise HTTPException(status_code=400, detail="Category already exists")
    return repo.create(data)

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: UUID, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    repo = CategoryRepository(db)
    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    repo.delete(category)