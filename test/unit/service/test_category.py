from model.category import Category
from service import category as code

sample = Category(id=1, name="Food", description="Expenses for food and groceries")

def test_get_all():
    result = code.get_all()
    assert isinstance(result, list)

def test_create():
    result = code.create(sample)
    assert result == sample

