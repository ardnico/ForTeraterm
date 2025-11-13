"""Helpers for managing dynamic content frames in the main window."""

from __future__ import annotations

from typing import Callable, Generic, List, Protocol, TypeVar


class SupportsDestroy(Protocol):
    """Protocol for widgets that can be destroyed."""

    def destroy(self) -> None:  # pragma: no cover - interface definition
        """Remove the widget from the UI."""


ParentT = TypeVar("ParentT")
FrameT = TypeVar("FrameT", bound=SupportsDestroy)
FrameFactory = Callable[[ParentT], FrameT]


class ViewManager(Generic[ParentT, FrameT]):
    """Maintain the currently displayed frame and clean up stale ones."""

    def __init__(self) -> None:
        self._parent: ParentT | None = None
        self._frames: List[FrameT] = []

    def set_parent(self, parent: ParentT) -> None:
        """Register the container that future frames will use."""

        self._parent = parent

    def require_parent(self) -> ParentT:
        """Return the registered parent or raise an informative error."""

        if self._parent is None:
            raise RuntimeError("Content frame has not been initialised.")
        return self._parent

    def show(self, factory: FrameFactory) -> FrameT:
        """Create and track a new frame using *factory*."""

        parent = self.require_parent()
        frame = factory(parent)
        self._frames.append(frame)
        return frame

    def reset(self) -> None:
        """Destroy all tracked frames and clear the internal state."""

        for frame in self._frames:
            frame.destroy()
        self._frames.clear()


__all__ = ["ViewManager", "FrameFactory", "SupportsDestroy"]
