{
    'name': 'GVP Fee Receipt',
    'version': '12.0.1.0.0',
    'summary': ' Fee Receipt',
    'sequence': 16,
    'category': 'GVP Account',
    'author': 'Gujarat Vidyapith, Sadra',
    'website': 'http://www.gujaratvidyapith.org',
    'depends': ['gvp_students_admission', 'web_digital_sign',
                'prt_report_attachment_preview'],
    'data': ['security/fee_receipt_security.xml',
             'security/ir.model.access.csv',
             'views/fee_configuration_view.xml',
             'views/fee_receipt_view.xml',
             'views/fee_department_view.xml',
             'views/fee_head_view.xml',
             'views/courses_view.xml',
             'data/ir_sequence_data.xml',
             'wizard/wiz_master_report_views.xml',
             'report/fee_receipt_report.xml',
             'report/fee_receipt_template.xml',
             'report/fees_report_template.xml',
             'report/master_report_template.xml',
             'views/menu.xml',
             ],
    'installable': True,
}
