import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object, read_tree
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    # PUT YOUR CODE HERE
    for i in paths:
        if not (i.is_dir()):
            update_index(gitdir, [i], write=True)

        else:
            add(gitdir, list(i.glob("*")))


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    # PUT YOUR CODE HERE
    parentcom = resolve_head(gitdir)
    comtree = write_tree(gitdir, read_index(gitdir), str(gitdir.parent))
    hashcom = commit_tree(gitdir, comtree, message, parentcom, author)
    return hashcom


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    # PUT YOUR CODE HERE
    for i in read_index(gitdir):
        if pathlib.Path(i.name).exists():
            os.remove(i.name)

    closeprog = False
    datacom = commit_parse(read_object(obj_name, gitdir)[1])

    while not closeprog:
        tree: tp.List[tp.Tuple[pathlib.Path, tp.List[tp.Tuple[int, str, str]]]] = [
            (gitdir.parent, read_tree(read_object(datacom["tree"], gitdir)[1]))
        ]

        while tree:
            pathoftree, treeinf = tree.pop()

            for j in treeinf:
                form, data = read_object(j[1], gitdir)
                if not (form == "tree"):
                    if not (pathoftree / j[2]).exists():
                        with (pathoftree / j[2]).open("wb") as fileforrep:
                            fileforrep.write(data)
                        (pathoftree / j[2]).chmod(int(str(j[0]), 8))

                else:
                    tree.append((pathoftree / j[2], read_tree(data)))
                    if not (pathoftree / j[2]).exists():
                        (pathoftree / j[2]).mkdir()

        if not ("parent" in datacom):
            closeprog = True

        else:
            datacom = commit_parse((read_object(datacom["parent"], gitdir)[1]))

    for dir in gitdir.parent.glob("*"):
        if dir != gitdir and dir.is_dir():
            try:
                os.removedirs(dir)
            except OSError:
                continue
