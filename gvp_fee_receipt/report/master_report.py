from odoo import api, models


class MasterReport(models.AbstractModel):
    _name = 'report.gvp_fee_receipt.master_report'
    _description = 'Master Report'

    def _getreport_data(self, rec_id):
        fee_dict = {}
        dept_dict = {}
        de_dict = {}
        year_list = ['fy', 'sy', 'ty']
        semester_list = ['1', '2', '3', '4', '5', '6']
        field_list = ['education_fee', 'semester_fee', 'medical_fee',
                      'internal_fee', 'game_fee', 'identity_fee',
                      'library_fee', 'name_registration_fee', 'reading_fee',
                      'practical_fee', 'exam_fee', 'department_reserve_fee',
                      'student_board_fee', 'computer_education_fee',
                      'hostel_management_fee', 'student_quarterly',
                      'text_literature_fee', 'essay_fee', 'other_fee',
                      'total_amount']
        wiz_id = self.env['wiz.master.report'].browse(rec_id)
        fee_receipt_obj = self.env['fee.receipt']
        if wiz_id.all_department:
            fee_receip_ids = fee_receipt_obj.search(
                [('academic_year_id', '=', wiz_id.academic_year_id.id),
                 ('is_student', '=', True), ('rec_state', '=', 'done')])
        else:
            fee_receip_ids = fee_receipt_obj.search(
                [('academic_year_id', '=', wiz_id.academic_year_id.id),
                 ('is_student', '=', True), ('rec_state', '=', 'done'),
                 ('company_id', 'in', wiz_id.company_ids.ids)])
        department_list = [rec.company_id for rec in fee_receip_ids]
        for dep_id in list(set(department_list)):
            cour_dict = {}
            courses_ids = self.env['courses.courses'].search(
                [('company_id', '=', dep_id.id)])
            for cour_id in courses_ids:
                year_dict = {}
                if not cour_id.is_semester:
                    for year_rec in year_list:
                        fee_rec = fee_receip_ids.filtered(
                            lambda x: x.company_id == dep_id and
                            x.courses_id == cour_id and
                            x.edu_year == year_rec)
                        if len(fee_rec.ids):
                            year_dict.update(
                                {year_rec: {'total_std': len(fee_rec.ids)}})
                            for field_rec in field_list:
                                total_sum = sum(fee_rec.mapped(field_rec))
                                year_dict.get(year_rec).update(
                                    {field_rec: total_sum})
                else:
                    for semester_rec in semester_list:
                        fee_rec = fee_receip_ids.filtered(
                            lambda x: x.company_id == dep_id and
                            x.courses_id == cour_id and
                            x.semester == semester_rec)
                        if len(fee_rec.ids):
                            year_dict.update({semester_rec: {
                                'total_std': len(fee_rec.ids)}})
                            for field_rec in field_list:
                                total_sum = sum(fee_rec.mapped(field_rec))
                                year_dict.get(semester_rec).update(
                                    {field_rec: total_sum})
                if year_dict:
                    cour_dict.update({cour_id: year_dict})
            de_dict.update({dep_id: cour_dict})
            rec_ids = fee_receip_ids.filtered(lambda x: x.company_id == dep_id)
            dept_dict.update({dep_id: {'total_std': len(rec_ids.ids)}})
            for field_name in field_list:
                if rec_ids:
                    total_sum = sum(rec_ids.mapped(field_name))
                    dept_dict.get(dep_id).update({field_name: total_sum})
            fee_dict.update({dep_id: cour_dict})
        return {'subject': de_dict, 'depat': dept_dict}

    @api.model
    def _get_report_values(self, docids, data=None):
        return {'doc_ids': docids,
                'doc_model': 'fee.receipt',
                'data': data,
                'getreport_data': self._getreport_data(data.get(
                    'form').get('id')),
                }

