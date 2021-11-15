from odoo import fields, models


class FeeDepartment(models.Model):
    _name = "fee.department"
    _description = 'Fee Department Information'

    sequence = fields.Integer(string='Sequence', default=1)
    name = fields.Char(string='Name', required='1')
    sequence_id = fields.Many2one('ir.sequence',
                                  string='Sequence', required='1')
    is_student = fields.Boolean(string='Is Student', default=False)
    fee_head_ids = fields.One2many('fee.head', 'fee_department_id',
                                   string='Head Name')
    user_ids = fields.Many2many(
        'res.users', string='Users',
        domain=lambda self: [('id', 'in', self.env.ref(
            'gvp_fee_receipt.group_gvp_account').users.ids)])
