import subprocess

p = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,universal_newlines=True)

out, err = p.communicate()

print out