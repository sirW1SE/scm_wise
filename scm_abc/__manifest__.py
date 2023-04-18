<<<<<<< HEAD
# -*- coding: utf-8 -*-
{
    'name': "SCM ABC Report",

    'summary': """
        SCM ABC Report""",

    'description': """
        SCM ABC Report.
    """,

    'author': "Divo",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase','sale','report_xlsx'],

    # always loaded
    'data': [
        'security/scm_security.xml',
        'security/ir.model.access.csv',
        'views/config.xml',
        'views/distribution.xml',
        'views/masterlist_mc.xml',
        'reports/report_distribution_xlsx.xml',
        'views/scm_menu.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
=======
# -*- coding: utf-8 -*-
{
    'name': "SCM Report",

    'summary': """
        SCM Report""",

    'description': """
        SCM Report.
    """,

    'author': "Divo",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase','sale','report_xlsx'],

    # always loaded
    'data': [
        'security/scm_security.xml',
        'security/ir.model.access.csv',
        'views/config.xml',
        'views/distribution.xml',
        'views/masterlist_mc.xml',
        'views/masterlist_mc_data.xml',
        'views/distribution_data.xml',
        'views/area_code.xml',
        'views/product_ranking_matrix.xml',
        'reports/report_distribution_xlsx.xml',
        'views/scm_menu.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
>>>>>>> 291cf88f137f7da43aafb1270b86f6565dba0dbc
