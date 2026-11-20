"""The public Controller methods the review side uses instead of writing its internals."""

import re
from pathlib import Path

from fastfoto_linux import gui
from fastfoto_linux.gui.controller import Controller
from fastfoto_linux.gui.form import ScanForm
from fastfoto_linux.gui.report import Banner
from fastfoto_linux.gui.state import State
from fastfoto_linux.session import DocumentSessionResult
from tests.gui.helpers import FakeWorker


def make() -> tuple[Controller, FakeWorker, list[int]]:
    worker, calls = FakeWorker(), []
    controller = Controller(worker, ScanForm(), on_change=lambda: calls.append(1))
    return controller, worker, calls


def test_exposes_worker_and_documents_side() -> None:
    controller, worker, _ = make()
    assert controller.worker is worker
    assert controller.docs is controller._docs


def test_set_banner_sets_without_notifying() -> None:
    controller, _, calls = make()
    banner = Banner("error", "x")
    controller.set_banner(banner)
    assert controller.banner is banner
    assert calls == []


def test_set_result_stores_result() -> None:
    controller, _, _ = make()
    result = DocumentSessionResult.__new__(DocumentSessionResult)
    controller.set_result(result)
    assert controller._result is result


def test_move_to_changes_state_and_banner_then_notifies() -> None:
    controller, _, calls = make()
    controller.move_to(State.CHECKING)
    assert controller.state is State.CHECKING
    assert controller.banner is None
    assert calls == [1]


def test_notify_fires_the_listeners() -> None:
    controller, _, calls = make()
    controller.notify()
    assert calls == [1]


def test_components_do_not_reach_into_controller_internals() -> None:
    root = Path(gui.__file__).parent
    pattern = re.compile(r"\b(?:_controller|controller|c)\._\w")
    offenders = [
        f"{path.relative_to(root)}:{n}: {line.strip()}"
        for path in root.rglob("*.py")
        if path.name != "controller.py"
        for n, line in enumerate(path.read_text().splitlines(), 1)
        if pattern.search(line)
    ]
    assert offenders == []
