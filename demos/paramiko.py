__author__ = 'JunSong<songjun54cm@gmail.com>'
import argparse, base64, paramiko

def main(config):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('10.214.155.238', username='songjun', password='songjun1234')
    stdin, stdout, stderr = client.exec_command('ls')
    print(stdout.readlines())
    cmd='adduser sj1'
    stdin,stdout,stderr=client.exec_command(cmd)
    print('stdout:\n%s\nstderr:\n%s\n'%(stdout.read(),stderr.read()))
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='file', type=str, default='example.txt')
    args = parser.parse_args()
    config = vars(args)
    main(config)


import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.15.82.182', username='udms', key_filename='/export/home/udms/.ssh/id_rsa')
stdin, stdout, stderr = client.exec_command('ls /home')
print(stdout.readlines())