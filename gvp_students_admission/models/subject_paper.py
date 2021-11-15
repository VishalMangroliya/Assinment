from odoo import fields, models


class SubjectPaper(models.Model):
    ''' Defining a Subject Paper information '''
    _name = 'subject.paper'
    _description = 'Subject Paper Information'

    name = fields.Char(string='Paper Name', required=True)
    paper = fields.Binary(string='Upload Paper', required=True)
    subject_id = fields.Many2one('subject.subject', string='Subject')
