from odoo import models, fields, api, _

class CreateScrumProject(models.TransientModel):
    _name = 'create.scrum.project'
    # Phương thức Create Scrum Project
    def create_scrum_project(self):
        vals={
            'name':self.name
        }
        self.env['scrum.project'].create(vals)
    # Thuộc tính bảng Scrum Project
    name=fields.Char("Tên Project",required="True")
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
class CreateSprint(models.TransientModel):
    _name='create.sprint'
    # Phương thức Create Sprint
    def create_sprint(self):
        vals = self.env['sprint.sprint'].create({
            'project_id':self.project_id.id,
            'sprint_backlog_ids':[(6,0,self.sprint_backlog_ids.ids)]
        })
    # Phương thức chỉ lấy các Product Backlog thuộc cùng một Project với Sprint
    @api.onchange('project_id')
    def onchange_project_id(self):
        for rec in self:
            return {'domain':{'sprint_backlog_ids':[('project_id','=',rec.project_id.id),('sprint_id','=',False)]}}
    # Thuộc tính bảng Create Sprint
    project_id = fields.Many2one('scrum.project',string="Project")
    # Quan hệ cha con với bảng Product Backlog: Một Sprint sẽ có ít nhất 0 hoặc nhiều Product Backlog
    sprint_backlog_ids = fields.Many2many('product.backlog',string="Product Backlog")

    