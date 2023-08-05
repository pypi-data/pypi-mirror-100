# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Enrico Ganzaroli (enrico.gz@gmail.com)
# Copyright 2018 Ermanno Gnan (ermannognan@gmail.com)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# Copyright 2018-2019 Sergio Zanchetta (https://github.com/primes2h)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Imposta di bollo',
    'version': '12.0.1.1.4',
    'category': 'Localization/Italy',
    'summary': "Gestione automatica dell'imposta di bollo",
    'author': 'Ermanno Gnan, Sergio Corato, Enrico Ganzaroli, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'LGPL-3',
    'depends': [
        'product',
        'account',
    ],
    'data': [
        'data/data.xml',
        'views/invoice_view.xml',
        'views/product_view.xml',
        'views/company_view.xml',
    ],
    'installable': True,
}
