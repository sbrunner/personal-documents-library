import re
from os import unlink
from tempfile import NamedTemporaryFile
from subprocess import check_call
from shutil import copyfile
import edocuments


def process(names, filename=None, destination_filename=None, in_extention=None):
    cmds = edocuments.config.get("cmds", {})
    out_ext = in_extention

    original_filename = filename
    if destination_filename is None:
        destination_filename = filename
    for name in names:
        cmd = cmds.get(name)
        if cmd is None:
            raise "Missing command '%s' in `cmds`" % name

        if isinstance(cmd, str):
            cmd = dict(cmd=cmd)

        if cmd.get('type') == 'rename':
            destination_filename = rename(cmd, destination_filename)
        else:
            if 'out_ext' in cmd:
                out_ext = cmd['out_ext']

            inplace = cmd.get('inplace', False)
            cmd_cmd = cmd.get('cmd')

            if inplace:
                out_name = filename
            else:
                if out_ext is None:
                    out_name = NamedTemporaryFile(mode='w+b').name
                else:
                    out_name = NamedTemporaryFile(mode='w+b', suffix='.' + out_ext).name

            params = {}

            if filename is not None:
                params["in"] = "'%s'" % filename.replace("'", "'\''")

            if not inplace:
                params["out"] = "'%s'" % out_name.replace("'", "'\''")

            cmd_cmd = cmd_cmd.format(**params)

            print("%s: %s" % (name, cmd_cmd))
            check_call(cmd_cmd, shell=True)

            filename = out_name

    if original_filename != filename:
        if original_filename is not None:
            unlink(original_filename)
        if out_ext is not None:
            destination_filename = "%s.%s" % (re.sub(
                r"\.[a-z0-9A-Z]{2,5}$", "",
                destination_filename
            ), out_ext)
        if filename != destination_filename:
            copyfile(filename, destination_filename)
            unlink(filename)

def rename(cmd, destination_filename)
    from_re = cmd.get('from')
    to_re = cmd.get('to')
    if cmd.get('format') in ['upper', 'lower']:
        def format_term(term):
            if cmd.get('format') == 'upper':
                return term.upper()
            else:
                return term.lower()
        to_re = lambda m: format_term(m.group(0))
    return re.sub(from_re, to_re, destination_filename)


def destination_filename(names, destination_filename=None, in_extention=None):
    cmds = edocuments.config.get("cmds", {})
    out_ext = in_extention

    original_filename = filename
    if destination_filename is None:
        destination_filename = filename
    for name in names:
        cmd = cmds.get(name)
        if cmd is None:
            raise "Missing command '%s' in `cmds`" % name

        if isinstance(cmd, str):
            cmd = {}

        if cmd.get('type') == 'rename':
            destination_filename = rename(cmd, destination_filename)
        else:
            if 'out_ext' in cmd:
                out_ext = cmd['out_ext']

    if original_filename != filename:
        if out_ext is not None:
            destination_filename = "%s.%s" % (re.sub(
                r"\.[a-z0-9A-Z]{2,5}$", "",
                destination_filename
            ), out_ext)
