from typing import Optional, Callable, Any, Union, List
from dash.development.base_component import Component
from dash import Output, html, Input, callback, State

import random
import string


def get_random_str(len: int = 10):
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(len)
    )



class Placeholder:
    class _Placeholder:
        _ele: Component
        _ele_id: str
        _custom_ele_args: List[Any] = []
        _custom_ele_kwargs: dict = {}

        def __init__(
            self,
            ele: Union[Callable[[Any], Component], Component] = None,
            id: str = None,
            style: dict = {},
        ) -> None:
            _id = get_random_str()
            if (
                ele is not None
                and isinstance(ele, Component)
                and (not hasattr(ele, "id"))
            ):
                ele.id = id or _id

            self._ele = (
                ele
                if isinstance(ele, Component) or callable(ele)
                else html.Div(id=id or _id, style=style)
            )
            self._ele_id = id or _id

        def get_id(self):
            return self._ele_id

        def get_element(self, *args, **kwargs):
            _args = args or []
            if callable(self._ele):
                self._custom_ele_args = _args or []
                self._custom_ele_kwargs = kwargs or {}
                current_ele = self._ele(*_args, **kwargs)
                if current_ele is not None and isinstance(current_ele, Component):
                    current_ele.id = self._ele_id
                return current_ele
            else:
                return self._ele

        def get_output(self, **kwargs):
            property = kwargs.pop("component_property", "children")
            return Output(
                component_id=self._ele_id,
                component_property=property,
                **kwargs,
            )

        def get_state(self, **kwargs):
            component_property = kwargs.pop("component_property", "data")
            return State(
                component_id=self._ele_id,
                component_property=component_property,
                **kwargs,
            )

        def get_input(self, **kwargs):
            property = kwargs.pop("component_property", "children")
            return Input(
                component_id=self._ele_id,
                component_property=property,
                **kwargs,
            )

    @classmethod
    def create(
        cls, ele: Union[Callable[[Any], Component], Component] = None, id: str = None
    ):
        return cls._Placeholder(ele, id)


def get_on_change(
    id: str,
    args_mutating: Optional[Callable] = None,
    component_property: Union[str, List[str]] = "value",
):
    def on_change(output, *args, **kwargs):
        _args = args or []

        inputs = (
            [
                Input(
                    component_id=id,
                    component_property=item,
                )
                for item in component_property
            ]
            if type(component_property) == list
            else Input(
                component_id=id,
                component_property=component_property,
            )
        )

        def decorator(func):
            @callback(
                output,
                inputs,
                *_args,
                **kwargs,
            )
            def wrapper(*args2, **kwargs2):
                current_args = args2
                current_kwargs = kwargs2
                if callable(args_mutating):
                    current_args, current_kwargs = args_mutating(*args2, **kwargs2)
                return func(*current_args, **current_kwargs)

            return wrapper

        return decorator

    return on_change
