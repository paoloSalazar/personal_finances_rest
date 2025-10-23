from fastapi import APIRouter
from model.category import Category
import service.category as service

router = APIRouter(prefix="/api/categories")

@router.get("/")
def get_all() -> list[Category]:
    """Get all categories"""
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> Category | None:
    """Get one category by name"""
    return service.get_one(name)

@router.post("/")
def create(category: Category) -> Category | None:
    """Create a new category (not implemented)"""
    # TODO: implement creation logic
    return service.create(category)

@router.patch("/")
def modify(category: Category) -> Category | None:
    """Modify fields of an existing category (not implemented)"""
    # TODO: implement partial update
    return service.modify(category)

@router.put("/")
def replace(category: Category) -> Category | None:
    """Replace an existing category (not implemented)"""
    # TODO: implement full replace
    return service.replace(category)

@router.delete("/{name}")
def delete(name: str) -> None:
    """Delete a category (not implemented)"""
    # TODO: implement deletion
    return service.delete(name)
