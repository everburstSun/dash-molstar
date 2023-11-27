from typing import List
import dash_mantine_components as dmc
from .base import Placeholder, get_on_change

index = 1

SELECT_PREFIX = "select_prefix"


def select_with_on_change(
    label: str = "",
    placeholder: str = "",
    options: List[dict] = [],
    multiple: bool = False,
    style: dict = {},
    id: str = "",
):
    global index

    def get_select(default="", **kwargs):
        current_label = kwargs.pop("label", label)
        current_placeholder = kwargs.pop("placeholder", placeholder)
        current_default = kwargs.pop("default", default)
        current_options = kwargs.pop("options", options)
        current_multiple = kwargs.pop("multiple", multiple)
        current_style = kwargs.pop("style", style)
        return (
            dmc.Select(
                label=current_label,
                placeholder=current_placeholder,
                value=current_default,
                data=current_options,
                selectOnBlur=False,
                style=current_style,
                **kwargs,
            )
            if not current_multiple
            else dmc.MultiSelect(
                label=current_label,
                placeholder=current_placeholder,
                value=current_default,
                data=current_options,
                selectOnBlur=False,
                styles={
                    "item": {
                        ":hover": {
                            "background-color": "#ab9fbc",
                            "color": "#fff",
                        },
                    },
                },
                **kwargs,
            )
        )

    select_placeholder = Placeholder.create(
        get_select, id=id or f"{SELECT_PREFIX}_{index}"
    )

    if not id:
        index += 1

    return select_placeholder, get_on_change(select_placeholder.get_id())
