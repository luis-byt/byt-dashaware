from typing import Any, Callable, Dict, Optional, Tuple, Union

from django.contrib.admin.widgets import (
    AdminTextInputWidget,
)
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms import (
    CheckboxInput,
    MultiWidget,
    NullBooleanSelect,
    NumberInput,
    Select,
)
from django.utils.translation import gettext_lazy as _


BASE_CLASSES = [
    "border",
    "bg-white",
    "font-medium",
    "rounded-md",
    "shadow-sm",
    "text-gray-500",
    "text-sm",
    "focus:ring",
    "focus:ring-primary-300",
    "focus:border-primary-600",
    "focus:outline-none",
    "group-[.errors]:border-red-600",
    "group-[.errors]:focus:ring-red-200",
    "dark:bg-gray-900",
    "dark:border-gray-700",
    "dark:text-gray-400",
    "dark:focus:border-primary-600",
    "dark:focus:ring-primary-700",
    "dark:focus:ring-opacity-50",
    "dark:group-[.errors]:border-red-500",
    "dark:group-[.errors]:focus:ring-red-600/40",
]

BASE_INPUT_CLASSES = [
    *BASE_CLASSES,
    "px-3",
    "py-2",
    "w-full",
]

INPUT_CLASSES = [*BASE_INPUT_CLASSES, "max-w-2xl"]

SELECT_CLASSES = [
    *BASE_INPUT_CLASSES,
    "pr-8",
    "max-w-2xl",
    "appearance-none",
]


class UnfoldAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(attrs={"class": " ".join(INPUT_CLASSES), **(attrs or {})})


class UnfoldAdminSelectWidget(Select):
    def __init__(self, attrs=None, choices=()):
        if attrs is None:
            attrs = {}

        attrs["class"] = " ".join(SELECT_CLASSES)
        super().__init__(attrs, choices)
