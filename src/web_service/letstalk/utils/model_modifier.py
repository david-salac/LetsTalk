from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel


def skip_fields_in_pydantic_model(
        base_model: type['BaseModel'],
        new_model_name: str,
        skip_fields: set[str]
) -> type['BaseModel']:
    """Create serializer (Pydantic model) and skips specific fields.

    Args:
        base_model (type['BaseModel']): Pydantic model
        new_model_name (str): Name of new class
        skip_fields (set[str]): Which fields are skipped (names)

    Returns:
        type['BaseModel']: Pydantic serializer.
    """
    # Create a deep copy of serializer class dictionary
    new_dict = {_k: _v for _k, _v in base_model.__dict__.items()}
    new_dict['__fields__'] = {
        _k: _v for _k, _v in base_model.__fields__.items()
        if _k not in skip_fields
    }
    # Return new type
    return type(new_model_name,
                base_model.__bases__,
                new_dict)


def skip_primary_keys_in_model(
        base_model: type['BaseModel'],
        new_model_name: str,
        pk_fields_names: set[str] = ("id", )
) -> type['BaseModel']:
    """Create serializer (Pydantic model) and skips primary keys.

    Args:
        base_model (type['BaseModel']): Pydantic model
        new_model_name (str): Name of new class
        pk_fields_names (set[str]): Name of primary key fields

    Returns:
        type['BaseModel']: Pydantic serializer.
    """
    return skip_fields_in_pydantic_model(
        base_model,
        new_model_name,
        set(pk_fields_names)
    )
