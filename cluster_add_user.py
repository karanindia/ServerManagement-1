__author__ = 'JunSong<songjun54cm@gmail.com>'
import argparse
from os import path, popen
import paramiko
from settings import MANAGER, KEY_FILENAME, CLIENT_HOSTS

def run_command(commd):
    return popen(commd)

def full_fill_config(config):
    config['user_home'] = path.join('/home',config['user_name'])
    config['user_shell'] = '/bin/bash'
    config['user_password'] = config['user_name']

def fill_uid(config):
    res_str = run_command('grep \'%s\' /etc/passwd' % config['user_name']).read().strip()
    if len(res_str)<1:
        run_command('sudo useradd %s;echo \"%s:%s\"|sudo chpasswd' % (config['user_name'],config['user_name'], config['user_password']))
        user_info = run_command('grep \'%s\' /etc/passwd' % config['user_name']).read().strip().split(':')
        uid = user_info[2]
        print('Create new user %s with uid %s' % (config['user_name'], uid))
        config['user_id'] = uid
    else:
        res_str = res_str.split('\n')
        if len(res_str)>1:
            print('Error: More than one user detected!')
            print(res_str)
            exit(1)
        elif len(res_str)==1:
            user_info = res_str[0].split(':')
            uid = user_info[2]
            print('Find user %s with uid %s' % (config['user_name'], uid))
            config['user_id'] = uid


def generate_command(config):
    command = 'sudo useradd -m -d %s -s %s -u %s %s;echo \"%s:%s\"|sudo chpasswd' % \
              (config['user_home'], config['user_shell'],
               config['user_id'], config['user_name'],
               config['user_name'], config['user_password']
               )
    return command

def distribute_command(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for client_ip in CLIENT_HOSTS:
        client.connect(client_ip, username=MANAGER, key_filename=KEY_FILENAME)
        stdin, stdout, stderr = client.exec_command(command)
        err_str = stderr.read()
        out_str = stdout.read()
        if len(err_str)>0:
            print('Host: [%s] Error!:\n%s' % (client_ip, err_str))
        else:
            print('Host: [%s] Success!\n%s' % (client_ip, out_str))
        client.close()

def main(config):
    fill_uid(config)
    command = generate_command(config)
    distribute_command(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user_name', dest='user_name', type=str)
    args = parser.parse_args()
    config = vars(args)
    user_name = config['user_name']
    full_fill_config(config)
    main(config)


'''
set privileges in visudo:
Cmnd_Alias USER_CMNDS = /usr/sbin/useradd, /usr/sbin/chpasswd
udms    ALL=(ALL) NOPASSWD: USER_CMNDS
'''