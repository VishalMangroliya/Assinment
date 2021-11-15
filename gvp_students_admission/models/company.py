from odoo import fields,  models


class Company(models.Model):
    _inherit = "res.company"

    courses_count = fields.Integer(string='Courses Count',
                                   compute='_get_courses')

    def _get_courses(self):
        for comp in self:
            comp.courses_count = self.env['courses.courses'].search_count(
                [('company_id', '=', comp.id)])

    def action_courses_rec(self):
        courses_ids = self.env['courses.courses'].search(
            [('company_id', '=', self.id)])
        return {
            'name': _('Courses'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'courses.courses',
            'domain': [('id', 'in', courses_ids.ids)],
            'type': 'ir.actions.act_window'
        }
