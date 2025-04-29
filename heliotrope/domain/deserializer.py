from datetime import date, datetime
from typing import Any, Mapping, Self, Union, get_args, get_origin, get_type_hints


class Deserializer:
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        converted_data: dict[str, Any] = {}
        type_hints = get_type_hints(cls)

        for key, value in data.items():
            type_ = type_hints.get(key)

            if type_ is None:
                raise ValueError(f"Key {key} not found in {cls.__name__}")

            if type_ is datetime:
                value = datetime.fromisoformat(value).replace(tzinfo=None)
            # Union type
            elif origin_type := get_origin(type_):
                # Optional type
                if origin_type is Union and type(None) in get_args(type_):
                    if value is not None:
                        arg_type = get_args(type_)[0]
                        if arg_type is date:
                            value = date.fromisoformat(value)
                        else:
                            value = arg_type(value)
                elif origin_type is list:
                    arg_type = get_args(type_)[0]
                    if issubclass(arg_type, Deserializer):
                        if value is None:
                            value = []
                        else:
                            value = [arg_type.from_dict(v) for v in value]
                    elif arg_type is int:
                        value = [int(v) for v in value]
            elif issubclass(type_, Deserializer):
                value = type_.from_dict(value)
            elif type_ is bool:
                if value in ["0", 0, None, ""]:
                    value = False
                if value in ["1", 1]:
                    value = True
            else:
                value = type_(value)
            converted_data[key] = value
        return cls(**converted_data)
