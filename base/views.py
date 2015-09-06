# -*- coding:utf-8 -*-
import hashlib
import datetime
import os
import random
import StringIO
from PIL import ImageFont, ImageDraw, Image
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from web.const import msgconst

authcode_font = os.path.join(os.path.dirname(__file__), 'msyh.ttc')


class LoginVars():
    def __init__(self):
        self.username = ''
        self.password = ''
        self.auth_code = ''
        self.errmsg = ''

    def post_to_obj(self, request):
        self.username = request.POST.get('username')
        self.password = request.POST.get('password')
        self.auth_code = request.POST.get('auth_code')


def login(request):
    try:
        # if request.user.is_authenticated():
        #     return HttpResponseRedirect(reverse('base:home'))
        lv = LoginVars()
        if request.method == 'POST':
            lv.post_to_obj(request)
           # if not lv.auth_code or lv.auth_code != request.session.get('auth_code', ''):
          #      lv.errmsg = u'验证码错误'
           #     return render_to_response('base/login.html', lv.__dict__, context_instance=RequestContext(request))
            if lv.username and lv.password:
                user = authenticate(username=lv.username, password=lv.password)
                if user and user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('base:home'))
            lv.errmsg = u'用户名或密码错误'
        return render_to_response('base/login.html', lv.__dict__, context_instance=RequestContext(request))
    except Exception, e:
        return render_to_response('503.html', {'errmsg': unicode(e).encode('utf-8')})


@login_required
def home(request):
    return render_to_response('base/home.html', {'user': request.user})


def auth_code(request):
    try:
        mp = hashlib.md5()
        mp.update(str(datetime.datetime.now()) + str(random.random()))
        mp_src = mp.hexdigest()
        rand_str = mp_src[0:4]
        font = ImageFont.truetype(authcode_font, 25)
        width = 75
        height = 30
        im = Image.new('RGB', (width, height), '#%s' % mp_src[-7:-1])
        draw = ImageDraw.Draw(im)
        draw.line(
            (random.randint(0, width), random.randint(0, height), random.randint(0, width), random.randint(0, height)))
        draw.line(
            (random.randint(0, width), random.randint(0, height), random.randint(0, width), random.randint(0, height)))
        draw.line(
            (random.randint(0, width), random.randint(0, height), random.randint(0, width), random.randint(0, height)))
        draw.line(
            (random.randint(0, width), random.randint(0, height), random.randint(0, width), random.randint(0, height)))
        draw.line(
            (random.randint(0, width), random.randint(0, height), random.randint(0, width), random.randint(0, height)))
        draw.text((7, 0), rand_str, font=font)
        del draw
        buffer = StringIO.StringIO()
        im.save(buffer, 'jpeg')
        httpResponse = HttpResponse(content=buffer.getvalue(), content_type="image/jpeg")
        request.session['auth_code'] = rand_str
        return httpResponse
    except Exception, e:
        print e


def logout_view(request):
    user = request.user
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponse("<b>%s</b> logged out! <br/><a href='/login'>Re-login</a>" % user)



