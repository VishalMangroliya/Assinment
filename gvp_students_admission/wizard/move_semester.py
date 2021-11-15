
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MoveSemester(models.TransientModel):
    _name = 'move.semester'
    _description = "Move Semester"

    status = fields.Selection([('regular', 'Regular'), ('detained', 'Detained')],
                              default='regular')
    courses_id = fields.Many2one('courses.courses', string='Courses')
    semester = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
                                 ('4', '4'), ('5', '5'), ('6', '6')],
                                string='Semester', default='1')
    move_semester = fields.Selection([('2', '2'), ('3', '3'),
                                      ('4', '4'), ('5', '5'), ('6', '6'),
                                      ('finish', 'Finish')],
                                     string='Move Semester', default='2')
    student_ids = fields.Many2many('student.student', 'move_sem_student_rel',
                                   string='Student')

    @api.onchange('status', 'semester', 'courses_id')
    def _on_change_status(self):
        for rec_move in self:
            rec_move.student_ids = False
            if rec_move.status and rec_move.semester and rec_move.courses_id:
                stu_domain = [('courses_id', '=', rec_move.courses_id.id),
                              ('semester', '=', self.semester)]
                if rec_move.status == 'regular':
                    stu_domain.append(('state', '=', 'done'))
                else:
                    stu_domain.append(('state', '=', 'detained'))
                student_ids = self.env['student.student'].search(stu_domain)
                if student_ids:
                    rec_move.student_ids = [(6, 0, student_ids.ids)]

    @api.multi
    def move_start(self):
        '''Code for moving student to next semester'''
        if self.semester == self.move_semester:
            raise ValidationError(_("Semester and next semester both are same!"))
        if self.student_ids:
            move_stu = {}
            student_ids = self.env['student.student']
            for rec in self.student_ids.filtered(lambda rec: rec.state == 'done'):
                student_ids |= rec
            if self.move_semester == 'finish':
                move_stu.update({'state': 'finish'})
            else:
                move_stu.update({'semester': self.move_semester})
            student_ids.write(move_stu)
            return {
                'name': _('Student'),
                'type': 'ir.actions.act_window',
                'views': [(self.env.ref('gvp_students_admission.student_student_kanban_view').id, 'kanban'),
                          (self.env.ref('gvp_students_admission.view_student_student_form_1').id, 'form')],
                'view_mode': 'kanban,form',
                'res_model': 'student.student',
                'context': {'search_default_courses': '1'},
                'domain': [('state', '=', 'done')],
            }
            # raise ValidationError(_("The students were moved to the next semester successfully."))
        else:
            raise ValidationError(_("Student records not founds! "))
