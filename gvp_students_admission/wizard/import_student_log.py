from odoo import fields, models


class ImportStudentsLog(models.TransientModel):
    _name = 'import.students.log'
    _description = "Import Students Log"

    name = fields.Char('Name')
    enrolment_number = fields.Char('Enrolment Number')
    operation = fields.Selection([('create', 'Create'),
                                  ('update', 'Update')],
                                 string='Operation')
    status = fields.Selection([('done', 'Done'),
                               ('issue', 'Issue')],
                              string='Status')
    courses_id = fields.Many2one('courses.courses', string='Courses')
    log_msg = fields.Text("Log Messages")
