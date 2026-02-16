"""CRUD-операции для рецептов."""

from app.crud.recipe import (
    create_recipe as create_recipe,
)
from app.crud.recipe import (
    delete_recipe as delete_recipe,
)
from app.crud.recipe import (
    get_recipe as get_recipe,
)
from app.crud.recipe import (
    list_recipes as list_recipes,
)
from app.crud.recipe import (
    update_recipe as update_recipe,
)

__all__ = [
    "create_recipe",
    "delete_recipe",
    "get_recipe",
    "list_recipes",
    "update_recipe",
]
