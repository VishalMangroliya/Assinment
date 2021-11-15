from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WizMasterReport(models.TransientModel):
    _name = "wiz.master.report"
    _description = "Wizard Master Report"

    all_department = fields.Boolean(string='All Department', default=False)
    company_ids = fields.Many2many('res.company', 'rel_wiz_report_comp',
                                   string='Department')

    @api.model
    def check_current_year(self):
        '''Method to get default value of logged in Student'''
        res = self.env['academic.year'].search([('current', '=',
                                                 True)])
        return res.id

    academic_year_id = fields.Many2one('academic.year', required=True,
                                       string='Academic Year',
                                       default=check_current_year)

    def print_report(self):
        datas = {
            'ids': [],
            'model': 'fee.receipt',
            'form': self.read()[0]
        }
        return self.env.ref(
            'gvp_fee_receipt.action_master_report'
        ).report_action(self, data=datas)
