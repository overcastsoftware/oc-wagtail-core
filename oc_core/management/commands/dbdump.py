"""
 Command for backup database
"""

import os, subprocess, time
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Backup database. Only Mysql and Postgresql engines are implemented"
    args = "<outfile>"

    def handle(self, *args, **options):

        from django.db import connection
        from django.conf import settings

        self.engine = settings.DATABASES['default']['ENGINE']
        self.db = settings.DATABASES['default']['NAME']
        self.user = settings.DATABASES['default']['USER']
        self.passwd = settings.DATABASES['default']['PASSWORD']
        self.host = settings.DATABASES['default']['HOST']
        self.port = settings.DATABASES['default']['PORT']

        if len(args) == 0:
            backup_dir = 'backups'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            outfile = os.path.join(backup_dir, 'backup_%s.dump' % time.strftime('%y%m%d%S'))
        else:
            outfile = args[0]

        if self.engine == 'mysql':
            print 'Doing Mysql backup to database %s into %s' % (self.db, outfile)
            self.do_mysql_backup(outfile)
        elif self.engine in ('django.db.backends.postgresql_psycopg2', 'postgresql_psycopg2', 'postgresql'):
            print 'Doing Postgresql backup to database %s into %s' % (self.db, outfile)
            self.do_postgresql_backup(outfile)
        else:
            print 'Backup in %s engine not implemented' % self.engine

    def do_mysql_backup(self, outfile):
        args = []
        if self.user:
            args += ["--user=%s" % self.user]
        if self.passwd:
            args += ["--password=%s" % self.passwd]
        if self.host:
            args += ["--host=%s" % self.host]
        if self.port:
            args += ["--port=%s" % self.port]
        args += [self.db]

        os.system('mysqldump %s > %s' % (' '.join(args), outfile))

    def do_postgresql_backup(self, outfile):
        args = []
        if self.user:
            args += ["--username=%s" % self.user]
        if self.host:
            args += ["--host=%s" % self.host]
        if self.port:
            args += ["--port=%s" % self.port]
        if self.db:
            args += [self.db]
        print 'pg_dump -Fc %s > %s' % (' '.join(args), outfile)
        subprocess.call(['PGPASSWORD="%s" pg_dump -Fc %s > %s' % (self.passwd, ' '.join(args), outfile)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True, shell=True)
