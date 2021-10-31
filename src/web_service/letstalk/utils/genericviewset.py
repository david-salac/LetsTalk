from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from fastapi_utils.cbv import cbv

if TYPE_CHECKING:
    from fastapi_utils.inferring_router import InferringRouter


def create_generic_viewset(router: 'InferringRouter',
                           sqlalchemy_model: type,
                           pydantic_model: type,
                           pydantic_modify_model: type,
                           db_session: object,
                           route_base: str) -> type:
    """Create a generic view set with all standard methods.
    Note:
        Would be better to use meta classes for this purpose.
    """
    @cbv(router)
    class _GenericAPIViewSet:
        """Base Generic API view set (implementing all CRUD)"""
        @router.get(route_base,
                    response_model=list[pydantic_model])
        def list_item(self):
            """List all items in the database"""
            return sqlalchemy_model.all(db_session)

        @router.get(route_base + "/{item_id}",
                    response_model=pydantic_model)
        def detail_item(self, item_id: int):
            """Detail of the item in the database"""
            try:
                return sqlalchemy_model.get(db_session, id=item_id)
            except AttributeError:  # Covers everything
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Item not found"
                )

        @router.post(route_base,
                     response_model=pydantic_model,
                     status_code=status.HTTP_201_CREATED)
        def create_item(self, item: pydantic_modify_model):
            """Create an item in the database"""
            return sqlalchemy_model(**item.dict()).create(db_session)

        @router.put(route_base + "/{item_id}",
                    response_model=pydantic_model)
        def update_item(self,
                        item_id: int,
                        item: pydantic_modify_model):
            """Update the item in the database"""
            resp_body, count = sqlalchemy_model.update(
                db_session, {"id": item_id}, item.dict()
            )
            if count != 1:
                # In the case of wrong ID
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Item not found")
            return resp_body

        @router.delete(route_base + "/{item_id}",
                       status_code=status.HTTP_204_NO_CONTENT)
        def delete_item(self, item_id: int):
            """Delete the item in the database"""
            count = sqlalchemy_model.delete(db_session,
                                            {"id": item_id})
            if count != 1:
                # In the case of wrong ID
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Item not found")

    return _GenericAPIViewSet
