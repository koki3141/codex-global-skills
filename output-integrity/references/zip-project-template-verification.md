# ZIP → project template verification pattern

Use this when a user attaches a ZIP and asks to create a project/template directory from it.

## Bounded workflow

1. Inspect the archive before writing:
   - confirm the ZIP exists and record byte size
   - count entries and total uncompressed bytes
   - list top-level roots; if there is one wrapper root, decide whether to strip it
2. Validate paths before extraction:
   - reject absolute paths
   - reject `..` path components
   - skip empty directory records unless needed
3. Extract to an explicit target under the user-requested scope.
4. Verify extraction:
   - count files and directories under target
   - sum file bytes
   - check key entry-point files (`README.md`, `START_HERE.md`, `pyproject.toml`, docs/scripts)
5. If it is a runnable project, run its own setup and smoke checks. Report actual command output, not just that files exist.
6. If setup generates `.venv`, build output, or artifacts, make clear that post-setup counts exceed raw archive counts.

## Python extraction skeleton

```python
from pathlib import Path
import shutil, zipfile

zip_path = Path("/path/to/archive.zip")
target = Path("/requested/projects/name")

with zipfile.ZipFile(zip_path) as z:
    infos = z.infolist()
    for info in infos:
        name = info.filename
        if not name or name.endswith("/"):
            continue
        p = Path(name)
        if p.is_absolute() or any(part in ("..", "") for part in p.parts):
            raise SystemExit(f"unsafe path in zip: {name}")

    roots = {Path(i.filename).parts[0] for i in infos if i.filename and not i.filename.endswith("/")}
    strip_root = len(roots) == 1

    if target.exists():
        raise SystemExit(f"target already exists: {target}")
    target.mkdir(parents=True)

    for info in infos:
        name = info.filename
        if not name or name.endswith("/"):
            continue
        parts = Path(name).parts[1:] if strip_root else Path(name).parts
        if not parts:
            continue
        out = target.joinpath(*parts)
        out.parent.mkdir(parents=True, exist_ok=True)
        with z.open(info) as src, open(out, "wb") as dst:
            shutil.copyfileobj(src, dst)
```

## macOS pybind11/scikit-build note

For C++/pybind11 Python projects that use CMake `find_package(HDF5 REQUIRED COMPONENTS C)`, Homebrew `hdf5` and `ninja` may be needed before `uv sync` can build the editable wheel. A portable setup check is:

```bash
brew install hdf5 ninja
export CMAKE_PREFIX_PATH="$(brew --prefix hdf5):${CMAKE_PREFIX_PATH:-}"
uv lock --refresh --default-index https://pypi.org/simple   # only if the shipped lock points at an inaccessible internal index
uv sync --frozen
uv run pytest
```

Do not record a transient missing-package failure as a durable limitation; record the setup fix and the verification commands that passed.
