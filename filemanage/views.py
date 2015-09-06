# -*- coding: utf-8 -*-
import os
import urllib
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import time
from filemanage.models import LXFile
from web import settings
from web.const import msgconst


class Pager(object):
    def __init__(self, page_total, cur, total_record):
        self.total_page = page_total
        self.cur = cur
        self.total_record = total_record
        self.page_list = self._page_list()
        # self.url_name = url_name
        #self.page_urls = self._page_url()

    # def _get_url(self, page_index):
    # return reverse(self.url_name, args=[page_index])
    #
    # def _page_url(self):
    #     plist = self.page_list
    #     urls = dict()
    #     urls[1] = self._get_url(1)
    #     urls[self.total_page] = self._get_url(self.total_page)
    #     for p in plist:
    #         urls[p] = self._get_url(p)
    #     return urls

    def _page_list(self):
        sp = self.cur - 2 if self.cur > 2 else 1
        ep = self.cur + 7 if self.cur + 7 < self.total_page else self.total_page
        return range(sp, ep + 1)


class FileListVars():
    def __init__(self, sort):
        self.title = sort
        self.files = []
        self.sort = sort
        self.pager = None

    def convert_title(self):
        if str(self.title) == '1':
            self.title = u'报告列表'
        elif str(self.title) == '2':
            self.title = u'常用工具'


@login_required
def file_list(request, sort, page_index):
    try:
        page_index = int(page_index)
        page_size = int(request.GET.get('pagesize', 10))
        flv = FileListVars(sort)
        request.session.set_expiry(0)
        request.session['sort'] = sort
        flv.convert_title()
        all_count = LXFile.objects.count()
        if all_count > 0:
            page_count = (all_count / page_size) if all_count % page_size == 0 else (all_count / page_size + 1)
            if page_index > page_count:
                page_index = page_count
            si = (page_index - 1) * page_size
            ei = page_index * page_size
            flv.files = LXFile.objects.filter(sort=sort).order_by("-createtime")[si:ei]
            flv.pager = Pager(page_count, page_index, all_count)
        return render_to_response('filemanage/file_list.html', flv.__dict__, context_instance=RequestContext(request))
    except Exception, e:
        return render_to_response('503.html', {'errmsg': unicode(e).encode('utf-8')})


def _handle_upload_file(f, timestamp_filename):
    with open(os.path.join(settings.UPLOAD_FILE_PATH, timestamp_filename), 'wb') as u:
        for chunk in f.chunks():
            u.write(chunk)


@login_required
def upload_file(request):
    try:
        if request.method != 'POST':
            raise Exception(msgconst.request_method_invaild)
        sort = request.session.get('sort', None)
        if not sort:
            raise Exception(msgconst.session_overtime)
        remark = request.POST.get('remark', '')
        if len(request.FILES) == 1:
            timestamp_filename = os.path.join(settings.UPLOAD_FILE_PATH, str(time.time()).replace('.', ''))
            uf = request.FILES['uploadfile']
            fname, fext = os.path.splitext(uf.name)
            if fext.lower() in settings.ALLOW_FILE_SORT:
                LXFile.objects.create(
                    name=uf.name,
                    path=timestamp_filename,
                    uploader=request.user,
                    sort=sort,
                    remark=remark
                )
            else:
                raise Exception(msgconst.invalid_upload_file_sort)
            with open(timestamp_filename, 'wb') as u:
                for chunk in uf.chunks():
                    u.write(chunk)
        return HttpResponseRedirect(reverse('filemanage:file_list', args=[sort, 1]))
    except Exception, e:
        return render_to_response('503.html', {'errmsg': unicode(e).encode('utf-8')})


@login_required
def download(request, fileid):
    try:
        f = LXFile.objects.get(pk=fileid)
        with open(f.path, 'rb') as fh:
            filecontent = fh.read()
        fname, fext = os.path.splitext(f.name)
        content_type = 'text/plain'
        if '.doc' == fext:
            content_type = 'application/msword'
        elif '.docx' == fext:
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif '.xls' == fext:
            content_type = 'application/vnd.ms-excel'
        elif '.xlsx' == fext:
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content=filecontent, content_type=content_type)
        response['Content-Disposition'] = 'attachment;filename=%s' % urllib.quote(unicode(f.name).encode('utf-8'))
        return response
    except Exception, e:
        return render_to_response('503.html', {'errmsg': unicode(e).encode('utf-8')})