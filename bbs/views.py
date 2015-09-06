from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
import models


@login_required
def bbs_list(request, page_index):
    bbs_lists = models.BBS.objects.all()
    return render_to_response("bbs/bbs_list.html", {"bbs_list": bbs_lists, 'user': request.user})


@login_required
def bbs_detail(request, bbs_id):
    bbs = models.BBS.objects.get(id=bbs_id)
    return render_to_response("bbs/bbs_detail.html", {"bbs_obj": bbs, 'user': request.user})


@login_required
def sub_comment(request):
    bbs_id = request.POST.get('bbs_id')
    comment = request.POST.get('comment_content')
    comments.models.Comment.objects.create(
        content_type_id=9,
        object_pk=bbs_id,
        site_id=1,
        user=request.user,
        comment=comment,
    )

    return HttpResponseRedirect('/bbs/detail/%s' % bbs_id)


def bbs_pub(request):
    return render_to_response("bbs/bbs_pub.html")


def bbs_sub(request):
    content = request.POST.get('content')
    author = request.user
    models.BBS.objects.create(
        title = 'TEST TITLE',
        summary = 'HAHA',
        content = content,
        author =author,
        view_count= 1,
        ranking = 1,
           )

    return HttpResponse('yes.')