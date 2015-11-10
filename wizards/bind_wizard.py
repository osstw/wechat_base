# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import exceptions
from wechat_sdk import WechatBasic
import __builtin__
from .. import tool
import base64  # file encode
import urllib2  # file download from url

import logging

_logger = logging.getLogger(__name__)


class TodoWizard(models.TransientModel):
    _name = 'wechat_base.bind_wizard'

    wechat_qrcode_url = fields.Char()  #compute="_compute_qrcode_url"
    wechat_qrcode = fields.Binary()

    @api.multi
    def _compute_qrcode_url(self):
        self.ensure_one()
        self.wechat_qrcode_url = "xxx"

    @api.multi
    def _compute_qrcode(self):
        self.ensure_one()
        tool.token_tool.refresh()
        wechat = WechatBasic(token=__builtin__.token["access_token"], appid=__builtin__.appid,
                             appsecret=__builtin__.appsecret)
        data = dict()
        # data["expire_seconds"] = 604800
        data["action_name"] = "QR_LIMIT_SCENE"
        data["action_info"] = {"scene": {"scene_id": self.id}}
        ret = wechat.create_qrcode(data)
        # ret = wechat.show_qrcode()
        self.weixin_qrcode = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" % ret["ticket"]

    @api.multi
    def action_get_qrcode(self):
        self.ensure_one()
        tool.token_tool.refresh()
        wechat = WechatBasic(token=__builtin__.token["access_token"], appid=__builtin__.appid,
                             appsecret=__builtin__.appsecret)
        data = dict()
        # data["expire_seconds"] = 604800
        data["action_name"] = "QR_LIMIT_SCENE"
        data["action_info"] = {"scene": {"scene_id": self.id}}
        ret = wechat.create_qrcode(data)
        # ret = wechat.show_qrcode()
        self.weixin_qrcode_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" % ret["ticket"]
        self.weixin_qrcode = base64.encodestring(urllib2.urlopen(self.weixin_qrcode_url).read())
        return True


