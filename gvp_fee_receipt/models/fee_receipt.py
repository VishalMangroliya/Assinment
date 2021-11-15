from datetime import datetime, date
from odoo import api, fields, models, _
from num2words import num2words
from odoo.exceptions import ValidationError


class FeeReceipt(models.Model):
    _name = 'fee.receipt'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'fee.configuration']
    _description = 'Fees Receipt Information'

    name = fields.Char(string='Name', default='New', copy=False)
    courses_id = fields.Many2one('courses.courses', string='Courses')
    fee_department_id = fields.Many2one('fee.department', string='Department')
    fee_head_id = fields.Many2one('fee.head', string='Head')
    is_student = fields.Boolean(string='Is Student',
                                related='fee_department_id.is_student')
    pay_name = fields.Char(string='Name')
    note = fields.Text(string='Description')
    receive_date = fields.Date('Date', default=fields.Date.context_today,
                               required='1')
    total_amount = fields.Monetary(string='Total Amount')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    is_current_year = fields.Boolean(related='academic_year_id.current',
                                     string='Current Year')
    rec_state = fields.Selection([('done', 'Done'), ('cancel', 'Canceled')],
                                 default='done', string='Receipt Sate',
                                 copy=False)
    received_option = fields.Selection([('cash', 'Cash'),
                                        ('check', 'Check'),
                                        ('other', 'Other')],
                                       default='cash',
                                       string='Fee Received Option')
    bank_name = fields.Char(string='Bank Name')
    check_number = fields.Char(string='Check Number', copy=False)
    other = fields.Char(string='Other')
    is_sevak_santan = fields.Boolean(string='Is Sevak Santan', default=False,
                                     copy=False)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='courses_id.company_id')

    @api.model
    def check_current_year(self):
        '''Method to get default value of logged in Student'''
        res = self.env['academic.year'].search([('current', '=',
                                                 True)])
        if not res:
            raise ValidationError(_("There is no current Academic Year "
                                    "defined!Please contact to "
                                    "Administrator!"))
        return res.id

    academic_year_id = fields.Many2one('academic.year',
                                       string='Academic Year',
                                       default=check_current_year)

    @api.constrains('receive_date')
    def _check_python_code(self):
        if self.receive_date > date.today():
            raise ValidationError(_("Future date is not valid, Select "
                                    "another date!"))

    @api.model
    def create(self, vals):
        res = super(FeeReceipt, self).create(vals)
        recipt_code = self.env['ir.sequence'].next_by_code(
            res.fee_department_id.sequence_id.code).split('/')
        recipt_code[1] = res.academic_year_id.name
        res.name = '/'.join(recipt_code)
        return res

    def write(self, vals):
        if vals.get('rec_state') == 'cancel':
            self.message_post(
                body="Receipt is Canceled, Date:" +
                     datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        if vals.get('pay_name'):
            self.message_post(
                body="<b>Updated Name: </b>" +
                     self.pay_name +
                     "<b> <i class='fa fa-long-arrow-right' "
                     "aria-hidden='true'/> </b>"
                     "" + vals.get('pay_name'))
        if vals.get('total_amount'):
            self.message_post(
                body="<b>Updated Amount: </b>" +
                     str(self.total_amount) +
                     "<b> <i class='fa fa-long-arrow-right' "
                     "aria-hidden='true'/> </b>"
                     "" + str(vals.get('total_amount')))
        return super(FeeReceipt, self).write(vals)

    @api.multi
    def amount_to_text(self, amount):
        return num2words(amount)

    @api.onchange('fee_department_id')
    def _onchange_fee_department_id(self):
        self.courses_id = self.edu_year = False

    @api.onchange('courses_id', 'edu_year', 'semester', 'is_sevak_santan')
    def _onchange_courses(self):
        self.student_id = False
        fee_conf_id = fee_conf_obj = self.env['fee.configuration']
        self.is_semester = self.courses_id.is_semester
        amount = 0.0
        if self.courses_id and self.edu_year and not self.is_semester:
            fee_conf_id = fee_conf_obj.search(
                [('courses_ids', 'in', self.courses_id.id),
                 ('edu_year', '=', self.edu_year)], limit=1)
        elif self.courses_id and self.semester and self.is_semester:
            fee_conf_id = fee_conf_obj.search(
                [('courses_ids', 'in', self.courses_id.id),
                 ('semester', '=', self.semester)], limit=1)
        if self.is_sevak_santan:
            self.education_fee = 0.0
            amount += 0.0
        else:
            self.education_fee = fee_conf_id.education_fee
            amount += fee_conf_id.education_fee
        self.medical_fee = fee_conf_id.medical_fee
        amount += fee_conf_id.medical_fee
        self.identity_fee = fee_conf_id.identity_fee
        amount += fee_conf_id.identity_fee
        self.name_registration_fee = fee_conf_id.name_registration_fee
        amount += fee_conf_id.name_registration_fee
        self.practical_fee = fee_conf_id.practical_fee
        amount += fee_conf_id.practical_fee
        self.department_reserve_fee =\
            fee_conf_id.department_reserve_fee
        amount += fee_conf_id.department_reserve_fee
        self.computer_education_fee =\
            fee_conf_id.computer_education_fee
        amount += fee_conf_id.computer_education_fee
        self.student_quarterly = fee_conf_id.student_quarterly
        amount += fee_conf_id.student_quarterly
        self.semester_fee = fee_conf_id.semester_fee
        amount += fee_conf_id.semester_fee
        self.internal_fee = fee_conf_id.internal_fee
        amount += fee_conf_id.internal_fee
        self.library_fee = fee_conf_id.library_fee
        amount += fee_conf_id.library_fee
        self.reading_fee = fee_conf_id.reading_fee
        amount += fee_conf_id.reading_fee
        self.exam_fee = fee_conf_id.exam_fee
        amount += fee_conf_id.exam_fee
        self.student_board_fee = fee_conf_id.student_board_fee
        amount += fee_conf_id.student_board_fee
        self.hostel_management_fee = fee_conf_id.hostel_management_fee
        amount += fee_conf_id.hostel_management_fee
        self.game_fee = fee_conf_id.game_fee
        amount += fee_conf_id.game_fee
        self.text_literature_fee = fee_conf_id.text_literature_fee
        amount += fee_conf_id.text_literature_fee
        self.essay_fee = fee_conf_id.essay_fee
        amount += fee_conf_id.essay_fee
        self.other_fee = fee_conf_id.other_fee
        amount += fee_conf_id.other_fee
        self.total_amount = amount

    @api.onchange('is_semester')
    def _onchange_is_semester(self):
        if self.is_semester:
            self.edu_year = False
        else:
            self.semester = False
