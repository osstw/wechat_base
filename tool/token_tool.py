from wechat_sdk import WechatBasic
import time

wechat_appid = "wxf7b5bd13112fe9fc"
wechat_appsecret = "2d150d1243c72816c3d67645c39154b4"
cur_token = None


def token_refresh_decorator(wechat_function):
    def wrapper(*args, **kwargs):
        global cur_token
        if not cur_token or cur_token["access_token_expires_at"] - 60 < int(time.time()):
            wechat = WechatBasic(appid=wechat_appid, appsecret=wechat_appsecret)
            wechat.grant_token(True)
            cur_token = wechat.get_access_token()
        return wechat_function(*args, **kwargs)

    return wrapper


def get_new_basic_wechat_client():
    wechat = WechatBasic(appid=wechat_appid, appsecret=wechat_appsecret)
    return wechat


@token_refresh_decorator
def get_new_wechat_client_with_token():
    wechat = WechatBasic(appid=wechat_appid, appsecret=wechat_appsecret,
                         token=cur_token["access_token"])
    return wechat
