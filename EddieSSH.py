EddieSSH.py


import paramiko


EddieName = 'EddiePlus_WTR_1.local'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(EddieName, username='root', password='nagidar1')



ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('pwd')



# Start the EddieBalance program
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('./EddieBalance/src/EddieBalance')
# WORKS!


#print ssh_stdout.read() # But don't try to read stdout, since there is not response it will just hang!


stdin, stdout, stderr = ssh.exec_command("sudo dmesg")

# http://jessenoller.com/blog/2009/02/05/ssh-programming-with-paramiko-completely-different
# the stdin return object can be used to interact programatically with the prompt
#stdin.write('lol\n')
#stdin.flush()
#data = stdout.read.splitlines()
