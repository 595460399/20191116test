from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from .libs.captcha.captcha import captcha
from django import http
from . import constants
import os
from meiduo_mall.utils.response_code import RETCODE
import random
from .libs.yuntongxun.ccp_sms import CCP
from celery_tasks.sms.tasks import send_sms_code
from django_redis import get_redis_connection


class SMSCodeView(View):
    def get(self, request, mobile):
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少参数')
        with open(os.path.join(
                r'C:\Users\59546\Desktop\python_work\gitee\dianshang_project\meiduo_project\meiduo_project\apps\verififcations\code',
                uuid), 'rb') as f:
            image_code_server = f.read()
        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '验证码失效'})
        image_code_server = image_code_server.decode()
        if image_code_server.lower() != image_code_client:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '验证码有误'})

        sms_code = '%06d' % random.randint(0, 999999)
        with open(os.path.join(
                r'C:\Users\59546\Desktop\python_work\gitee\dianshang_project\meiduo_project\meiduo_project\apps\verififcations\code',
                mobile), 'wb') as f:
            f.write(sms_code)
        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
        #                         constants.SEND_SMS_TEMPLATE_ID)

        send_sms_code.delay(mobile, sms_code)

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """

        # print(uuid)
        # print('开始生成')
        # 生成图片验证码
        text, image = captcha.generate_captcha()
        print(text)

        # 保存图片验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        return http.HttpResponse(image, content_type='image/jpg')
