import sys
import os


def writehost(hostname, catalog=None):
    os.system('mkdir /var/www/' + catalog)

    with open('/etc/hosts', 'rt') as f:
        s = f.read() + '\n' + '127.0.0.1\t\t\t' + hostname + '\n'
        with open('/tmp/etc_hosts.tmp', 'wt') as outf:
            outf.write(s)
        os.system('sudo mv /tmp/etc_hosts.tmp /etc/hosts')

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
    host = sys.argv[1]
    catalog = sys.argv[2]
    # if len(sys.argv) > 2:
    #     catalog = sys.argv[2]

    writehost(host, catalog)