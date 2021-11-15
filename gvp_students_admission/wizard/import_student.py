# importing csv module
from datetime import datetime
import csv
from odoo import api, fields, models, modules, _
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import ValidationError, Warning
import logging
from xlrd import open_workbook
from base64 import b64decode
_logger = logging.getLogger(__name__)
try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None


class WizImportStudents(models.TransientModel):
    _name = 'wiz.import.students'
    _description = "Import Students"

    upload = fields.Binary('Upload (.XLSX File)')
    filename = fields.Char('Filename')
    operation = fields.Selection([('create', 'Create'),
                                  ('update', 'Update')],
                                 string='Operation',
                                 default='create')
    courses_id = fields.Many2one('courses.courses', string='Courses')
    semester = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'),
                                 ('4', '4'), ('5', '5'), ('6', '6')],
                                string='Semester', default='1')

    def get_default_image(self):
        with open(modules.get_module_resource('gvp_students_admission', 'static/', 'sample.xlsx'),
                  'rb') as f:
            return base64.b64encode(f.read())

    sample_file = fields.Binary('Sample File', default=get_default_image)
    is_download = fields.Boolean('Download')
    sample = fields.Char('Sample File', default='Sample_file')

    def re_open_wizard(self):
        self.is_download = True
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.id,
            'target': 'new',
        }
    def read_csv_file(self):
        student_obj = self.env['student.student']
        in_count = self.env.ref('base.in').id
        student_list = []
        log_list = []
        if not self.upload:
            raise ValidationError(_('Please select .XLSX file !'))
        if not self.semester:
            raise ValidationError(_('Please select semester !'))
        if not self.courses_id:
            raise ValidationError(_('Please select courses !'))
        if not self.operation:
            raise ValidationError(_('Please select operation '
                                    '(Ex. Create or Update) !'))
        try:
            data_file = b64decode(self.upload)
            wb = open_workbook(file_contents=data_file)
        except:
            raise Warning(_("Please select valid .XLSX file!"))
        firstline = True
        for s in wb.sheets():
            for row in range(s.nrows):
                student_dict = {}
                error_msg = ''
                if firstline:
                    firstline = False
                    continue
                # data_row = []
                # for col in range(s.ncols):
                #     value = (s.cell(row, col).value)
                #     data_row.append(value)
                stu_list = (s.row(row))
                student_rec = student_obj.search([('enrolment_number', '=', stu_list[0].value),
                                                  ('semester', '=', self.semester),
                                                  ('courses_id', '=', self.courses_id.id),
                                                  ('state', '=', 'done')])
                if not stu_list[0].value:
                    error_msg += 'Enrolment number is not available\n'
                elif not stu_list[1].value or not stu_list[2].value or not stu_list[3].value:
                    error_msg += 'Name is not available\n'
                elif not stu_list[8].value:
                    error_msg += 'Date Of Birth is not available\n'
                elif stu_list:
                    try:
                        dob = datetime.strptime((stu_list[8]).value.replace(
                            '/', '-'), '%d-%m-%Y').strftime(DEFAULT_SERVER_DATE_FORMAT)
                        admi_date = datetime.strptime((stu_list[9]).value.replace(
                            '/', '-'), '%d-%m-%Y').strftime(DEFAULT_SERVER_DATE_FORMAT)
                        student_dict.update(
                            {'enrolment_number': stu_list[0].value,
                             'name': (stu_list[1].value).replace(' ', ''),
                             'middle': (stu_list[2].value).replace(' ', ''),
                             'last': (stu_list[3].value).replace(' ', ''),
                             'street': stu_list[4].value,
                             'state': 'done', 'zip': int(stu_list[6].value),
                             'city': (stu_list[5].value).replace(' ', ''),
                             'country_id': in_count,
                             'courses_id': self.courses_id.id,
                             'gender': (stu_list[7].value).replace(' ', ''),
                             'semester': self.semester,
                             'date_of_birth': dob or False,
                             'admission_date': admi_date or False})
                    except ValueError:
                        error_msg += 'ValueError! Please check the record\n'
                    except Exception as e:
                        error_msg += '' + e
                if student_rec and self.operation == 'create':
                    error_msg += 'Record is already exist\t'
                if not student_rec and self.operation == 'update':
                    error_msg += 'Record not exist\t'
                if self.operation == 'create' and not student_rec and student_dict:
                    student_list.append(student_dict)
                elif self.operation == 'update' and student_rec:
                    student_rec.write(student_dict)
                if error_msg:
                    log_list.append(
                        {'name': stu_list[1].value or '' + stu_list[2].value or '' +
                         stu_list[3].value or '',
                         'enrolment_number': stu_list[0].value,
                         'operation': self.operation, 'status': 'issue',
                         'courses_id': self.courses_id.id, 'log_msg': error_msg})
                else:
                    log_list.append(
                        {'name': stu_list[1].value or '' + stu_list[2].value or '' +
                                 stu_list[3].value or '',
                         'enrolment_number': stu_list[0].value,
                         'operation': self.operation, 'status': 'done',
                         'courses_id': self.courses_id.id, 'log_msg': 'Successfully.'})

        # csv file name
        # studend_list = []
        # in_count = self.env.ref('base.in').id
        # try:
        #     file = base64.b64decode(self.upload)
        #     file_string = file.decode('utf-8')
        #     file_string = file_string.split('\n')
        # except:
        #     raise Warning(_("Please Select .CSV!"))
        # firstline = True
        # for file_item in file_string:
        #     if firstline:
        #         firstline = False
        #         continue
        #     if file_item:
        #         stu_list = file_item.split('\t')
        #         studend_list.append({'name': stu_list[0], 'middle': stu_list[1],
        #         'last': stu_list[2],
        #         'street': stu_list[3],
        #         'state': 'done', 'zip': stu_list[5],
        #         'city': stu_list[4], 'country_id':in_count,
        #         'state_id': self.env.user.partner_id.country_id.id, 'courses_id': self.courses_id.id,
        #         'gender': stu_list[6], 'semester': '1', 'date_of_birth': str(stu_list[7]),
        #                              'admission_date': str(stu_list[8])})
        if student_list and self.operation == 'create':
            student_obj.create(student_list)
        if log_list:
            self.env['import.students.log'].create(log_list)
