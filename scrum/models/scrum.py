from odoo import models, fields, api, _

class ScrumProject(models.Model):
    _inherit = 'project.project'
    is_scrum = fields.Boolean(string="Template Scrum")
    # sprint_count = fields.Integer(compute='_compute_sprint_count')
    # def _compute_sprint_count(self):
    #     count =0
    #     for project in self:
    #         count +=1
    #     project.sprint_count = count
class ProductBacklog(models.Model):
    _name = 'product.backlog'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Product Backlog Items(PBIs)"
    _order = 'priority desc'
    # Thuộc tính bảng Product Backlog
    name = fields.Char(string="#",required=True,copy=False,readonly=True,index=True,default=lambda self:_('New'))
    name_backlog = fields.Char(string="Name",required=True)
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
    # Mối quan hệ cha con với Task
    backlog_id = fields.One2many('scrum.task','task_id',string="Tasks")
    # ID tự động tăng và cộng chuỗi
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('product.backlog.name') or _('New')
        result = super(ProductBacklog,self).create(vals)
        return result
class Sprint(models.Model):
    _name = 'sprint.sprint'
    _description = "Sprint"
    _inherit = ['mail.thread','mail.activity.mixin']
    # Thuộc tính bảng Sprint
    name = fields.Char(string="Sprint Name",required=True,copy=False,readonly=True,index=True,default=lambda self:_('New'))
    sprint_goal = fields.Text(string="Sprint Goal")
    define_of_done = fields.Text(string="Define of done")
    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")
    state = fields.Selection([
        ('draft','Draft'),
        ('start','Start'),
        ('complete','Complete')
    ],default="draft",string="Trạng thái",track_visibility='always')
    # Mối quan hệ là con của cha product backlog
    sprint_backlog_ids = fields.One2many('product.backlog','sprint_id',string="Backlogs")
    # Mối quan hệ là con của cha Scrum Team
    user_sprint_id = fields.Many2one('scrum.team',string="Người tạo")
    # user_id = fields.Many2one('res.users',string="PRO")
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
    def action_start_sprint(self):
        for rec in self:
            rec.state = 'start'
    def action_complete_sprint(self):
        for rec in self:
            rec.state = 'complete'
    def unlink(self):
        for rec in self:
            if rec.state == 'start':
                raise UserError(_("Bạn không được phép xóa Sprint này vì đang ở trạng thái 'Start'"))
        return super(Sprint, self).unlink()
class ScrumTeam(models.Model):
    _name='scrum.team'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description="Những người dùng tham gia Scrum Project"

    name = fields.Char(string="Name",required="True")
    user_id = fields.Many2one('res.users',string="Tên tài khoản",track_visibility='always')

class Task(models.Model):
    _name = 'scrum.task'
    _description = "Các Task nằm trong một Product Backlog"

    name =fields.Char(string="Tên Task",required=True)
    task_id = fields.Many2one('product.backlog',string="Task ID")
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