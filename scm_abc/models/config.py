<<<<<<< HEAD
#!/usr/bin/python
from configparser import ConfigParser
import psycopg2
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ScmConfig(models.Model):
    _name = 'scm.config'

    host = fields.Char(string='Host')
    database = fields.Char(string='DB Name')
    port = fields.Char(string='Port')
    user = fields.Char(string='User')
    password = fields.Char(string='Password')
    active = fields.Boolean(string="Active", default=True)

    # # host = localhost
    # # database = odoo_awb
    # # port = 5422
    # # user = odoo14wsl
    # # password = odoo
    #
    def scm_conn(self):
        """ Connect to the PostgreSQL database server """
        conf = self.env['scm.config'].search([('active', '=', True)], limit=1)
        if conf:
            print("connection dndbdbddbdbdb: ", conf.port)
            print("connection dndbdbddbdbdb: ", conf.active)
            params = {'host':conf.host,
                      'database':conf.database,
                      'port':conf.port,
                      'user':conf.user,
                      'password':conf.password}
                                 # print('From Config Connecting to the PostgreSQL database...', params)

                                 # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            return conn

            # create a cursor
            # cur = conn.cursor()
            #
            # cur.execute('SELECT name, partner_id from res_company')
            #
            # # display the PostgreSQL database server version
            # db_version = cur.fetchall()
            # for com in db_version:
            #     print(com)
            # #
            # print(db_version)
            # cur.close()

        # conn = None
        # try:
        #     conf = self.env.search([('active', '=', True)], limit=1)
        #     print("connection dndbdbddbdbdb: ", conf.port)
        #     print('POrt port...', self.port)
        #     # read connection parameters
        #     # conn =
        #     # params = {host = "localhost",
        #     #                  #                 database = "odoo_awb",
        #     #                  #                 port = "5422",
        #     #                  #                 user = "odoo14wsl",
        #     #                  #                 password = "odoo"}
        #     #                  # print('From Config Connecting to the PostgreSQL database...', params)
        #     #
        #     #                  # connect to the PostgreSQL server
        #     #                  print('Connecting to the PostgreSQL database...')
        #     conn = psycopg2.connect(
        #         host="localhost",
        #         database="odoo_awb",
        #         port="5422",
        #         user="odoo14wsl",
        #         password="odoo")
        #
        #     # create a cursor
        #     cur = conn.cursor()
        #
        #     # execute a statement
        #     print('PostgreSQL database version:')
        #     cur.execute('SELECT name, partner_id from res_company')
        #
        #     # display the PostgreSQL database server version
        #     db_version = cur.fetchall()
        #     for com in db_version:
        #         print(com)
        #
        #     # print(db_version)
        #
        #     # close the communication with the PostgreSQL
        #     cur.close()
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print(error)
        # finally:
        #     if conn is not None:
        #         conn.close()
        #         print('Database connection closed.')
=======
#!/usr/bin/python
from configparser import ConfigParser
import psycopg2
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ScmConfig(models.Model):
    _name = 'scm.config'

    host = fields.Char(string='Host')
    database = fields.Char(string='DB Name')
    port = fields.Char(string='Port')
    user = fields.Char(string='User')
    password = fields.Char(string='Password')
    active = fields.Boolean(string="Active", default=True)

    def scm_conn(self):
        """ Connect to the PostgreSQL database server """
        conf = self.env['scm.config'].search([('active', '=', True)], limit=1)
        if conf:
            print("connection dndbdbddbdbdb: ", conf.port)
            print("connection dndbdbddbdbdb: ", conf.active)
            params = {'host':conf.host,
                      'database':conf.database,
                      'port':conf.port,
                      'user':conf.user,
                      'password':conf.password}
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            return conn

>>>>>>> 291cf88f137f7da43aafb1270b86f6565dba0dbc
