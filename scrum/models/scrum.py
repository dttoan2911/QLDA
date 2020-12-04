from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ScrumProject(models.Model):
    _name = 'scrum.project'
    # Phương thức đếm các Product Backlog
    def get_product_backlog_count(self):
        count = self.env['product.backlog'].search_count([('project_id','=',self.id)])
        self.backlog_count = count
    # Phương thức trỏ đến các Product Backlog của một Project
    def open_product_backlog(self):
        return{
            'name': _('Product Backlog'),
            'domain': [('project_id','=',self.id)],
            'view_type': 'form',
            'res_model': 'product.backlog',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
    # Phương thức đếm các Sprint
    def get_sprint_count(self):
        count = self.env['sprint.sprint'].search_count([('project_id','=',self.id)])
        self.sprint_count = count
    # Phương thức trỏ đến các Sprint của một Project
    def open_sprint(self):
        return{
            'name': _('Sprint'),
            'domain': [('project_id','=',self.id)],
            'view_type': 'form',
            'res_model': 'sprint.sprint',
            'view_id': False,
            'view_mode': 'tree,form,graph',
            'type': 'ir.actions.act_window',
        }
    # Phương thức lấy Task của một Project
    def test_get_task(self):
        for rec in self:
            print("Tasks")
            table_pb = self.env['product.backlog']
            get_pb = table_pb.search([('project_id','=',self.id)])
            get_task = get_pb.mapped('task_id')
            self.task_count = len(get_task)
    # Phương thức trỏ đến các Task của một Project
    # BUG: CHỈ LẤY ĐƯỢC TASK CỦA MỘT PRODUCT BACKLOG
    def open_task(self):
        return{
            'name': _('Task'),
            'domain':[('backlog_id','=',self.id)],
            'view_type': 'form',
            'res_model': 'scrum.task',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
    # Thuộc tính bảng Scrum Project
    name=fields.Char(string="Tên Project",required="True")
    is_scrum = fields.Boolean(string="Template Scrum",default=True)
    # Thuộc tính đếm các Product Backlog
    backlog_count = fields.Integer(string="Product Backlog Count",compute='get_product_backlog_count')
    # Thuộc tính đếm các Sprint
    sprint_count = fields.Integer(string="Sprint Count",compute='get_sprint_count')
    # Thuộc tính đếm các Task của một Project
    task_count = fields.Integer(string="Task Count",compute='test_get_task')
    # Thuộc tính lấy các Product Backlog của riêng Project
    project_backlog_ids = fields.One2many('product.backlog','project_id',string="Product Backlog")
    # Thuộc tính lấy các Sprint của riêng Project
    project_sprint_ids = fields.One2many('sprint.sprint','project_id',string="Sprint")
class ProductBacklog(models.Model):
    _name = 'product.backlog'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Product Backlog Items(PBIs)"
    _order = 'priority desc'
    # Phương thức đếm các Task trong Product Backlog
    def get_task_count(self):
        count = self.env['scrum.task'].search_count([('backlog_id','=',self.id)])
        self.task_count = count
    # Phương thức trỏ đến các Task của một Product Backlog
    def open_product_backlog_tasks(self):
        return{
            'name': _('Tasks'),
            'domain': [('backlog_id','=',self.id)],
            'view_type': 'form',
            'res_model': 'scrum.task',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'context':{'default_backlog_id':self.id},
        }
    # Phương thức tự động tạo chuỗi và tăng ID cho thuộc tính name
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('product.backlog.name') or _('New')
        result = super(ProductBacklog,self).create(vals)
        return result
    # Phương thức xóa tạm tất cả Task trong một Product Backlog
    def delete_all_task(self):
        for rec in self:
            rec.task_id = [(5,0,0)]
    # Phương thức hiển thị tất cả cột state trong Kanban
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]
    # @api.onchange('project_id')
    # def set_project_id(self):
    #     for rec in self:
    #         if rec.project_id:
    #             rec.project_id = rec.project_id.name
    # Phương thức kiểm tra trạng thái product backlog
    @api.onchange('state')
    def _status_check(self):
        for rec in self:
            if rec.state == 'done':
                for task in rec.task_id:
                    if task.state != 'done':
                        raise UserError("Các task phải ở trạng thái done")
    # Phương thức kiểm tra không cho thay đổi pb với sprint đang chạy
    @api.onchange('sprint_id')
    def sprint_check(self):
        if self._origin.sprint_id.state == 'start':
            raise UserError("%s đã ở trạng thái start, không thể thay đổi" %(str(self._origin.sprint_id.name)))
    # Thuộc tính bảng Product Backlog
    name = fields.Char(string="Số thứ tự",required=True,copy=False,readonly=True,index=True,default=lambda self:_('New'))
    name_backlog = fields.Char(string="Tên Product Backlog",required=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirm'),
        ('done','Done')
    ],default="draft",string="Trạng thái",group_expand='_expand_states',track_visibility='always',index=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
    ],default='0', index=True, string="Ưu tiên")
    description = fields.Text(string="Mô tả")
    storypoint = fields.Integer(string="Story Point")
    attachment = fields.Binary(string="Đính kèm tệp",attachment=True)
    # Thuộc tính đếm các Task trong Product Backlog
    task_count = fields.Integer(string="Đếm Task",compute='get_task_count')
    # Quan hệ cha con với bảng Sprint: Một Product Backlog chỉ được nằm trong một Sprint
    sprint_id = fields.Many2one('sprint.sprint',string="Sprint ID",ondelete="set null")
    # Quan hệ cha con với bảng Scrum Task: Một Product Backlog có ít nhất 0 hoặc nhiều Task
    task_id = fields.One2many('scrum.task','backlog_id',string="Task ID")
    # Quan hệ một một với bảng Scrum Project: Một Product Backlog chỉ được nằm trong một Scrum Project
    project_id = fields.Many2one('scrum.project',string="Tên Dự Án")
