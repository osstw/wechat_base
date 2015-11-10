from openerp import models, fields, api, exceptions, _


class User(models.Model):
    _inherit = "res.users"

    @api.multi
    def test_weixin(self):
        self.ensure_one()
        data = dict()
        data["text"] = {"value": "hello!", "color": "#173177"}
        self.partner_id.send_template_message("Ix5Z3oyiXtxjO81oqdpq3F47mngysQWjRW1vaGNDlPo", data)
        return True

    @api.multi
    def action_get_qrcode(self):
        return self.partner_id.action_get_qrcode()

    @api.multi
    def bind_wechat_user(self):
        self.ensure_one()
        wizard = self.env["wechat_base.bind_wizard"].create(
            {"wechat_qrcode_url": "yyy", "wechat_qrcode": self.wechat_qrcode})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wechat_base.bind_wizard',
            'res_id': wizard.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def go_to_binding_center(self):
        return {
            "type": "ir.actions.act_url",
            "url": "http://www.qq.com",
            "target": "new",
        }
