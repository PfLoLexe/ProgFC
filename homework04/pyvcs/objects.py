import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    # PUT YOUR CODE HERE
    resdata = (fmt + " " + str(len(data))).encode() + b"\00" + data
    sumofhash = hashlib.sha1(resdata).hexdigest()

    if write:
        gitdir = repo_find()
        (gitdir / "objects" / sumofhash[:2]).mkdir(exist_ok=True)

        with (gitdir / "objects" / sumofhash[:2] / sumofhash[2:]).open("wb") as fileforrep:
            fileforrep.write(zlib.compress(resdata))

    return sumofhash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    if not (4 <= len(obj_name) <= 40):
        raise Exception(f"Not a valid object name {obj_name}")

    res = []

    for file in (gitdir / "objects" / obj_name[:2]).glob(f"{obj_name[2:]}*"):
        res.append(obj_name[:2] + file.name)

    if not res:
        raise Exception(f"Not a valid object name {obj_name}")
    
    return res


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    pass


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    with (gitdir / "objects" / sha[:2] / sha[2:]).open("rb") as fileforrep:
        date = zlib.decompress(fileforrep.read())

    return date.split(b" ")[0].decode(), date.split(b"\00", maxsplit=1)[1]


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    tree = []

    while data:
        before_sha_ind = data.index(b"\00")
        mode, name = map(lambda x: x.decode(), data[:before_sha_ind].split(b" "))
        sha = data[before_sha_ind + 1 : before_sha_ind + 21]
        tree.append((int(mode), sha.hex(), name))
        data = data[before_sha_ind + 21 :]

    return tree


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    form, data = read_object(obj_name, repo_find())
    if form == "commit" or form == "blob":
        print(data.decode())

    else:
        for i in read_tree(data):
            print(f"{i[0]:06}", "tree" if (i[0] == 40000) else "blob", i[1] + "\t" + i[2])




def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    pass


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    date: tp.Dict[str, tp.Any] = {"message": []}

    for i in raw.decode().split("\n"):
        if i.startswith(("tree", "parent", "author", "committer")):
            name, val = i.split(" ", maxsplit=1)
            date[name] = val

        else:
            date["message"].append(i)

    return date
