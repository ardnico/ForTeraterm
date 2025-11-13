from __future__ import annotations

import pytest

from ForTeraterm.view_manager import ViewManager


class DummyFrame:
    def __init__(self) -> None:
        self.destroyed = False

    def destroy(self) -> None:
        self.destroyed = True


class DummyParent:
    pass


def test_show_raises_without_parent() -> None:
    manager: ViewManager[DummyParent, DummyFrame] = ViewManager()

    with pytest.raises(RuntimeError):
        manager.show(lambda parent: DummyFrame())


def test_reset_destroys_frames() -> None:
    manager: ViewManager[DummyParent, DummyFrame] = ViewManager()
    parent = DummyParent()
    manager.set_parent(parent)

    frames = []

    def factory(received_parent: DummyParent) -> DummyFrame:
        assert received_parent is parent
        frame = DummyFrame()
        frames.append(frame)
        return frame

    manager.show(factory)
    (frame,) = frames
    assert frame.destroyed is False

    manager.reset()
    assert frame.destroyed is True
