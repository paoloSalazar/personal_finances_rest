from fastapi import APIRouter
from model.schemas.category import CategoryBase, CategoryRead, CategoryCreate
import service.category as service

router = APIRouter(prefix="/api/categories")

@router.get("/")
def get_all() -> list[CategoryBase]:
    """Get all categories"""
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> CategoryRead | None:
    """Get one category by name"""
    return service.get_one(name)

@router.post("/")
def create(category: CategoryCreate) -> CategoryCreate | None:
    """Create a new category (not implemented)"""
    # TODO: implement creation logic
    return service.create(category)

@router.patch("/")
def modify(category: CategoryBase) -> CategoryBase | None:
    """Modify fields of an existing category (not implemented)"""
    # TODO: implement partial update
    return service.modify(category)

@router.put("/")
def replace(category: CategoryBase) -> CategoryBase | None:
    """Replace an existing category (not implemented)"""
    # TODO: implement full replace
    return service.replace(category)

@router.delete("/{name}")
def delete(name: str) -> None:
    """Delete a category (not implemented)"""
    # TODO: implement deletion
    return service.delete(name)
