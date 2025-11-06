import logging
from fastapi import APIRouter, HTTPException, Depends
from model.schemas.category import CategoryBase, CategoryRead, CategoryCreate
import service.category as service
import sqlite3
from service.user import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/categories")

@router.get("/")
def get_all() -> list[CategoryBase]:
    """Get all categories"""
    logger.info("Fetching all categories")
    result = service.get_all()
    logger.info(f"Retrieved {len(result)} categories")
    return result

@router.get("/{name}")
def get_one(name: str) -> CategoryRead | None:
    """Get one category by name"""
    logger.info(f"Fetching category with name: {name}")
    result = service.get_one(name)
    if result:
        logger.info(f"Found category: {result.name}")
    else:
        logger.warning(f"Category not found: {name}")
    return result

@router.post("/")
def create(category: CategoryCreate, current_user: dict = Depends(get_current_user)) -> CategoryRead:
    """Create a new category"""
    logger.info(f"Creating category: {category.name}")
    try:
        result = service.create(category)
        logger.info(f"Successfully created category: {result.name} with id: {result.id}")
        return result
    except sqlite3.IntegrityError as e:
        logger.error(f"Failed to create category {category.name}: {str(e)}")
        if "UNIQUE constraint failed: categories.name" in str(e):
            raise HTTPException(status_code=400, detail="Category with this name already exists")
        else:
            raise HTTPException(status_code=500, detail="Database error occurred")
            

@router.patch("/")
def modify(category: CategoryBase, current_user: dict = Depends(get_current_user)) -> CategoryBase | None:
    """Modify fields of an existing category (not implemented)"""
    # TODO: implement partial update
    return service.modify(category)

@router.put("/")
def replace(category: CategoryBase, current_user: dict = Depends(get_current_user)) -> CategoryBase | None:
    """Replace an existing category (not implemented)"""
    # TODO: implement full replace
    return service.replace(category)

@router.delete("/{name}")
def delete(name: str, current_user: dict = Depends(get_current_user)) -> None:
    """Delete a category (not implemented)"""
    # TODO: implement deletion
    return service.delete(name)
