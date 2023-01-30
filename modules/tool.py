import sys
import os
import argparse
import getopt
import git
from datetime import datetime
from modules import utils as u

class tool:
    """A class used to create small python tools"""
    def get_git_data(self):
        # get path
        filepath = os.path.realpath(sys.argv[0])
        filedir  = os.path.dirname(filepath)
        try:
            g = git.Git(filedir)
            log = g.log("--pretty=%an::%ad::%s")
        except:
            versions = [{'author' :'-----',
                         'date'   :'--.--.--',
                         'time'   :'------',
                         'comment':'NOT COMMITED YET!'}]
            return versions
        # get log string
        versions = []
        for line in log.split('\n'):
            parts = line.split('::')
            v_dict = dict()
            v_dict['author'] = parts[0]
            v_time = datetime.strptime(parts[1],
                        "%a %b %d %H:%M:%S %Y %z")
            v_dict['date']    = v_time.strftime("%d.%m.%y")
            v_dict['time']    = v_time.strftime("%H:%M")
            v_dict['comment'] = parts[2]
            versions.append(v_dict)
        return versions

    def __init__(self, name,
                deprecated=False,
                lic = "MIT",
                ):
        self.path            = os.path.realpath(__file__)
        self.name            = name
        self.deprecated      = deprecated
        self.parser          = argparse.ArgumentParser(
                               formatter_class=argparse.RawDescriptionHelpFormatter,
                               add_help=False,
                               usage=argparse.SUPPRESS,
                               epilog = None,
                               )
        self.parser._action_groups.pop()
        self.required_list   = []
        self.required = self.parser.add_argument_group('required arguments')
        self.optional_list   = []
        self.optional = self.parser.add_argument_group('optional arguments')
        self.add_optional('verbose','toggle status messages', default=None)
        self.add_optional('help', 'display help text')
        self.add_optional('license', 'display license text')
        self.default = None
        self.versions= self.get_git_data()    
        self.license = lic
    """
    check build
    """

    # some functions the check the built tool

    """
    Printing functions
    """
    def print_arguments_formatted(self):
        longest = 14
        if self.required_list:
            print('*** Required arguments are:')
            for req in self.required_list:
                print('*** '+req['s']+', '+req['l']+' '*(longest-len(req['l']))+' : ',req['desc'])
            u.print_starline()
        if self.optional_list:
            print('*** Optional arguments are:')
            for opt in self.optional_list:
                print('*** '+opt['s']+', '+opt['l']+' '*(longest-len(opt['l']))+' : ',opt['desc'])
            u.print_starline()

    def print_help(self):
        u.print_starline()
        print('*** Help for tool      :', self.name)
        u.print_starline()
        print('*** Tool Description   :')
        print(self.description)
        u.print_starline()
        self.print_arguments_formatted()
        print('*** created on         :', self.versions[-1]['date'])
        print('*** by                 :', self.versions[-1]['author'])
        print('*** last commit        :', self.versions[0]['date'])
        print('*** by                 :', self.versions[0]['author'])
        print('*** version            :', len(self.versions))
        print('*** deprecated         :', self.deprecated)
        print('*** license            :', self.license)
        u.print_starline()
        print('***   date   | version | change log')
        u.print_starline()
        for i,v in enumerate(self.versions):
            i = len(self.versions)-i
            print('***',v['date'],'|'+(4-len(str(i)))*' ',i,'   |',v['comment'])
    
        u.print_starline()
        sys.exit()

    def print_license(self):
        if self.license == "MIT":
            mit =u.mit_license().format("20"+self.versions[-1]['date'][-2:],
                                            self.versions[-1]['author'])
            u.print_starline()
            print(mit)
            u.print_starline()
        else:
            print("ERROR: Unknown License specified")
        exit()
        

    def start(self):
        if self.args.verbose:
            u.print_starline()
            print('*** Tool "'+self.name+'" successfully initiated')
            u.print_starline()
            print('*** created on     :', self.versions[-1]['date'])
            print('*** by             :', self.versions[-1]['author'])
            print('*** last commit    :', self.versions[0]['date'])
            print('*** by             :', self.versions[0]['author'])
            print('*** version        :', len(self.versions))
            print('*** deprecated     :', self.deprecated)
            print('*** license        :', self.license)
            u.print_starline()

    def end(self):
        if self.args.verbose:
            u.print_starline()
            print('*** Tool "'+self.name+'" successfully executed')
            u.print_starline()

    def msg(self, string):
        if self.args.verbose:
            print('*** '+string)

    """
    actions
    """
    def add_description(self, string):
        lines = string.split('\n')
        lines = list(filter(None,lines))
        for i,line in enumerate(lines):
            lines[i] = '*** '+u.remove_1st_spaces(line)  
        string = '\n'.join(lines[0:-1])
         
        self.description = string
    """
    argument parsing
    """
    def add_required(self,
                     argument,
                     desc,
                     default=None,
                     action=None,
                     ):
        req = {}
        req['s'] = '-'+list(argument)[0]
        req['l'] = '--'+argument
        req['default'] = default
        req['desc'] = desc
        req['action'] = action
        self.required_list.append(req)
        self.required.add_argument(req['s'],req['l'],default=req['default'], action = req['action'])

    def add_optional(self,
                     argument,
                     desc,
                     default=None,
                     action=None,
                     ):
        opt = {}
        opt['s'] = '-'+list(argument)[0]
        opt['l'] = '--'+argument
        opt['default'] = default
        opt['desc'] = desc
        opt['action'] = action
        self.optional_list.append(opt)
        self.optional.add_argument(opt['s'],opt['l'],default=opt['default'], action = opt['action'])

    def add_default(self,arg):
        self.default = '-'+list(arg)[0] 

    def insert_default_arg(self, arguments):
        if arguments:
            if '-' or '--' not in arguments :
                arguments.insert(0,self.default)
        return arguments

    def help_empty(self, arguments):
        # no argument is passed -> print help
        if not arguments:
            self.print_help()
        # help argument is passed
        elif any (s in ['-h','--help'] for s in arguments):
            self.print_help()
        elif any (s in ['-l','--license'] for s in arguments):
            self.print_license()
        else:
            return

    def read_arguments(self, arguments):
        if self.default != None:
            arguments=self.insert_default_arg(arguments)
        self.help_empty(arguments)
        args = self.parser.parse_args(arguments)
        args.verbose = not args.verbose
        self.args = args
