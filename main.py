#!/usr/bin/env python
import sys
from tool_class import tool_class
import os

""" database directory """
tool_dir = os.path.dirname(os.path.realpath(__file__))
db_folder = os.path.join(tool_dir, "database")
if not os.path.isdir(db_folder):
    os.mkdir(db_folder)
database = os.path.join(db_folder, "repos.txt")
print(database)
try:
    repo_list = open(database).read().split("\n")
    repo_list = list(filter(None, repo_list))
except:
    repo_list = []

def tool_setup():
    t = tool_class.tool(name='Repo Manager')
    # description
    t.add_description("""
                    Used to manage Repositories, given in a list
                    Used now to pull all updates for given repos
                    """)
    # required args
    t.add_required("action", "requested action")

    # optional args

    # default args
    t.add_default("action")
    return t

def pull_repos(t):
    if len(repo_list) == 0:
        t.msg("No repos to pull in database")
        t.msg("Aborting...")
        exit()
    for repo in repo_list:
        if "~" in repo:
            r_path = os.path.expanduser(repo)
        else:
            r_path = repo
        t.msg("Pulling rep: "+ repo)
        os.chdir(r_path)
        out = os.popen("git pull").read()
        t.msg("git output : "+ out)

def add_repo(t):
    cwd = os.getcwd()
    t.msg("Appending "+cwd)
    repo_list.append(cwd)
    f = open(database,"w")
    f.write("\n".join(repo_list))
    f.close()

def rem_repo(t):
    cwd = os.getcwd()
    t.msg("Removing "+cwd)
    repo_list.remove(cwd)
    f = open(database,"w")
    f.write("\n".join(repo_list))
    f.close()

def list_repos(t):
    if len(repo_list) == 0:
        t.msg("No repos to pull in database")
        t.msg("Aborting...")
        exit()
    t.msg("the following Repos are managed:")
    for item in repo_list:
        t.msg(item)

def run(t):
    if t.args.action == "pull":
        pull_repos(t)
    elif t.args.action == "add":
        add_repo(t)
    elif t.args.action == "rm":
        rem_repo(t)
    elif t.args.action == "list":
        list_repos(t)
    else:
        t.msg("Unknown action, aborting...")
        exit()

def main(args):
    t = tool_setup()
    t.read_arguments(sys.argv[1:])
    t.start()
    run(t)
    t.end()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
