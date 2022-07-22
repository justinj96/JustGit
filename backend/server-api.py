import paramiko

host = 'ec2-35-164-42-238.us-west-2.compute.amazonaws.com'

con = paramiko.SSHClient()
con.load_system_host_keys()
con.connect(host, username='ubuntu')

stdin, stdout, stderr = con.exec_command('cd /srv/git/justgit.git && git ls-tree HEAD')   
   
files = {}
# process the output   
if stderr.read() == b'':   
    for line in stdout.readlines(): 
        lst = line[7:].split('\t')
        file_type, commit = lst[0].split(' ')
        name = lst[1].strip()
        files[commit] = {
            'file_type': file_type,
            'name': name
        }
else:   
    print(stderr.read())  

sub_files = {}

for parent_commit, dct in files.items():
    if dct['file_type'].lower().strip() == 'tree':
        stdin, stdout, stderr = con.exec_command(f'cd /srv/git/justgit.git && git ls-tree {parent_commit}')   
        if stderr.read() == b'':
            for line in stdout.readlines(): 
                lst = line[7:].split('\t')
                file_type, commit = lst[0].split(' ')
                name = lst[1].strip()
                if 'children' in files[parent_commit]:
                    files[parent_commit]['children'].update({
                        commit: {
                        'file_type': file_type,
                        'name': name
                    }})
                else:
                    files[parent_commit].update({'children': {
                        commit: {
                        'file_type': file_type,
                        'name': name
                    }}})
print(files)
stdin.close()
stdout.close()
stderr.close()
con.close()