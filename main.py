#!/usr/bin/env python
import sys
from tool_class import tool_class
import os

list_f = "./repos.txt"
repo_list = open(list_f).read().split("\n")
def tool_setup():
    t = tool_class.tool(name='Repo Manager')
    # description
    t.add_description("""
                    Used to manage Repositories, given in a list
                    Used now to pull all updates for given repos
                    """)
    # required args

    # optional args

    # default args
    return t
def run(t):
    print(repo_list)

def main(args):
    t = tool_setup()
    t.read_arguments(sys.argv[1:])
    t.start()
    run(t)
    t.end()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
