import os


class WriteHost():

    def __init__(self):
        pass

    def go(self):
        print('Select action')
        print('1 - create catalog end host file')
        print('2 - create only host file')
        print('3 - exit')

        action = int(raw_input('Enter num: '))

        if action == 1:
            self.createcatalog(1)
        elif action == 2:
            self.createcatalog(0)
        else:
            exit()

    def createcatalog(self, cat):
        catalog = raw_input('Enter dir name for site (/var/www/...):')
        if catalog == '':
            self.createcatalog(cat)

        if cat == 1:
            print('Creating directory /var/www/' + catalog + '...\n')
            os.system('mkdir /var/www/' + catalog)

        self.createhost(catalog)

    def createhost(self, catalog):
        hostname = raw_input('Enter hostname:')
        if hostname == '':
            self.createhost(catalog)

        print('Add to host file... \n')
        with open('/etc/hosts', 'rt') as f:
            s = f.read() + '\n' + '127.0.0.1\t\t\t' + hostname + '\n'
            with open('/tmp/etc_hosts.tmp', 'wt') as outf:
                outf.write(s)
        os.system('sudo mv /tmp/etc_hosts.tmp /etc/hosts')

        print('Generate virtual host file...\n')
        with open('/tmp/' + hostname + '.tmp', 'wt') as hostfile:
            conf = '<VirtualHost ' + hostname + '>\n'
            conf += '\tDocumentRoot /var/www/' + catalog + '\n'
            conf += '\t<Directory "/var/www/' + catalog + '">\n'
            conf += '\t\tallow from all\n'
            conf += '\t\tOptions All\n'
            conf += '\t\tAllowOverride All\n'
            conf += '\t</Directory>\n'
            conf += '</VirtualHost>'
            hostfile.write(conf)

        os.system('sudo mv /tmp/' + hostname + '.tmp /etc/apache2/sites-available/' + hostname + '.conf')
        os.system('sudo a2ensite ' + hostname + '.conf')
        os.system('sudo service apache2 restart')

if __name__ == "__main__":
    print('Generate virtual host script.\n')
    h = WriteHost()
    h.go()