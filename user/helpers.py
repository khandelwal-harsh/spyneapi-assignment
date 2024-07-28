from dataclasses import asdict, dataclass, is_dataclass

from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

from django.db import models
from django.utils import timezone

# Generic type for a Django model
# Reference: https://mypy.readthedocs.io/en/stable/kinds_of_types.html#the-type-of-class-objects
DjangoModelType = TypeVar("DjangoModelType", bound=models.Model)

def model_update(
    *,
    instance: DjangoModelType,
    fields: List[str],
    data: Union[Dict[str, Any], dataclass],
    save: bool = True,
    clean: bool = True,
) -> Tuple[DjangoModelType, bool, list[str]]:
    """
    Generic update service meant to be reused in local update services
    For example:
    def user_update(*, user: User, data) -> User:
        fields = ['first_name', 'last_name']
        user, is_updated, updated_fields = model_update(instance=user, fields=fields, data=data)
        // Do other actions with the user here
        return user
    Return value: Tuple with the following elements:
        1. The instance we updated
        2. A boolean value representing whether we performed an update or not.
        3. A list of updated fields
    """
    if is_dataclass(data):
        data = asdict(data)

    updated_fields = []
    for field in fields:
        # Skip if a field is not present in the actual data
        if field not in data:
            continue

        if getattr(instance, field) != data[field]:
            # TODO: handle file field case, also check file replace
            #  also decide whether to updated file using this or not?
            updated_fields.append(field)
            setattr(instance, field, data[field])

    # Perform an update only if any of the fields was actually changed
    if len(updated_fields):
        if clean:
            instance.full_clean()
        # Update only the fields that are meant to be updated.
        # Django docs reference:
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#specifying-which-fields-to-save
        if save:
            instance.save(update_fields=updated_fields)
        return instance, True, updated_fields

    return instance, False, updated_fields