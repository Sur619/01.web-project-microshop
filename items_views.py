from typing import Annotated

from fastapi import Path, APIRouter

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def hello():
    return [{"item_id": 1, "name": "Item 1"}, {"item_id": 2, "name": "Item 2"}]


@router.get("/{item_id}/")
def get_item_by_id(item_id: Annotated[int, Path(ge=1)]):
    return {"item_id": item_id}
