from odoo import api, fields,  models, _
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _inherit = "hr.employee"

    is_professor = fields.Boolean(string='Is Professor')
    courses_subjects_ids = fields.One2many('courses.subjects', 'employee_id',
                                           string='Courses And Subjects')

    @api.model
    def create(self, vals):
        teacher_grp_id = self.env.ref(
            'gvp_students_admission.group_professor')
        user_base_grp = self.env.ref('base.group_user')
        contact_create = self.env.ref('base.group_partner_manager')
        teacher_group_ids = [user_base_grp.id, teacher_grp_id.id,
                             contact_create.id]
        res_user_id = self.env['res.users'].create(
            {'image': vals.get('image'),
             'name': vals.get('name'),
             'login': vals.get('work_email'),
             'password': vals.get('work_email'),
             'email': vals.get('work_email'),
             'mobile': vals.get('mobile_phone'),
             'phone': vals.get('work_phone'),
             'company_id': vals.get('company_id'),
             'company_ids': [(6, 0, [vals.get('company_id')])],
             'groups_id': [(6, 0, teacher_group_ids)], })
        if res_user_id:
            vals.update({'user_id': res_user_id.id})
        return super(Employee, self).create(vals)


class CoursesSubjects(models.Model):
    _name = 'courses.subjects'
    _description = 'Courses And Subjects Information'
    _sql_constraints = [
        ('courses_employee_uniq', 'unique (courses_id,employee_id)',
         'The courses must be unique per professor!')
    ]

    subject_ids = fields.Many2many('subject.subject', 'subject_courses_rel',
                                   'teacher_id', 'subject_id',
                                   'Course-Subjects', required=True)
    courses_id = fields.Many2one('courses.courses', "Courses", required=True)
    employee_id = fields.Many2one('hr.employee', string='Professor')

    @api.onchange('courses_id')
    def _onchange_courses_idr(self):
        self.subject_ids = False
        return {'domain': {'subject_ids': [
            ('id', 'in', self.courses_id.subject_ids.ids)]}}

    @api.model
    def create(self, vals):
        subject_obj = self.env['subject.subject']
        for subject in vals.get('subject_ids')[0][2]:
            subject_id = subject_obj.browse(subject)
            # if subject_id.employee_id:
            #     professor_name = self.env['hr.employee'].browse(
            #         vals.get('employee_id')).name
            #     raise ValidationError(_("%s subject is already add in "
            #                             "%s!" % (subject_id.name,
            #                                      professor_name)))
            # else:
            subject_id.employee_id = vals.get('employee_id')
        return super(CoursesSubjects, self).create(vals)

    def write(self, vals):
        subject_obj = self.env['subject.subject']
        subject_ids = subject_obj.browse(vals.get('subject_ids')[0][2])
        for subject_id in self.subject_ids - subject_ids:
            subject_id.employee_id = False
        for subject_id in subject_ids - self.subject_ids:
            # if subject_id.employee_id:
            #     raise ValidationError(_("%s subject is already add in "
            #                             "%s!" % (subject_id.name,
            #                                      self.employee_id.name)))
            # else:
            subject_id.employee_id = self.employee_id.id
        return super(CoursesSubjects, self).write(vals)
