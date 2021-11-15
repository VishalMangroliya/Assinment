from odoo import fields, models


class FeeHead(models.Model):
    _name = "fee.head"
    _description = 'Fee Head Information'

    sequence = fields.Integer(string='Sequence', default=1)
    name = fields.Char(string='Head Name', required='1')
    fee_department_id = fields.Many2one('fee.department',
                                        string='Fee Department',
                                        required='1')
