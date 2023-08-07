import argparse
from collections import defaultdict
import json
import sys
import os

from terminaltables import SingleTable

from .param import Param
from .section import Section
from .exceptions import MissingValueError, ValidationError
from .dict_utils import (
    fix_dict, expand_keys, recursive_get, rec_dd, recursive_set,
    NestedNamespace)


class Config:
    def __init__(self):
        self.sections = defaultdict(lambda: None)
        self.sections_to_entries = defaultdict(list)
        self.entries = {}
        self.content = {}

    def add_section(self, section):
        self.sections[section.ns] = section

    def add_entry(self, ns, name, param):
        path = ns + tuple(name.split('.'))
        self.sections_to_entries[ns].append(path)
        self.entries[path] = param

    def collect(self, config):
        config = fix_dict(expand_keys(config))
        for path, param in self.entries.items():
            try:
                value = recursive_get(config, path)
                if value is not None:
                    self.content[path] = value
            except:
                pass
        return self

    def augment_argparse(self, parser):
        parser.add_argument('--config-file', '-C', action='append', default=[],
                            help='Integrate a config file (json or yaml, can be repeated)')

        parser.formatter_class = argparse.RawTextHelpFormatter


        epilog = """
Arguments:
----------

Each argument can be defined from a JSON file, a YAML file, env variable
or from CLI arguments. For CLI just use:

--PATH.TO.ARG=value

"""
        for sec_path, entries in self.sections_to_entries.items():
            table_content = [['Name', 'Default', 'Constraint', 'Description']]
            for path in entries:
                param = self.entries[path]
                argname = '.'.join(path)
                # We do not want to show the args since we have our nice table after
                parser.add_argument(f'--{argname}', help=argparse.SUPPRESS)
                default = param.default
                if param.required:
                    default = 'Requried!'
                table_content.append([argname, default, param.checker.help(), param.desc])
            section_desc = self.sections[sec_path].desc
            epilog += SingleTable(table_content, section_desc).table + "\n\n"


        parser.epilog = epilog

        return self


    def collect_config_file(self, fname):
        try:
            self.collect_json(fname)
        except json.decoder.JSONDecodeError:
            self.collect_yaml(fname)

        return self


    def collect_json(self, fname):
        with open(fname) as handle:
            self.collect(json.load(handle))

        return self

    def collect_yaml(self, fname):
        import yaml
        with open(fname) as handle:
            content = handle.read()
        self.collect(yaml.safe_load(content))

        return self

    def collect_env_variables(self):
        self.collect(dict(os.environ))

        return self

    def collect_argparse_args(self, parser):
        args = parser.parse_args()
        for fname in args.config_file:
            self.collect_config_file(fname)

        args = vars(args)
        del args['config_file']

        self.collect(args)
        self.collect_env_variables()

        return self

    def __getitem__(self, path):
        if isinstance(path, str):
            path = tuple(path.split('.'))

        try:
            param = self.entries[path]
        except KeyError:
            raise KeyError(f"{'.'.join(path)} not defined")

        try:
            value = self.content[path]
        except KeyError:
            value = None

        if value is None and param.default is not None:
            value = param.default

        if value is None and not param.required:
            return value

        return param.validate(value)


    def get(self):
        result = rec_dd()
        for path in self.entries.keys():
            value = self[path]
            recursive_set(result, path, value)

        return NestedNamespace(fix_dict(result))

    def validate(self, mode='stderr'):
        errors = {}
        for path, param in self.entries.items():
            try:
                self[path]
            except (MissingValueError, ValidationError) as e:
                errors[path] = e

        if mode == 'stderr':
            if len(errors) > 0:
                table = [['Param', 'Issue', 'Got']]

                for path, error in errors.items():
                    if isinstance(error, MissingValueError):
                        issue = "Required!"
                        got = ""
                    elif isinstance(error, ValidationError):
                        issue = self.entries[path].checker.help()
                        got = self.content[path]
                    table.append(['.'.join(path), issue, got])

                print(SingleTable(table, 'Argument validation errors').table,
                      file=sys.stderr)
                sys.exit()

        elif mode == 'errordict':
            return errors
