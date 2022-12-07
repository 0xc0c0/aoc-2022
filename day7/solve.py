from __future__ import annotations
import logging
import os
from dataclasses import dataclass, field
from typing import List

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

@dataclass
class Line():
    command: bool
    data: List[str]

@dataclass
class File():
    size: int
    name: str

@dataclass
class DirNode():
    name: str
    files: List[File] = field(default_factory=lambda: [])
    child_dirs: List[DirNode] = field(default_factory=lambda: [])
    parent_dir: DirNode = None
    
    def getParentDir(self):
        if self.parent_dir:
            return self.parent_dir
        else:
            return self
    
    def getFile(self, name: str):
        file = next((f for f in self.files if f.name == name), None)
        return file or None
    
    def getChildDir(self, name: str):
        dir = next((d for d in self.child_dirs if d.name == name), None)
        return dir or None
    
    def printDirTree(self, tab=0):
        print(f"{' ' * tab}- {self.name} (dir)")
        for f in self.files:
            print(f"{' ' * (tab + 2)}- {f.name} (file, size={f.size})")
        for d in self.child_dirs:
            d.printDirTree(tab=tab + 2)
            
    def getTotalSize(self):
        total = sum([f.size for f in self.files])
        total += sum([d.getTotalSize() for d in self.child_dirs])
        return total
    
    def getAllDirs(self):
        dirs = [self]
        for n in self.child_dirs:
            dirs = dirs + n.getAllDirs()
        return dirs

def parse_line(text_line: str):
    if text_line.startswith('$'):
        return Line(command=True, data=text_line[1:].strip().split())
    else:
        return Line(command=False, data=text_line.strip().split())

def parse_data(text_data):
    lines = [parse_line(line.strip()) for line in text_data.strip('\n').strip().split('\n')]
    return lines

def process_line(root: DirNode, dir: DirNode, line: Line):
    logger.debug(line)
    if line.command:
        cmd = line.data[0]
        if cmd == 'ls':
            return dir #no action
        elif cmd == 'cd':
            arg = line.data[1]
            child_dir = dir.getChildDir(arg)
            if arg == '..':
                return dir.getParentDir()
            elif arg == '/':
                return root
            if child_dir:
                return child_dir
            else: 
                #TODO: create child_dir if need be
                logger.debug(f"child dir {arg} for dir {dir.name} not found!")
                return None
        else:
            return None
    else: # data line return for ls
        if line.data[0] == 'dir':
            dirname = line.data[1]
            if dir.getChildDir(dirname) is None:
                # child directory needs to be created
                new_dir = DirNode(name=dirname, parent_dir=dir)
                dir.child_dirs.append(new_dir)
        else: #this is a file entry line with format <size> <filename>
            size, fname = line.data
            size = int(size)
            if dir.getFile(fname) is None:
                new_file = File(size, fname)
                dir.files.append(new_file)
    return dir

def process_lines(lines):
    root = dir = DirNode(name='/')
    for line in lines:
        dir = process_line(root, dir, line)
    return root

def find_all_dirs(root: DirNode, limit:int = 100000, upper_limit:bool = True):
    all_dirs = root.getAllDirs()
    if upper_limit is True:
        return [d.getTotalSize() for d in all_dirs if d.getTotalSize() <= limit]
    else:
        return [d.getTotalSize() for d in all_dirs if d.getTotalSize() >= limit]

def find_best_dir_to_free_up_space(root: DirNode):
    disk_size = 70000000
    current_used = root.getTotalSize()
    required_disk_space = 30000000
    required_free_up = required_disk_space - (disk_size - current_used)
    logger.debug(f"Need to free up {required_free_up} space")
    return min(find_all_dirs(root, required_free_up, upper_limit=False))

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    lines = parse_data(data)
    root = process_lines(lines)
    # root.printDirTree()
    answer = sum(find_all_dirs(root))
    logger.info(f"Puzzle1: Total Size of All Directories <= 100000: {answer}")
    answer = find_best_dir_to_free_up_space(root)
    logger.info(f"Puzzle2: Directory Size to Delete to get to >= 30000000 free space: {answer}")
    
if __name__ == '__main__':
    main()