from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ScrumProject(models.Model):
    _inherit = 'project.project'
    # _rec_name = 'sp_name'

    is_scrum = fields.Boolean()
    sprint_count = fields.Integer(compute='_compute_sprint_count')


    def _compute_sprint_count(self):
        count =0
        for project in self:
            count +=1
        project.sprint_count = count
#   Một Project có ít nhất 0 hoặc 1 product backlog

class ProductBacklog(models.Model):
    _name = 'product.backlog'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Product Backlog Items(PBIs)"
    _rec_name = 'name'
    _order = 'storypoint desc'

    id = fields.Char(string="Task ID",required=False,copy=False,readonly=True,index=True,default=lambda self:_('Task'))
    name = fields.Char(string="Tên Task",required=True,track_visibility='always')
    workflow = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done')
    ],default="draft",string="Tình trạng Task",track_visibility='always')
    description = fields.Text(string="Mô tả", default="Mô tả Task của bạn", required=True,track_visibility='always')
    storypoint = fields.Integer(string="StoryPoint",  track_visibility='always')
    attachment = fields.Binary(string="Đính kèm tệp",attachment=True, track_visibility='always')

    # Rắc rối: nối bảng. Có cách nào hay hơn không ta?
    sprint_id = fields.Many2one('sprint.sprint', ondelete="set null")



    @api.model
    def create(self,vals):
        if vals.get('id',_('Task')) == _('Task'):
            vals['id'] = self.env['ir.sequence'].next_by_code('product.backlog.id') or _('Task')
        result = super(ProductBacklog,self).create(vals)
        return result

class Sprint(models.Model):
    _name = 'sprint.sprint'
    _description = "Sprint"
    _inherit = ['mail.thread','mail.activity.mixin']

    iname = fields.Char(string="Sprint Name",required=True,copy=False,readonly=True,index=True,default=lambda self:_('Sprint'))
    sprint_goal = fields.Char(string="Sprint Goal",default="Sprint Goal của bạn",required=True)
    define_of_done = fields.Char(string="Define of done")
    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")
    sprint_backlog_ids = fields.One2many('product.backlog',  'sprint_id')

    # Sprint quan hệ(1,n) - quan hệ(1,1) Product Backlog
    sprint_list = fields.One2many('one.2.many','sprint_id',string="Sprint List")
    @api.constrains('end_date')
    def _timecheck(self):
        for sprint in self.filtered('end_date'):
            flag = sprint.end_date - sprint.start_date
            if(flag.days<0):
                raise ValidationError(_('Ngày kết thúc không được nhỏ hơn ngày bắt đầu'))
            elif(flag.days>28):
                raise ValidationError(_('Thời hạn sprint không được vượt quá 4 tuần'))
            
    @api.constrains('start_date')
    def _timechk(self):
        for sprint in self.filtered('start_date'):
            today = fields.Date.today()
            flag = today - sprint.start_date
            if(flag.days>0):
                raise ValidationError(_('Ngày bắt đầu phải trước hôm nay'))
    @api.model
    def create(self,vals):
        if vals.get('id',_('Sprint')) == _('Sprint'):
            vals['id'] = self.env['ir.sequence'].next_by_code('sprint.sprint.id') or _('Sprint')
        result = super(Sprint,self).create(vals)
        return result
    
class One2Many(models.Model):
    _name="one.2.many"
    _description = "One 2 Many"
    _rec_name = 'sprint_id'

    product_backlog_id = fields.Many2one('product.backlog',string="Task ID")
    sprint_id = fields.Many2one('sprint.sprint',string="Sprint ID")
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