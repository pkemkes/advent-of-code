from typing import Dict, List, Tuple, Optional


class File:
    def __init__(self, name: str, size: int, parent) -> None:
        self.name = name
        self.size = size
        self.parent: Optional[File] = parent

    def get_size(self) -> int:
        return self.size


class Dir(File):
    def __init__(self, name: str, parent) -> None:
        super().__init__(name, 0, parent)
        self.children: Dict[File] = {}

    def get_size(self) -> int:
        return sum([c.get_size() for c in self.children.values()])

    def add_child_file(self, name: str, size: int) -> File:
        child = File(name, size, self)
        self.children[name] = child
        return child

    def add_child_dir(self, name: str):
        child = Dir(name, self)
        self.children[name] = child
        return child


class Tree():
    def __init__(self, input: List[str]):
        self.root = Dir("/", None)
        self.curr_dir = self.root
        self.cmds = input[1:]
        self.parse_cmds()

    def parse_cmds(self):
        i = 0
        while i < len(self.cmds):
            cmd = self.cmds[i].split(" ")[1]
            if cmd == "cd":
                self.change_dir(i)
            elif cmd == "ls":
                i += self.parse_ls(i)
            else:
                raise Exception(f"Unknown command {cmd}")
            i += 1

    def change_dir(self, i: int):
        dir_to_change_to = self.cmds[i].split(" ")[2]
        if dir_to_change_to == "..":
            self.curr_dir = self.curr_dir.parent
        else:
            self.curr_dir = self.curr_dir.children[dir_to_change_to]

    def parse_ls(self, i: int) -> int:
        output = self.get_ls_output(i)
        for size_or_type, name in output:
            if size_or_type.isnumeric():
                self.curr_dir.add_child_file(name, int(size_or_type))
            else:
                self.curr_dir.add_child_dir(name)
        return len(output)

    def get_ls_output(self, i: int) -> List[Tuple[str, str]]:
        output = []
        pos = i+1
        while pos < len(self.cmds) and not is_cmd(self.cmds[pos]):
            output.append(self.cmds[pos])
            pos += 1
        return [line.split(" ") for line in output]


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]
    tree = Tree(input)
    all_dirs = get_all_dirs(tree.root)

    # #### Puzzle 1 #### #

    sum_size = sum([d.get_size() for d in all_dirs if d.get_size() <= 100000])
    print("Summed size of dirs with max size 100000:", sum_size)

    # #### Puzzle 2 #### #

    total_space = 70000000
    needed_space = 30000000
    used_space = tree.root.get_size()
    need_to_free = needed_space - (total_space - used_space)
    print("Need to free", need_to_free)
    dirs_large_enough = [d for d in all_dirs if d.get_size() >= need_to_free]
    dirs_large_enough_sorted = sorted(dirs_large_enough,
                                      key=lambda d: d.get_size())
    print("Smallest size to delete:", dirs_large_enough_sorted[0].get_size())


def get_all_dirs(curr_dir: Dir) -> List[Dir]:
    dirs = [curr_dir]
    for child in curr_dir.children.values():
        if isinstance(child, Dir):
            dirs += get_all_dirs(child)
    return dirs


def is_cmd(line: str) -> bool:
    return line.startswith("$ ")


if __name__ == "__main__":
    main()
