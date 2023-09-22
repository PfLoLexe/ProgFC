import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        # PUT YOUR CODE HERE
        return struct.pack((f"!10I20sH{ len(self.name) }s{ 8 - ( 62 + len(self.name) ) % 8 }x"), self.ctime_s, self.ctime_n, self.mtime_s, self.mtime_n, self.dev, self.ino & 0xFFFFFFFF, self.mode, self.uid, self.gid, self.size, self.sha1, self.flags, self.name.encode(),)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        # PUT YOUR CODE HERE
        date = list(struct.unpack(f"!10I20sH{len(data) - 62}s", data))
        date[len(date) - 1] = date[len(date) - 1].strip(b"\00").decode()

        return GitIndexEntry(*date)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    # PUT YOUR CODE HERE
    if not ((gitdir / "index").exists()):
        return []

    with (gitdir / "index").open("rb") as fileforrep:
        read = fileforrep.read()

    flastpos = 12
    res = []

    for it in range(struct.unpack("!I", read[8:12])[0]):
        slastpos = read.index(b"\00", flastpos + 62)

        while ((slastpos - 11) % 8 != 0) or (read[slastpos] != 0):
            slastpos += 1

        res.append(GitIndexEntry.unpack(read[flastpos : slastpos + 1]))

        flastpos = slastpos + 1

    return res


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    # PUT YOUR CODE HERE
    inf = b"DIRC" + struct.pack("!2I", 2, len(entries))

    for i in entries:
        inf += i.pack()

    inf += hashlib.sha1(inf).digest()
    with (gitdir / "index").open("wb") as fileforrep:
        fileforrep.write(inf)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    # PUT YOUR CODE HERE
    readinf = read_index(gitdir)

    if not details:
        for j in readinf:
            print(j.name)

    else:
        for i in readinf:
            print(f"{i.mode:o} {i.sha1.hex()} 0\t{i.name}")


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    # PUT YOUR CODE HERE
    readinf = read_index(gitdir)

    for i in paths:
        with i.open("rb") as fileforrep:
            inf = fileforrep.read()

        hash = hash_object(inf, "blob", write=True)
        stat = i.stat()

        readinf.append(GitIndexEntry(ctime_s=int(stat.st_ctime), ctime_n=0, mtime_s=int(stat.st_mtime), mtime_n=0, dev=stat.st_dev, ino=stat.st_ino, mode=stat.st_mode, uid=stat.st_uid, gid=stat.st_gid, size=stat.st_size, sha1=bytes.fromhex(hash), flags=len(i.name), name=str(i),))

    if write:
        write_index(gitdir, sorted(readinf, key=lambda j: j.name))
