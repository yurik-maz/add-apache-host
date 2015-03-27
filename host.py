#!/usr/bin/env python3
# -*-coding: utf-8 -*-
import os


class WriteHost:
    def __init__(self):
        self.choice = 0

    def get_choice(self):
        print('''
        ================================
        Select action:
        1 - create catalog end host file
        2 - create only host file
        3 - exit
        ================================
        ''')
        try:
            self.choice = int(input('? '))
        except Exception:
            print('Your choice is wrong! Please, try again...')
            exit()

    def main(self):
        self.get_choice()
        if self.choice == 1:
            self.create_catalog(1)
        elif self.choice == 2:
            self.create_catalog(0)
        else:
            print("Good bye!")
            exit()

    def create_catalog(self, cat):
        catalog = str(input('Enter dir name for site (/var/www/...):'))
        if catalog == '':
            self.create_catalog(cat)

        if cat == 1:
            print('Creating directory /var/www/' + catalog + '...\n')
            os.system('sudo mkdir /var/www/' + catalog)

        self.create_host(catalog)

    def create_host(self, catalog):
        hostname = input('Enter hostname:')
        if hostname == '':
            self.create_host(catalog)

        print('Add to host file... \n')
        with open('/etc/hosts', 'rt') as f:
            s = f.read() + '\n' + '127.0.0.1\t\t\t' + hostname + '\n'
            with open('/tmp/etc_hosts.tmp', 'wt') as file:
                file.write(s)
        os.system('sudo mv /tmp/etc_hosts.tmp /etc/hosts')

        print('Generate virtual host file...\n')
        with open('/tmp/' + hostname + '.tmp', 'wt') as file:
            conf = '<VirtualHost ' + hostname + '>\n'
            conf += '\tDocumentRoot /var/www/' + catalog + '\n'
            conf += '\t<Directory "/var/www/' + catalog + '">\n'
            conf += '\t\tallow from all\n'
            conf += '\t\tOptions All\n'
            conf += '\t\tAllowOverride All\n'
            conf += '\t</Directory>\n'
            conf += '</VirtualHost>'
            file.write(conf)

        os.system('sudo mv /tmp/' + hostname + '.tmp /etc/apache2/sites-available/' + hostname + '.conf')
        os.system('sudo a2ensite ' + hostname + '.conf')
        os.system('sudo service apache2 restart')

if __name__ == "__main__":
    print('Generate virtual host script.\n')
    h = WriteHost()
    h.main()
