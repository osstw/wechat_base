from openerp import models, fields, api, _
from .. import tool
import base64
import urllib2
import threading


class Partner(models.Model):
    _inherit = "res.partner"

    wechat_qrcode_url = fields.Text()
    wechat_qrcode = fields.Binary()
    wechat_openID = fields.Char()

    @api.multi
    def action_get_qrcode(self):
        for partner in self:
            data = dict()
            data["action_name"] = "QR_LIMIT_SCENE"
            data["action_info"] = {"scene": {"scene_id": partner.id}}

            wechat = tool.token_tool.get_new_basic_wechat_client()
            ret = wechat.create_qrcode(data)
            url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" % ret["ticket"]

            partner.wechat_qrcode_url = url
            partner.wechat_qrcode = base64.encodestring(urllib2.urlopen(url).read())
        return True

    @api.multi
    def send_template_message(self, wechat_template_id, data, url='', topcolor='#FF0000'):
        for partner in self:
            def send_message(*args):
                wechat = tool.token_tool.get_new_wechat_client_with_token()
                wechat.send_template_message(*args)

            threaded_wechat_sending = threading.Thread(target=send_message, args=(
                partner.wechat_openID, wechat_template_id, data, url or '', topcolor or '#FF0000'))
            threaded_wechat_sending.start()

        return True
