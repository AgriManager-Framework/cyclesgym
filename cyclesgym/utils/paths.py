import os
import pathlib

__all__ = [
    'PROJECT_PATH',
    'BASE_PROJECT_PATH',
    'CYCLES_PATH',
    'BASE_CYCLES_PATH',
    'CYCLES_RUNTIME_PATH',
    'CYCLES_INPUT_PATH',
    'CYCLES_OUTPUT_PATH',
    'AGENTS_PATH',
    'FIGURES_PATH',
    'DATA_PATH',
]

DEFAULT_PROJECT_PATH = pathlib.Path(__file__).parents[2].resolve()
BASE_PROJECT_PATH = DEFAULT_PROJECT_PATH
PROJECT_PATH = pathlib.Path(
    os.environ.get("CYCLESGYM_PROJECT_PATH", DEFAULT_PROJECT_PATH)
).resolve()

# Base immutable Cycles assets live with the installed repo unless explicitly overridden.
BASE_CYCLES_PATH = pathlib.Path(
    os.environ.get("CYCLESGYM_BASE_CYCLES_PATH", DEFAULT_PROJECT_PATH.joinpath("cycles"))
).resolve()

# Runtime I/O can be redirected elsewhere to avoid filling home quota.
CYCLES_RUNTIME_PATH = pathlib.Path(
    os.environ.get("CYCLESGYM_RUNTIME_CYCLES_PATH", BASE_CYCLES_PATH)
).resolve()
CYCLES_PATH = CYCLES_RUNTIME_PATH
CYCLES_INPUT_PATH = pathlib.Path(
    os.environ.get("CYCLESGYM_INPUT_PATH", CYCLES_RUNTIME_PATH.joinpath("input"))
).resolve()
CYCLES_OUTPUT_PATH = pathlib.Path(
    os.environ.get("CYCLESGYM_OUTPUT_PATH", CYCLES_RUNTIME_PATH.joinpath("output"))
).resolve()

AGENTS_PATH = pathlib.Path(
    os.environ.get("CYCLESGYM_AGENTS_PATH", PROJECT_PATH.joinpath("agents"))
).resolve()
FIGURES_PATH = pathlib.Path(
    os.environ.get("CYCLESGYM_FIGURES_PATH", PROJECT_PATH.joinpath("figures"))
).resolve()
DATA_PATH = pathlib.Path(
    os.environ.get("CYCLESGYM_DATA_PATH", PROJECT_PATH.joinpath("data"))
).resolve()
TEST_PATH = PROJECT_PATH.joinpath('cyclesgym', 'tests')

CYCLES_PATH.mkdir(exist_ok=True, parents=True)
CYCLES_INPUT_PATH.mkdir(exist_ok=True, parents=True)
CYCLES_OUTPUT_PATH.mkdir(exist_ok=True, parents=True)
AGENTS_PATH.mkdir(exist_ok=True, parents=True)
FIGURES_PATH.mkdir(exist_ok=True, parents=True)
DATA_PATH.mkdir(exist_ok=True, parents=True)


def _symlink_if_missing(src: pathlib.Path, dest: pathlib.Path) -> None:
    if dest.exists() or dest.is_symlink():
        return
    dest.symlink_to(src)


def _bootstrap_runtime_cycles_tree() -> None:
    if CYCLES_PATH == BASE_CYCLES_PATH:
        return

    base_binary = BASE_CYCLES_PATH.joinpath("Cycles")
    runtime_binary = CYCLES_PATH.joinpath("Cycles")
    if base_binary.exists():
        _symlink_if_missing(base_binary, runtime_binary)

    base_input_dir = BASE_CYCLES_PATH.joinpath("input")
    if base_input_dir.exists():
        for item in base_input_dir.iterdir():
            # Keep generated runtime directories separate; only mirror top-level
            # immutable templates needed for env registration and reset.
            if item.is_file():
                _symlink_if_missing(item, CYCLES_INPUT_PATH.joinpath(item.name))


_bootstrap_runtime_cycles_tree()
