# -*- coding: utf-8 -*-
{
    'name': "SCM ABC Sheet 2",

    'summary': """
        SCM ABC Sheet 2""",

    'description': """
        SCM ABC Sheet 2.
    """,

    'author': "WISE",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase','sale', 'report_xlsx'],

    # always loaded
    'data': [
        'security/scm_security.xml',
        'security/ir.model.access.csv',
        'views/config.xml',
        'views/raw.xml',
        'reports/report_raw_xlsx.xml',
        'views/scm_menu.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
