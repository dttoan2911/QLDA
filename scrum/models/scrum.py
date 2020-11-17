from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ScrumProject(models.Model):
    _inherit = 'project.project'
<<<<<<< HEAD
    is_scrum = fields.Boolean()
    # sprint_count = fields.Integer(compute='_compute_sprint_count')
    # def _compute_sprint_count(self):
    #     count =0
    #     for project in self:
    #         count +=1
    #     project.sprint_count = count
=======
    # _rec_name = 'sp_name'

    is_scrum = fields.Boolean()
    sprint_count = fields.Integer(compute='_compute_sprint_count')


    def _compute_sprint_count(self):
        count =0
        for project in self:
            count +=1
        project.sprint_count = count
#   Một Project có ít nhất 0 hoặc 1 product backlog

>>>>>>> 18c72a686dfd0e83f96c78fc1848b7f5217745a0
class ProductBacklog(models.Model):
    _name = 'product.backlog'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Product Backlog Items(PBIs)"
<<<<<<< HEAD
    _order = 'priority desc'
    # Thuộc tính bảng Product Backlog
    name = fields.Char(string="#",required=True,copy=False,readonly=True,index=True,default=lambda self:_('New'))
    name_backlog = fields.Char(string="Tên Product Backlog",required=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done')
    ],default="draft",string="Trạng thái",track_visibility='always')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
    ],default='0', index=True, string="Ưu tiên")
    description = fields.Text(string="Mô tả")
    storypoint = fields.Integer(string="Story Point")
    attachment = fields.Binary(string="Đính kèm tệp",attachment=True)
    # Mối quan hệ cha con với Sprint
    sprint_id = fields.Many2one('sprint.sprint',ondelete="set null")
    # ID tự động tăng và cộng chuỗi
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('product.backlog.name') or _('New')
=======

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
>>>>>>> 18c72a686dfd0e83f96c78fc1848b7f5217745a0
        result = super(ProductBacklog,self).create(vals)
        return result
class Sprint(models.Model):
    _name = 'sprint.sprint'
    _description = "Sprint"
    _inherit = ['mail.thread','mail.activity.mixin']
<<<<<<< HEAD
    # Thuộc tính bảng Sprint
    name = fields.Char(string="Sprint Name",required=True,copy=False,readonly=True,index=True,default=lambda self:_('New'))
    sprint_goal = fields.Text(string="Sprint Goal")
    define_of_done = fields.Text(string="Define of done")
    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")
    # Mối quan hệ là con của cha product backlog
    sprint_backlog_ids = fields.One2many('product.backlog','sprint_id',string="Backlogs")
    # Thuộc tính cho phương thức
    backlog_count = fields.Integer(string="Backlog Count",compute='get_backlog_count')
    def open_sprint_backlogs(self):
        return{
            'name': _('Backlogs'),
            'domain': [('sprint_id','=',self.id)],
            'view_type': 'form',
            'res_model': 'product.backlog',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
    # Những constraint ràng buộc
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sprint.sprint.name') or _('New')
=======

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
>>>>>>> 18c72a686dfd0e83f96c78fc1848b7f5217745a0
        result = super(Sprint,self).create(vals)
        return result
    @api.constrains('start_date')
    def _timechk(self):
        for sprint in self.filtered('start_date'):
            today = fields.Date.today()
            flag = today - sprint.start_date
            if(flag.days>0):
                raise ValidationError(_('Ngày bắt đầu phải trước hôm nay'))
    @api.constrains('end_date')
    def _timecheck(self):
        for sprint in self.filtered('end_date'):
            flag = sprint.end_date - sprint.start_date
            if(flag.days<0):
                raise ValidationError(_('Ngày kết thúc không được nhỏ hơn ngày bắt đầu'))
            elif(flag.days>28):
                raise ValidationError(_('Thời hạn sprint không được vượt quá 4 tuần'))
    def get_backlog_count(self):
        count = self.env['product.backlog'].search_count([('sprint_id','=',self.id)])
        self.backlog_count = count
# from odoo.exceptions import UserError
# class ProductBacklog(models.Model):
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
