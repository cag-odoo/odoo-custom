# -*- coding: utf-8 -*-

{
    'name': "Odoo Explorer",
    'description': """
       A tool for Odoo developer
    """,
    'author': 'Gautier Casabona',
    'category': "Tools",
    'version': "1.0",
    'installable': True,
    'sequence': 500,

    'author': "Odoo S.A.",
    'website': "http://www.odoo.com",

    'depends': ['web'],

    'data': [
        'views/ir_model.xml',
        'views/ir_model_fields.xml',

        'wizard/model_pathfinder_wizard.xml',

        'views/menu_items.xml',
    ],
}