class Sprint(models.Model):
    _name = 'sprint.sprint'
    _description = "Sprint"
    _inherit = ['mail.thread','mail.activity.mixin']
    # Phương thức đếm các Product Backlog trong Sprint
    def get_backlog_count(self):
        count = self.env['product.backlog'].search_count([('sprint_id','=',self.id)])
        self.backlog_count = count
    # Phương thức trỏ đến các Product Backlog của một Sprint
    def open_sprint_backlogs(self):
        return{
            'name': _('Backlogs'),
            'domain': [('sprint_id','=',self.id)],
            'view_type': 'form',
            'res_model': 'product.backlog',
            'view_id': False,
            'view_mode': 'kanban,form',
            'type': 'ir.actions.act_window',
        }
    # Phương thức tự động tạo chuỗi và tăng ID cho thuộc tính name
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sprint.sprint.name') or _('New')
        result = super(Sprint,self).create(vals)
        return result
    # Phương thức kiểm tra start date
    @api.constrains('start_date')
    def _timechk(self):
        for sprint in self.filtered('start_date'):
            today = fields.Date.today()
            flag = today - sprint.start_date
            if(flag.days>0):
                raise ValidationError(_('Ngày bắt đầu phải trước hôm nay'))
    # Phương thức kiểm tra end date
    @api.constrains('end_date')
    def _timecheck(self):
        for sprint in self.filtered('end_date'):
            flag = sprint.end_date - sprint.start_date
            if(flag.days<0):
                raise ValidationError(_('Ngày kết thúc không được nhỏ hơn ngày bắt đầu'))
            elif(flag.days>28):
                raise ValidationError(_('Thời hạn sprint không được vượt quá 4 tuần'))
    # Phương thức chuyển đổi trạng thái thành start
    def action_start_sprint(self):
        count = self.env['product.backlog'].search_count([('sprint_id','=',self.id)])
        for rec in self:
            if rec.sprint_goal == False:
                raise UserError("Bạn phải nhập sprint goal")
            elif count == 0:
                raise UserError("Không có Product Backlog nào")
            else:
                for pb in rec.sprint_backlog_ids:
                    if not pb.task_id:
                        raise UserError("Product Backlog này không có task nào")
                    else:
                        rec.state = 'start'
    # Phương thức chuyển đổi trạng thái thành complete
    def action_complete_sprint(self):
        count = self.env['product.backlog'].search_count([('sprint_id','=',self.id)])
        if count ==0:
            raise UserError("Không có backlog nào")
        else: 
            for rec in self:
                for backlog in rec.sprint_backlog_ids:
                    if backlog.state != 'done':
                        raise UserError("Các backlog phải ở trạng thái done")
                    else:   
                        rec.state = 'complete'
                        return {
                        'effect':{
                            'fadeout':'slow',
                            'message':'Sprint Complete',
                            'type':'rainbow_man',
                            }
                        }
    # Phương thức kiểm tra không được xóa Sprint khi đang ở trạng thái Start
    def unlink(self):
        for rec in self:
            if rec.state == 'start':
                raise UserError(_("Bạn không được phép xóa Sprint này vì đang ở trạng thái 'Start'"))
        return super(Sprint, self).unlink()
    # Phương thức chỉ lấy các Product Backlog thuộc cùng một Project với Sprint
    @api.onchange('project_id')
    def onchange_project_id(self):
        for rec in self:
            return {'domain':{'sprint_backlog_ids':[('project_id','=',rec.project_id.id),('sprint_id','=',False)]}}
    # Thuộc tính bảng Sprint
    name = fields.Char(string="Tên Sprint",required=True,copy=False,readonly=True,index=True,default=lambda self:_('New'))
    sprint_goal = fields.Text(string="Sprint Goal")
    define_of_done = fields.Text(string="Define of done")
    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")
    state = fields.Selection([
        ('draft','Draft'),
        ('start','Start'),
        ('complete','Complete')
    ],default="draft",string="Trạng thái",track_visibility='always')
    review_note=fields.Text(string="Review Note")
    retrospective_note=fields.Text(string="Retrospective Note")
    # Thuộc tính đếm các Product Backlog trong một Sprint
    backlog_count = fields.Integer(string="Đếm Product Backlog",compute='get_backlog_count')
    # Quan hệ cha con với bảng Product Backlog: Một Sprint sẽ có ít nhất 0 hoặc nhiều Product Backlog
    sprint_backlog_ids = fields.One2many('product.backlog','sprint_id',string="Product Backlog")
    # Quan hệ cha con với bảng Scrum Team: Chưa rõ phần này
    user_sprint_id = fields.Many2one('scrum.team',string="Người tạo")
    # Quan hệ cha con với bảng Project
    project_id = fields.Many2one('scrum.project',string="Dự Án")
