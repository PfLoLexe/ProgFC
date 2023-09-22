import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    # PUT YOUR CODE HERE
    files = [str(i) for i in (gitdir.parent / dirname).glob("*")]
    sectree: tp.Dict[str, tp.List[GitIndexEntry]] = dict()
    treeinf: tp.List[tp.Tuple[int, pathlib.Path, bytes]] = []

    for i in index:
        if not (i.name in files):
            dirsecname = i.name.lstrip(dirname).split("/", 1)[0]

            if not (dirsecname in sectree):
                sectree[dirsecname] = []
            sectree[dirsecname].append(i)

        else:
            treeinf.append((i.mode, (gitdir.parent / i.name), i.sha1))

    for j in sectree:
        treeinf.append(
            (
                0o40000,
                gitdir.parent / dirname / j,
                bytes.fromhex(
                    write_tree(gitdir, sectree[j], dirname + "/" + j if (dirname != "") else j)
                ),
            )
        )

    treeinf.sort(key=lambda x: x[1])

    data = b"".join(f"{i[0]:o} {i[1].name}".encode() + b"\00" + i[2] for i in treeinf)

    return hash_object(data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    
    # PUT YOUR CODE HERE
    zonetime = time.timezone
    att = int(time.mktime(time.localtime()))

    if zonetime <= 0:
        strofzonetime = "+"
    else:
        strofzonetime = "-"

    strofzonetime += f"{abs(zonetime) // 60 // 60:02}{abs(zonetime) // 60 % 60:02}"
    inf = [f"tree {tree}"]

    if parent is not None:
        inf.append(f"parent {parent}")

    if author is None:
        author = f'{os.getenv("GIT_AUTHOR_NAME")} {os.getenv("GIT_AUTHOR_EMAIL")}'

    inf.append(f"author {author} {att} {strofzonetime}")
    inf.append(f"committer {author} {att} {strofzonetime}")
    inf.append(f"\n{message}\n")

    return hash_object("\n".join(inf).encode(), "commit", write=True)
