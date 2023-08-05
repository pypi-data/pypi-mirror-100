import importlib
import sys
from pathlib import Path


def _check_scorer_file(app_name: str):
    """
    Check if the name of the scorer has not been modified to be upload
    on the plateform
    """
    local_path = Path().cwd()
    path_folder = (local_path / app_name).resolve()

    if not path_folder.is_dir():
        raise NameError(f"The app {app_name} doesn't exist")

    path_init = path_folder.joinpath("__init__.py")
    path_scorer = path_folder.joinpath("scorer.py")

    if not path_init.is_file():
        raise FileNotFoundError(
            "The app folder must be a module and contain __init__.py file"
        )

    if not path_scorer.is_file():
        similar_file = _find_similar_file(path_folder, "score")
        message = "The scorer filename must be scorer.py"
        if similar_file is not None:
            message += f", found this similar file instead : {similar_file}"

        raise FileNotFoundError(message)

    # append current path to the pkg to find the app
    # as a module
    sys.path.append(".")
    mod = importlib.import_module(app_name + ".scorer")
    avail_members = dir(mod)

    if "Scorer" not in avail_members:
        raise ModuleNotFoundError("You must have a Scorer class in your scorer class")


def _find_similar_file(path_folder: Path, pattern: str) -> str:
    """
    Find python files containing pattern in a specific folder
    """
    for file in path_folder.iterdir():
        filename = file.name
        if (filename.__contains__(pattern)) and (filename.endswith("py")):
            return filename
            break

    return None