class ScrumTeam(models.Model):
    _name='scrum.team'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description="Những người dùng tham gia Scrum Project"
    # Thuộc tính bảng Scrum Team
    name = fields.Char(string="Tên Scrum Team",required="True")
    # Quan hệ cha con với bảng Users: Chưa rõ phần này
    user_id = fields.Many2one('res.users',string="Tên tài khoản",track_visibility='always')
class Task(models.Model):
    _name = 'scrum.task'
    _description = "Các Task nằm trong một Product Backlog"
    # Phương thức hiển thị tất cả cột state trong Kanban
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]
    # Thuộc tính bảng Task
    name =fields.Char(string="Tên Task",required=True)
    state = fields.Selection([
        ('todo','To do'),
        ('inprogress','In Progress'),
        ('done','Done')
    ],default="todo",string="Trạng thái",group_expand='_expand_states',track_visibility='always')
    # Quan hệ cha con với bảng Product Backlog: Một Task chỉ được nằm trong một Product Backlog
    backlog_id = fields.Many2one('product.backlog',string="Product Backlog ID")
    # Quan hệ cha con với bảng Users: Chưa rõ phần này
    user_id = fields.Many2one('scrum.team',string="Tên trong Scrum",track_visibility='always')
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
    # sprint_count = fields.Integer(compute='_compute_sprint_count')
    # def _compute_sprint_count(self):
    #     count =0
    #     for project in self:
    #         count +=1
    #     project.sprint_count = count
    # Mối quan hệ 1-1 với Scrum Project
    # Phương thức lấy tự động ID Project
    # @api.model
    # def create(self,vals):
    #     res = super(ProductBacklog, self).create(vals)
    #     self.env['scrum.project'].search([('project_id', '=', False)]).write({'project_id':res.id})
    #     return res
    # project_id = fields.Many2one('scrum.project',string="Tên Project",index=True,ondelete="cascade",default=create)