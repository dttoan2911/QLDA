# -*- coding: utf-8 -*-
{
    'name': "Ứng dụng Quản trị Dự án",

    'summary': """
        Ứng dụng Quản trị Dự án theo mô hình Agile & Scrum
    """,

    'description': """
        Được phân tích, thiết kế và thực hiện trong vòng 1 tháng
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': 'Pre-alpha',

    # any module necessary for this one to work correctly
    'depends': ['base','project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/scrum.xml',
        'views/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
}