
import time
import base64
from datetime import date
from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import except_orm
from odoo.exceptions import ValidationError
from . import school

try:
    from odoo.tools import image_colorize, image_resize_image_big
except:
    image_colorize = False
    image_resize_image_big = False


class StudentStudent(models.Model):
    ''' Defining a student information '''
    _name = 'student.student'
    _description = 'Student Information'
    _sql_constraints = [
        ('enrolment_number', 'unique (enrolment_number)',
         'The Enrolment number is already exist!'),
    ]

    @api.depends('date_of_birth')
    def _compute_student_age(self):
        '''Method to calculate student age'''
        current_dt = date.today()
        for rec in self:
            if rec.date_of_birth:
                start = rec.date_of_birth
                age_calc = ((current_dt - start).days / 365)
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc

    @api.constrains('date_of_birth')
    def check_age(self):
        '''Method to check age should be greater than 5'''
        current_dt = date.today()
        if self.date_of_birth:
            start = self.date_of_birth
            age_calc = ((current_dt - start).days / 365)
            # Check if age less than 5 years
            if age_calc < 5:
                raise ValidationError(_('''Age of student should be greater
                than 5 years!'''))

    @api.model
    def create(self, vals):
        '''Method to create user when student is created'''
        if vals.get('pid', _('New')) == _('New'):
            vals['pid'] = self.env['ir.sequence'
                                   ].next_by_code('student.student'
                                                  ) or _('New')
        if vals.get('pid', False):
            vals['login'] = vals['pid']
            vals['password'] = vals['pid']
        else:
            raise except_orm(_('Error!'),
                             _('''PID not valid
                                 so record will not be saved.'''))
        if vals.get('company_id', False):
            company_vals = {'company_ids': [(4, vals.get('company_id'))]}
            vals.update(company_vals)
        if vals.get('email'):
            school.emailvalidation(vals.get('email'))
        res = super(StudentStudent, self).create(vals)
        # Assign group to student based on condition
        emp_grp = self.env.ref('base.group_user')
        if res.state == 'draft':
            admission_group = self.env.ref(
                'gvp_students_admission.group_is_admission')
            new_grp_list = [admission_group.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, new_grp_list)]})
        elif res.state == 'done':
            done_student = self.env.ref(
                'gvp_students_admission.group_school_student')
            group_list = [done_student.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, group_list)]})
        return res

    @api.model
    def _default_image(self):
        '''Method to get default Image'''
        image_path = get_module_resource('hr', 'static/src/img',
                                         'default_image.png')
        return tools.image_resize_image_big(base64.b64encode(
            open(image_path, 'rb').read()))

    @api.depends('state')
    def _compute_teacher_user(self):
        for rec in self:
            if rec.state == 'done':
                teacher = self.env.user.has_group(
                    "gvp_students_admission.group_professor")
                if teacher:
                    rec.teachr_user_grp = True

    @api.model
    def check_current_year(self):
        '''Method to get default value of logged in Student'''
        res = self.env['academic.year'].search([('current', '=',
                                                 True)])
        if not res:
            raise ValidationError(_('''There is no current Academic Year
                                    defined!Please contact to Administrator!'''
                                    ))
        return res.id

    family_con_ids = fields.One2many('student.family.contact',
                                     'family_contact_id',
                                     'Family Contact Detail',
                                     states={'done': [('readonly', True)]})
    user_id = fields.Many2one('res.users', 'User ID', ondelete="cascade",
                              required=True, delegate=True)
    student_name = fields.Char('Student Name', related='user_id.name',
                               store=True, readonly=True)
    pid = fields.Char('Student ID', required=True,
                      default=lambda self: _('New'),
                      help='Personal Identification Number')
    contact_phone = fields.Char('Phone no.')
    contact_mobile = fields.Char('Mobile no')
    enrolment_number = fields.Char('Enrolment Number')
    photo = fields.Binary('Photo', default=_default_image)
    year = fields.Many2one('academic.year', 'Academic Year', readonly=True,
                           default=check_current_year)
    cast_id = fields.Many2one('student.cast', 'Religion/Caste')
    relation = fields.Many2one('student.relation.master', 'Relation')

    admission_date = fields.Date('Admission Date', default=date.today())
    middle = fields.Char('Middle Name', required=True,
                         states={'done': [('readonly', True)]})
    last = fields.Char('Surname', required=True,
                       states={'done': [('readonly', True)]})
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              'Gender', states={'done': [('readonly', True)]})
    date_of_birth = fields.Date('BirthDate', required=True,
                                states={'done': [('readonly', True)]})
    age = fields.Integer(compute='_compute_student_age', string='Age',
                         readonly=True)
    maritual_status = fields.Selection([('unmarried', 'Unmarried'),
                                        ('married', 'Married')],
                                       'Marital Status',
                                       states={'done': [('readonly', True)]})
    reference_ids = fields.One2many('student.reference', 'reference_id',
                                    'References',
                                    states={'done': [('readonly', True)]})
    doctor = fields.Char('Doctor Name', states={'done': [('readonly', True)]})
    designation = fields.Char('Designation')
    doctor_phone = fields.Char('Contact No.')
    blood_group = fields.Char('Blood Group')
    height = fields.Float('Height', help="Hieght in C.M")
    weight = fields.Float('Weight', help="Weight in K.G")
    eye = fields.Boolean('Eyes')
    ear = fields.Boolean('Ears')
    nose_throat = fields.Boolean('Nose & Throat')
    respiratory = fields.Boolean('Respiratory')
    cardiovascular = fields.Boolean('Cardiovascular')
    neurological = fields.Boolean('Neurological')
    muskoskeletal = fields.Boolean('Musculoskeletal')
    dermatological = fields.Boolean('Dermatological')
    blood_pressure = fields.Boolean('Blood Pressure')
    remark = fields.Text('Remark', states={'done': [('readonly', True)]})
    company_id = fields.Many2one('res.company', string='Department', required=True,
                                 default=lambda self: self.env.user.company_id)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('terminate', 'Terminate'),
                              ('detained', 'Detained'),
                              ('alumni', 'Alumni'),
                              ('finish', 'Finish')],
                             'Status', readonly=True, default="draft")
    certificate_ids = fields.One2many('student.certificate', 'student_id',
                                      'Certificate')
    description = fields.One2many('student.description', 'des_id',
                                  'Description')
    award_list = fields.One2many('student.award', 'award_list_id',
                                 'Award List')
    stu_name = fields.Char('First Name', related='user_id.name',
                           readonly=True)
    Acadamic_year = fields.Char('Year', related='year.name',
                                help='Academic Year', readonly=True)
    terminate_reason = fields.Text('Reason')
    active = fields.Boolean(default=True)
    teachr_user_grp = fields.Boolean("Teacher Group",
                                     compute="_compute_teacher_user")
    courses_id = fields.Many2one('courses.courses', string='Courses',
                                 required=True)
    semester = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
                                 ('4', '4'), ('5', '5'), ('6', '6')],
                                string='Semester')
    library_acco_number = fields.Char("Account number for library")

    @api.multi
    def set_to_draft(self):
        '''Method to change state to draft'''
        self.state = 'draft'

    @api.multi
    def set_alumni(self):
        '''Method to change state to alumni'''
        student_user = self.env['res.users']
        for rec in self:
            rec.state = 'alumni'
            user = student_user.search([('id', '=',
                                         rec.user_id.id)])
            rec.active = False
            if user:
                user.active = False

    @api.multi
    def set_done(self):
        '''Method to change state to done'''
        self.state = 'done'

    @api.multi
    def admission_draft(self):
        '''Set the state to draft'''
        self.state = 'draft'

    @api.multi
    def set_terminate(self):
        self.state = 'terminate'

    def detain_admission(self):
        for rec in self:
            rec.state = 'detained'

    def admission_done(self):
        '''Method to confirm admission'''
        ir_sequence = self.env['ir.sequence']
        for rec in self:
            if rec.admission_date:
                rec.state = 'done'
                return True
            rec.write({'state': 'done',
                       'admission_date': time.strftime('%Y-%m-%d'),
                       })
        return True

    def semester_move(self):
        context = self._context
        rec_id = self.browse(context.get('rec_id'))
        if context.get('state_done'):
            rec_id.state = 'detained'
        else:
            rec_id.state = 'done'