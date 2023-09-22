import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    # PUT YOUR CODE HERE
    with (gitdir / ref).open("w") as file:
        file.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    pass


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    # PUT YOUR CODE HERE
    if not is_detached(gitdir) and refname == "HEAD":
        return str(resolve_head(gitdir))

    if (gitdir / refname).exists():
        with (gitdir / refname).open() as fileforrep:
            return fileforrep.read().strip()

    return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    # PUT YOUR CODE HERE
    with (gitdir / "HEAD").open() as fileforrep:
        return ref_resolve(gitdir, fileforrep.read().strip().split()[1])


def is_detached(gitdir: pathlib.Path) -> bool:
    # PUT YOUR CODE HERE
    try:
        get_ref(gitdir)
    except IndexError:
        return True

    return False


def get_ref(gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    with (gitdir / "HEAD").open() as fileforrep:
        return fileforrep.read().strip().split()[1]
