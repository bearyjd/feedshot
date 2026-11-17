import inspect

import pytest

from fastfoto_linux.gui.modes import WorkerPort

# Every worker method the controller and its sides call through ``controller._worker``.
USED_METHODS = (
    "check",
    "scan",
    "scan_documents",
    "process_kept",
    "cancel",
    "photo_edit_job",
    "analyse_folder",
    "write_draft",
    "preview_page",
    "estimate_page",
)


@pytest.mark.parametrize("name", USED_METHODS)
def test_worker_port_declares_method_the_components_call(name: str) -> None:
    assert callable(getattr(WorkerPort, name, None))


def test_worker_port_declares_busy() -> None:
    assert isinstance(inspect.getattr_static(WorkerPort, "busy"), property)
