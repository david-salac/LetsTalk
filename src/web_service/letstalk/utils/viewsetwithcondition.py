from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from fastapi_utils.cbv import cbv


from .genericviewset import create_generic_viewset
from ..models import Condition


def viewset_with_condition_detail(
        router: 'InferringRouter',
        sqlalchemy_model: type,
        pydantic_model: type,
        pydantic_modify_model: type,
        pydantic_nested_model: type,
        db_session: object,
        route_base: str) -> type:
    """Special viewset that returns details of condition
    Note:
        Would be better to use meta classes for this purpose.
    """

    @cbv(router)
    class _SpecialAPIViewSet(
        create_generic_viewset(router,
                               sqlalchemy_model,
                               pydantic_model,
                               pydantic_modify_model,
                               db_session,
                               route_base)
    ):
        @router.get(
            route_base + "-with-condition",
            response_model=list[pydantic_nested_model]
        )
        def list_item_with_condition(self):
            """List all items in the database and return a list of
            nested structures with condition as a nested field
            """
            # TODO: This should be rewritten using JOIN statement
            list_of_items = sqlalchemy_model.all(db_session)
            for item in list_of_items:
                condition_id = item.pop('condition_id')
                condition = Condition.get(db_session,
                                          id=condition_id)
                item['condition'] = condition
            return list_of_items

        @router.post(route_base + "-with-condition",
                     response_model=pydantic_nested_model,
                     status_code=status.HTTP_201_CREATED)
        def create_item_condition(
                self,
                item: pydantic_modify_model
        ):
            """Create an item in the database and return
            nested structure with condition as a nested field
            """
            new_item = sqlalchemy_model(**item.dict()).create(
                db_session
            )
            # Populate condition ID
            condition_id = new_item.pop('condition_id')
            # Create condition dict
            condition = Condition.get(db_session,
                                      id=condition_id)
            new_item['condition'] = condition

            return new_item

        @router.put(route_base + "-with-condition",
                    response_model=pydantic_nested_model,
                    status_code=status.HTTP_200_OK)
        def update_item_condition(
                self,
                item: pydantic_model
        ):
            """Update the item in the database and return
            nested structure with condition as a nested field
            """
            request = item.dict()
            resp_body, count = sqlalchemy_model.update(
                db_session, {"id": request['id']}, request
            )
            if count != 1:
                # In the case of wrong ID
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Item not found")
            # Populate condition ID
            condition_id = resp_body.pop('condition_id')
            # Create condition dict
            condition = Condition.get(db_session,
                                      id=condition_id)
            resp_body['condition'] = condition
            return resp_body

    return _SpecialAPIViewSet
