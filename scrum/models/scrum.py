from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ScrumProject(models.Model):
    _name = 'scrum.project'
    # _inherit = 'project.project'
    _description = "Scrum Project"
    # _rec_name = 'sp_name'

    name = fields.Char(string="Tên Project",required=True)
#   Một Project có ít nhất 0 hoặc 1 product backlog

class ProductBacklog(models.Model):
    _name = 'product.backlog'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Product Backlog Items(PBIs)"
    _rec_name = 't_name'

    t_id = fields.Char(string="Task ID",required=True,copy=False,readonly=True,index=True,default=lambda self:_('Task'))
    t_name = fields.Char(string="Tên Task",required=True,track_visibility='always')
    t_workflow = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done')
    ],default="draft",string="Tình trạng Task",track_visibility='always')
    t_description = fields.Text(string="Mô tả",track_visibility='always')
    t_storypoint = fields.Integer(string="Story Point",track_visibility='always')
    t_attachment = fields.Binary(string="Đính kèm tệp",attachment=True,track_visibility='always')

    # Rắc rối: nối bảng. Có cách nào hay hơn không ta?
    s_ids = fields.Many2one('sprint.sprint',string="Sprint")
    
    t_ids = fields.Many2one('product.backlog',string="Taks")

    @api.model
    def create(self,vals):
        if vals.get('t_id',_('Task')) == _('Task'):
            vals['t_id'] = self.env['ir.sequence'].next_by_code('product.backlog.id') or _('Task')
        result = super(ProductBacklog,self).create(vals)
        return result

class Sprint(models.Model):
    _name = 'sprint.sprint'
    _description = "Sprint"
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 's_id'

    s_id = fields.Char(string="Sprint Name",required=True,copy=False,readonly=True,index=True,default=lambda self:_('Sprint'))
    s_sprint_goal = fields.Char(string="Sprint Goal")
    s_define_of_done = fields.Char(string="Define of done")
    s_start_date = fields.Date(string="Ngày bắt đầu")
    s_end_date = fields.Date(string="Ngày kết thúc")

    # Sprint quan hệ(1,n) - quan hệ(1,1) Product Backlog
    t_name = fields.One2many('product.backlog','t_ids',string="Task", required=True)
    @api.constrains('s_end_date')
    def _timecheck(self):
        for sprint in self.filtered('s_end_date'):
            today = fields.Date.today()
            flag = sprint.s_end_date - sprint.s_start_date
            if(flag.days<0):
                raise ValidationError(_('Ngày kết thúc không được nhỏ hơn ngày bắt đầu'))
            elif(flag.days>28):
                raise ValidationError(_('Thời hạn sprint không được vượt quá 4 tuần'))
            elif((today-sprint.s_start_date).days<0):
                raise ValidationError(_('Ngày bắt đầu không được trước hôm nay'))




    @api.model
    def create(self,vals):
        if vals.get('s_id',_('Sprint')) == _('Sprint'):
            vals['s_id'] = self.env['ir.sequence'].next_by_code('sprint.sprint.id') or _('Sprint')
        result = super(Sprint,self).create(vals)
        return result
#   Một Product Backlog có ít nhất và nhiều nhất 1 trong Project
#   Một Product Backlog có ít nhất 1 và nhiều nhất n Task
#   Bản thân bảng Product Backlog là bảng Task nên không có thuộc tính gì riêng mà thay vào đó là nơi chứa thuộc tính của Task

# class ProjectInherit(models.Model):
#     _inherit='project.project'

#     item_name = fields.Char(string="Product Backlog")

# class ProductBacklog(models.Model):
#     _name = 'product.backlog'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = "Product Backlog Items(PBIs)"
#     _rec_name = "item_name"

#     item_name = fields.Char(string="Tên Item",required=True)
#     item_priority =fields.Integer(string="Độ ưu tiên")
#     item_description = fields.Text(string="Mô tả")
#     item_attached_file = fields.Binary(string="Đính kèm tệp")
#     sprint = fields.Char(string="Sprint ID", required=True,copy=False,readonly=True,index=True,default=lambda self:_('Sprint'))

#     # Tạo ID tự động tăng
#     @api.model
#     def create(self,vals):
#         if vals.get('sprint',_('Sprint')) == _('Sprint'):
#             vals['sprint'] = self.env['ir.sequence'].next_by_code('product.backlog.sprint') or _('Sprint')
#         result = super(ProductBacklog,self).create(vals)
#         return result

    



# from odoo.exceptions import UserError

# class ScrumProject(models.Model):
#     _name = 'project.project.scrum'
#     # _inherit = 'project.project'
#     _description = "Scrum Project"

#     name = fields.Char(string="Tên Project",required=True)


# class ProductBacklog(models.Model):
#     _name = 'project.project.backlog'
#     # _inherit = 'project.project'
#     _description = "Product Backlog items(PBIs)"
    
#     name = fields.Char(string="Tên Item",required=True)
#     description = fields.Text(string="Mô tả Item")

    # _sql_constraints = [
    #     ('nho_hon_0', 'check(value<0)', 'khong duoc nhap gia tri lon hon 0'),
    # ]


    # @api.constrains('name')
    # def _check_name(self):

    #     action=self.env['ir.actions.act_window'].create({
    #         'name': '',
    #         'view_ids': [
    #             (5, 0 , 0),
    #             (0, 0, {
    #                 'view_mode': 'kanban',
    #             })
    #         ]
    #     })

    #     self.env['ir.actions.view'].create({
    #         'view_mode': 'kanban',
    #         'act_action_id': action.id
    #     })

    #     for backlog in self:

    # def unlink(self):
    #     for backlog in self:
    #         if backlog.name == 'root':
    #             raise UserError(_("Ban ko duoc phep xoa backlog ten 'root'"))
    #     return super(Backlog, self).unlink()