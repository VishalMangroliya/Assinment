from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TimeTab(models.Model):
    _name = 'time.table'
    _description = 'Time Table Information'

    @api.model
    def check_current_year(self):
        res = self.env['academic.year'].search([('current', '=', True)])
        if not res:
            raise ValidationError(_('''There is no current 
            Academic Year defined!Please contact to Administrator!'''))
        return res.id

    name = fields.Char('Name', required=True)
    year = fields.Many2one('academic.year', 'Academic Year', readonly=True,
                           default=check_current_year)
    time_table_ids = fields.One2many('time.table.line', 'time_table_id',
                                     string='Time Table Line')


class TimeTableLine(models.Model):
    _name = 'time.table.line'
    _description = 'Time Table Line Information'

    start_time = fields.Float('Start Time', required=True)
    end_time = fields.Float('End Time', required=True)
    days = fields.Selection([
        ('monday', 'Monday'), ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'), ('thursday', 'Thursday'),
        ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')])
    time_table_id = fields.Many2one('time.table', string='Time Table')
    subject_ids = fields.One2many('subject.subject', 'time_table_line_id',
                                  string='Subjects')

