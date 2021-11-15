from odoo import api, models


class FeesReport(models.AbstractModel):
    _name = 'report.gvp_fee_receipt.fees_report'
    _description = 'Fees Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        recipt_dict = {}
        courses_dict = {}
        fee_receipt_ids = self.env['fee.receipt'].browse(docids)
        for rec_receipt in fee_receipt_ids.filtered(
                lambda x: x.edu_year and x.rec_state == 'done'):
            fee_receipt_list = fee_receipt_ids.filtered(
                lambda x: x.edu_year == rec_receipt.edu_year and
                x.rec_state == 'done')
            fee_receipt_year_list = [
                rec.courses_id.name for rec in fee_receipt_list]
            recipt_dict.update({rec_receipt.edu_year: fee_receipt_list})
            courses_dict.update({rec_receipt.edu_year: [
                ', '.join(set(fee_receipt_year_list)), True]})
        for rec_receipt in fee_receipt_ids.filtered(
                lambda x: x.semester and x.rec_state == 'done'):
            fee_receipt_list = fee_receipt_ids.filtered(
                lambda x: x.semester == rec_receipt.semester and
                x.rec_state == 'done')
            fee_receipt_year_list = [
                rec.courses_id.name for rec in fee_receipt_list]
            recipt_dict.update({rec_receipt.semester: fee_receipt_list})
            courses_dict.update({rec_receipt.semester: [
                ', '.join(set(fee_receipt_year_list)), False]})
        return {'doc_ids': docids,
                'doc_model': 'fee.receipt',
                'data': data,
                'fee_receipt_year_dist': courses_dict,
                'docs': recipt_dict,
                }
