from odoo import models, fields, api, _

class CreateProductBacklog(models.TransientModel):
    _name='create.product.backlog'
    # Phương thức Create Product Backlog
    def create_product_backlog(self):
        vals={
            'project_id':self.project_id.id,
            'name_backlog':self.name_backlog
        }
        self.env['product.backlog'].create(vals)
    # Thuộc tính bảng Create Product Backlog
    project_id = fields.Many2one('scrum.project',string="Project")
    name_backlog = fields.Char(string="Name",required=True)