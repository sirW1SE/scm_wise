import xmlrpc.client

url_db1 = "http://localhost:8092"
db_1 = 'test_db'
username_db_1 = 'admin'
password_db_1 = 'admin'

common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
version_db1 = common_1.version()


print("details...", version_db1)


url_db2 = "http://localhost:8092"
db_2 = 'xml_db'
username_db_2 = 'admin'
password_db_2 = 'admin'

common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
version_db2 = common_2.version()


print("details...", version_db2)


uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})


db_1_leads = models_1.execute_kw(db_1, uid_db1, password_db_1, 'sale.order', 'search_read', [[]], {'fields': ['id', 'name', 'user_id']})
total_count = 0
for lead in db_1_leads:
    print("..", lead)
    total_count += 1
    new_lead = models_2.execute_kw(db_2, uid_db2, password_db_2, 'sale.order', 'create', [lead])
print("Total Created..", total_count)