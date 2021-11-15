from odoo import fields, models


class CoursesCourses(models.Model):
    _inherit = 'courses.courses'

    fee_configuration_id = fields.Many2one('fee.configuration',
                                           string='Fees Configuration')
    is_semester = fields.Boolean("Is Semester", default=False)
