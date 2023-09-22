import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    # PUT YOUR CODE HERE
    dirname = os.getenv("GIT_DIR", ".pyvcs")
    workdir = pathlib.Path(workdir)

    while pathlib.Path(workdir.absolute().root) != workdir.absolute():
        if (workdir / dirname).is_dir():
            return workdir / dirname
        workdir = workdir.parent

    if (workdir / dirname).is_dir():
        return workdir / dirname

    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    # PUT YOUR CODE HERE
    dirname = os.getenv("GIT_DIR", ".pyvcs")
    workdir = pathlib.Path(workdir)
    folders = "refs"

    if workdir.is_file():
        raise Exception(f"{workdir} is not a directory")

    os.makedirs(workdir / dirname / folders / "heads", exist_ok=True)
    os.makedirs(workdir / dirname / folders / "tags", exist_ok=True)
    folders = "objects"
    (workdir / dirname / folders).mkdir()

    with (workdir / dirname / "HEAD").open("w") as fileforrep:
        fileforrep.write("ref: refs/heads/master\n")
    with (workdir / dirname / "config").open("w") as fileforrep:
        fileforrep.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n",
        )
    with (workdir / dirname / "description").open("w") as fileforrep:
        fileforrep.write("Unnamed pyvcs repository.\n")

    return workdir / dirname
