import logging
from model.schemas.category import CategoryBase, CategoryCreate, CategoryRead
import data.category as data

logger = logging.getLogger(__name__)

def get_all() -> list[CategoryRead]:
    """return all categories"""
    logger.debug("Service: Fetching all categories")
    result = data.get_all()
    logger.debug(f"Service: Retrieved {len(result)} categories")
    return result

def get_one(name: str) -> CategoryRead | None:
    """return one category by name"""
    logger.debug(f"Service: Fetching category by name: {name}")
    result = data.get_one(name)
    if result:
        logger.debug(f"Service: Found category: {result.name}")
    else:
        logger.debug(f"Service: Category not found: {name}")
    return result


## Non functional methods

def create(category: CategoryCreate) -> CategoryRead:
    logger.info(f"Service: Creating category: {category.name}")
    result = data.create(category)
    logger.info(f"Service: Created category: {result.name} with id: {result.id}")
    return result

def modify(category: CategoryBase) -> CategoryRead:
    return data.modify(category)

def replace(category: CategoryBase) -> CategoryRead:
    return data.replace(category)

def delete(name: str) -> bool:
    return data.delete(name)