import os

DOMAIN_FILE = '/etc/postfix/vdomain'
USERS_FILE = '/etc/postfix/vmap'
MAILDIR_BASE = '/var/spool/vhosts/'

def getbody(message): #getting plain text 'email body'
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload()
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload()
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload()
    return body

def write_user(user):
    users = read_users().get('users')
    users.append(user)

    with open(USERS_FILE, 'w') as f:
        for u in users:
            domain = u.split('@')[1]
            username = u.split('@')[0]
            f.write("%s %s/%s/\n"%(u, domain, username))
    os.system("postmap %s"%USERS_FILE)
    return users

def read_users():
    with open(USERS_FILE) as f:
        lines = f.readlines()
        users = [line.strip().split()[0] for line in lines]
        users_maildir = [line.strip().split()[1] for line in lines]
    return {"users": users, "users_maildir": users_maildir}

def write_domains(domains):
    with open(DOMAIN_FILE, 'w') as f:
        for domain in domains:
            f.write("%s OK\n"%domain)
    return domains

def read_domains():
    with open(DOMAIN_FILE) as f:
        domains = [line.strip().split()[0] for line in f.readlines()]
    return domains

