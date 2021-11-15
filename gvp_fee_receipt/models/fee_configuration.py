from odoo import api, fields, models


class FeeConfiguration(models.Model):
    _name = 'fee.configuration'
    _description = 'Fees Configuration Information'

    name = fields.Char(string='Name')
    courses_ids = fields.Many2many('courses.courses',
                                   'courses_confi_rel',
                                   string='Courses', copy=False)
    edu_year = fields.Selection([('fy', '1 Year'), ('sy', '2 Year'),
                                 ('ty', '3 Year')], string='Education Year',
                                copy=False)
    education_fee = fields.Float('Education Fee')
    semester_fee = fields.Float('Semester Fee')
    medical_fee = fields.Float('Medical Fee')
    internal_fee = fields.Float('Internal Fee')
    game_fee = fields.Float('Game Fee')
    identity_fee = fields.Float('Identity Fee')
    library_fee = fields.Float('Library Fee')
    name_registration_fee = fields.Float('Name Registration Fee')
    reading_fee = fields.Float('Reading Fee')
    practical_fee = fields.Float('Practical Fee')
    exam_fee = fields.Float('Exam Fee')
    department_reserve_fee = fields.Float('Department Reserve Fee')
    student_board_fee = fields.Float('Student Board Fee')
    computer_education_fee = fields.Float('Computer Education Fee')
    hostel_management_fee = fields.Float('Hostel Management Fee')
    student_quarterly = fields.Float('Student Quarterly')
    text_literature_fee = fields.Float('Pathya Chahitya Fee')
    essay_fee = fields.Float('Nibandh Fee')
    other_fee = fields.Float('Other Fee')
    is_semester = fields.Boolean("Is Semester", default=False, copy=False)
    semester = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
                                 ('4', '4'), ('5', '5'), ('6', '6')],
                                string='Semester', copy=False)
    total = fields.Float('Total Fees', readonly='1', copy=False)

    @api.onchange('is_semester')
    def _onchange_is_semester(self):
        self.courses_ids = False
        if self.is_semester:
            self.edu_year = False
        else:
            self.semester = False
        return {'domain': {
            'courses_ids': [('is_semester', '=', self.is_semester)]}}

    @api.onchange('education_fee', 'semester_fee', 'medical_fee',
                  'internal_fee', 'game_fee', 'identity_fee', 'library_fee',
                  'name_registration_fee', 'reading_fee', 'practical_fee',
                  'exam_fee', 'department_reserve_fee', 'student_board_fee',
                  'computer_education_fee', 'hostel_management_fee',
                  'student_quarterly', 'text_literature_fee',
                  'essay_fee', 'other_fee', '')
    def _onchange_fees(self):
        self.total = self.education_fee + self.semester_fee + \
                     self.medical_fee + self.internal_fee + self.game_fee + \
                     self.identity_fee + self.library_fee + \
                     self.name_registration_fee + self.reading_fee + \
                     self.practical_fee + self.exam_fee + \
                     self.department_reserve_fee + self.student_board_fee + \
                     self.computer_education_fee + self.student_quarterly + \
                     self.hostel_management_fee + self.essay_fee + \
                     self.text_literature_fee + self.other_fee
