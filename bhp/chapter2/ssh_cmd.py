import paramiko

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # As we are both client and server, accept the key
    client.connect(ip, port=port, username=user, password = passwd) #Make the connection

    _, stdout, stderr = client.exec_command(cmd) #Run the command

    output = stdout.readlines() + stderr.readlines() #Get and report the output

    if output:
        print('--- Output ---')
        for line in output:
            print (line.strip())

if __name__ == '__main__':
    import getpass
    # user = getpass.getuser()

    #You should use key-based authentication in a real engagement. Consider adding later?
    user = input('Username: ')
    password = getpass.getpass()

    ip = input('Enter service IP: ') or '127.0.0.1'
    port = input('Enter port or <CR>: ') or 2222
    cmd = input('Enter command or <CR>: ') or 'id'

    ssh_command(ip, port, user, password, cmd)
