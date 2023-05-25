from pathlib import Path


def get_rsc_path(relative_path: str) -> Path:
    path: Path
    path = Path(Path(__file__).parent.parent, relative_path)
    return path.as_posix()
