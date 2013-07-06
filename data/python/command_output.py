from subprocess import Popen, PIPE, STDOUT
import shlex


def get_simple_cmd_output(cmd, stderr=STDOUT):
    """Execute a simple external command and get its output.
    
    The command contains no pipes. Error messages are
    redirected to the standard output by default.
    """
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]


def get_complex_cmd_output(cmd, stderr=STDOUT):
    """
    Execute a piped command and get the lines of the output in a list.
    """
    proc =  Popen(cmd, shell=True, stdout=PIPE, stderr=stderr)
    return proc.stdout.readlines()

print get_simple_cmd_output("date")
print get_complex_cmd_output("date | wc")[0]
