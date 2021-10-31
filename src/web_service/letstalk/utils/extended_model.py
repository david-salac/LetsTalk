from typing import TYPE_CHECKING, ParamSpecKwargs, Any
import logging

from sqlalchemy import inspect

if TYPE_CHECKING:
    from sqlalchemy.orm.session import Session

LOGGER = logging.getLogger(__name__)


class ExtendedModelMixin:
    """Extension of SQLAlchemy model. Allows serialization, CRUD
    operations and others.
    """

    def to_dict(self) -> dict[str, Any]:
        """Serialize database row as dictionary.

        Returns:
            dict[str, Any]: Dictionary object representation.
        """
        return {
            _name: getattr(self, _name) for _name in vars(self)
            if not _name.startswith("_")
        }

    @classmethod
    def all(cls,
            db_session: 'Session',
            order_by: object = None) -> list[dict[str, Any]]:
        """Select all object in the model

        Args:
            db_session (Session): Database connector.
            order_by (object): Order by statement (if defined),
                by default orders by the first column of PK.

        Returns:
            list[dict[str, Any]]: List of all rows serialized as dict
        """
        # Execute selection
        if order_by:
            # If there is a custom order by statement
            results = db_session.query(cls).order_by(order_by)
        else:
            # Default order is by the first column of PK
            results = db_session.query(cls).order_by(
                inspect(cls).primary_key[0]
            )
        # Return results
        return [_item.to_dict() for _item in results.all()]

    @classmethod
    def get(cls,
            db_session: 'Session',
            **filtration: dict | ParamSpecKwargs) -> dict[str, Any]:
        """Select all object in the model.

        Args:
            db_session (Session): Database connector.
            **filtration (dict): parameters for filtration
        Returns:
            dict[str, Any]: Specific row serialized as dictionary.
        """
        # Execute selection
        results = db_session.query(cls).filter_by(**filtration)
        # Get results
        fetch_res = [_item.to_dict() for _item in results.all()]
        if len(fetch_res) == 1:
            return fetch_res[0]
        elif len(fetch_res) > 1:
            raise AttributeError("more than one plausible item")
        else:
            raise AttributeError("item is not in system")

    @classmethod
    def filter(cls,
               db_session: 'Session',
               **filtration: dict | ParamSpecKwargs) -> list[dict]:
        """Select all object in the model

        Args:
            db_session (Session): Database connector.
            filtration (dict | ParamSpecKwargs): Conditions
                for selection.
        """
        # Execute selection
        results = db_session.query(cls).filter_by(**filtration)
        # Get results
        return [_item.to_dict() for _item in results.all()]

    def create(self, db_session) -> dict[str, Any]:
        """Insert into the database

        Args:
            db_session (Session): Database connector.

        Returns:
            dict[str, Any]: Inserted values.
        """
        # Perform creation
        db_session.add(self)
        db_session.commit()

        # Force to fetch the ID of the new object
        for pk in inspect(type(self)).primary_key:
            # Fetches it by calling the property
            getattr(self, pk.name)

        # Return identity (with new ID)
        return self.to_dict()

    @classmethod
    def update(cls,
               db_session,
               filtration: dict | ParamSpecKwargs,
               new_values: dict) -> tuple[dict[str, Any], int]:
        """Update in the database

        Args:
            db_session (Session): Database connector.
            filtration (dict | ParamSpecKwargs): Conditions
                for selection.
            new_values (dict): Values that are updated.

        Returns:
            tuple[dict[str, Any], int]: New values, number of
                updated items.
        """
        # Perform database update
        selection = db_session.query(cls).filter_by(**filtration)
        selection.update(new_values)
        db_session.commit()

        # Return updated item
        return filtration | new_values, int(selection.count())

    @classmethod
    def delete(cls,
               db_session,
               filtration: dict | ParamSpecKwargs) -> int:
        """Delete rows in the database

        Args:
            db_session (Session): Database connector.
            filtration (dict | ParamSpecKwargs): Conditions
                for selection.

        Returns:
            int: number of deleted items.
        """
        # Perform database update
        selection = db_session.query(cls).filter_by(**filtration)
        affected = int(selection.count())
        selection.delete()
        db_session.commit()

        # Return updated item
        return affected
