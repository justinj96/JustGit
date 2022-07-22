import paramiko

host = 'ec2-35-164-42-238.us-west-2.compute.amazonaws.com'

con = paramiko.SSHClient()
con.load_system_host_keys()
con.connect(host, username='ubuntu')

stdin, stdout, stderr = con.exec_command('cd /srv/git/justgit.git && git ls-tree HEAD')   
   
files = []
# process the output   
if stderr.read() == b'':   
    for line in stdout.readlines():   
        files.append(line)
         # strip the trailing line breaks   
else:   
    print(stderr.read())  
stdin.close()

for fle in files:
    item = fle.strip().split('\t')[1]
    print(item)