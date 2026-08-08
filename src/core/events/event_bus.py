"""
AEGIS

Broker Event Bus

A lightweight publish/subscribe event system used by all
core engines.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventBus:
    """
    Publish / Subscribe event bus.
    """

    def __init__(self) -> None:

        self._listeners: dict[
            str,
            list[Callable[..., Any]],
        ] = defaultdict(list)

    # =====================================================
    # Subscribe
    # =====================================================

    def subscribe(
        self,
        event: str,
        callback: Callable[..., Any],
    ) -> None:

        if callback not in self._listeners[event]:

            self._listeners[event].append(callback)

    # =====================================================
    # Unsubscribe
    # =====================================================

    def unsubscribe(
        self,
        event: str,
        callback: Callable[..., Any],
    ) -> None:

        if callback in self._listeners[event]:

            self._listeners[event].remove(callback)

    # =====================================================
    # Publish
    # =====================================================

    def publish(
        self,
        event: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:

        for callback in list(
            self._listeners[event]
        ):

            callback(
                *args,
                **kwargs,
            )

    # =====================================================
    # Utility
    # =====================================================

    def clear(self) -> None:

        self._listeners.clear()

    def listener_count(
        self,
        event: str,
    ) -> int:

        return len(
            self._listeners[event]
        )
