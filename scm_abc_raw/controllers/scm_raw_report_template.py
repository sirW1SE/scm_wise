import psycopg2
from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter
from odoo import models, fields, api


class ScmABCExcelReportController(http.Controller):
    @http.route([
        '/scm_abc_raw/get_raw_excel_report/<model("scm.raw"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_raw_excel_report(self, wizard=None, **args):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('ABC Sheet 2 Report' + '.xlsx'))
            ]
        )

        # create workbook object from xlsxwriter library
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # create some style to set up the font type, the font size, the border, and the aligment
        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 14, 'bold': True, 'align': 'center'})
        header_style = workbook.add_format(
            {'font_name': 'Times', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center'})
        text_style = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'left'})
        number_style = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'right'})

        # loop all selected user/salesperson


        # create worksheet/tab per salesperson
        sheet = workbook.add_worksheet('Sheet 2 ' + str(wizard.end_date))
        # set the orientation to landscape
        sheet.set_landscape()
        # set up the paper size, 9 means A4
        sheet.set_paper(9)
        # set up the margin in inch
        sheet.set_margins(0.5, 0.5, 0.5, 0.5)

        # set up the column width
        sheet.set_column('A:H', 30)



        # the report title
        # merge the A1 to E1 cell and apply the style font size : 14, font weight : bold
        sheet.merge_range('A1:H1', 'As of ' + str(wizard.end_date), title_style)

        # table title
        sheet.write(1, 0, 'Raw Description', header_style)
        sheet.write(1, 1, 'Brand', header_style)
        sheet.write(1, 2, 'Cost', header_style)
        sheet.write(1, 3, 'Model', header_style)
        sheet.write(1, 4, 'Branch', header_style)
        sheet.write(1, 5, 'Last 30D Sale per branch', header_style)
        sheet.write(1, 6, 'Last 60D Sale per branch', header_style)
        sheet.write(1, 7, 'Last 90D Sale per branch ', header_style)


        row = 2
        number = 1

        conn = request.env['scm.config'].scm_conn()
        cur = conn.cursor()

        companies = '(1,2)'
        date_to = wizard.end_date

        sql_str = '''SELECT c.name as raw_desc, c.brand, c.model, e.name as branch,
                            COUNT(CASE WHEN (date(b.date_order) >= (date('%s') - interval '30 days') 
                            AND date(b.date_order) <= '%s') THEN a.product_id end) as ms_a,
                            COUNT(CASE WHEN (date(b.date_order) >= (date('%s') - interval '60 days') 
                            AND date(b.date_order) <= '%s') THEN a.product_id end) as ms_b,
                            COUNT(CASE WHEN (date(b.date_order) >= (date('%s') - interval '90 days') 
                            AND date(b.date_order) <= '%s') THEN a.product_id end) as ms_c
                            FROM ((sale_order_line a FULL JOIN sale_order b ON a.order_id = b.id) 
                            FULL JOIN (product_template c FULL JOIN product_product d 
                            ON c.id = d.product_tmpl_id) ON a.product_id = d.id), stock_warehouse e 
                            WHERE a.company_id IN (1,2) AND b.state IN ('sale','done')
                            AND b.warehouse_id = e.id AND c.type = 'product' AND c.tracking = 'serial'
                            AND b.date_order BETWEEN (date('%s') - interval '90 days') 
                            AND ('%s') AND b.partner_id NOT IN (1,8,9)  
                            GROUP BY c.name, c.brand, c.model, e.name
                            ORDER by c.name
                ''' % (date_to, date_to, date_to, date_to, date_to, date_to, date_to, date_to)


        cur.execute(sql_str)

        # display the PostgreSQL database server version
        raw = cur.fetchall()
        for data in raw:
            print(data)
            # the report content
            sheet.write(row, 0, data[0], text_style)
            sheet.write(row, 1, data[1], text_style)
            sheet.write(row, 2, '', text_style)
            sheet.write(row, 3, data[2], text_style)
            sheet.write(row, 4, data[3], text_style)
            sheet.write(row, 5, data[4], number_style)
            sheet.write(row, 6, data[5], number_style)
            sheet.write(row, 7, data[6], number_style)



            row += 1
            number += 1


        # return the excel file as a response, so the browser can download it
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        cur.close()
        return response




        # SELECT a.name as raw, a.price_subtotal, b.name as sale_order, 
        #                     c.name as raw_desc, c.brand, e.name as branch, 
        #                     date(b.date_order) as date_of_sale, f.value_float, g.quantity
        #                     FROM ((sale_order_line a FULL JOIN sale_order b ON a.order_id = b.id) 
        #                     FULL JOIN (product_template c FULL JOIN product_product d 
        #                     ON c.id = d.product_tmpl_id) ON a.product_id = d.id) 
        #                     FULL JOIN ir_property f ON f.res_id = 'product.product,' || d.id, 
        #                     stock_warehouse e, stock_quant g WHERE a.company_id IN %s AND a.state = 'sale'
        #                     AND date(b.date_order) >= '%s' AND date(b.date_order) <= '%s'
        #                     AND b.warehouse_id = e.id AND a.company_id = f.company_id
        #                     AND a.product_id = g.product_id AND g.quantity >= 0 AND g.company_id IN (1,2)
        #                     AND f.res_id = 'product.product,' || g.product_id
        #                     AND e.lot_stock_id = g.location_id
        #                     ORDER BY c.name
