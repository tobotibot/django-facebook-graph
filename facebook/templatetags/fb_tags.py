#coding=utf-8
from django import template
from django.conf import settings
from facebook.utils import get_app_dict, get_static_graph, get_graph
from django.template.defaultfilters import escapejs, capfirst, stringfilter
import re
register = template.Library()
from django.utils.safestring import mark_safe
from facebook.testusers import TestUsers
from datetime import datetime

@register.simple_tag
def fb_app_settings(app_id=None):
    """ Returns a link to the user's app settings page for the current app. """
    if not settings.DEBUG:
        return ''
    else:
        if not app_id:
            app = get_app_dict()
            app_id = app['ID']
        link = '<a id="fb_app_settings_link" href="http://www.facebook.com/settings/?tab=applications&app_id=%s" target="_blank">X</a>' % app_id
        return mark_safe(link)
    
@register.simple_tag
def fb_api_key(app_name=None):
    app = get_app_dict(app_name)
    return app['API-KEY']

@register.simple_tag
def fb_app_id(app_name=None):
    app = get_app_dict(app_name)
    return app['ID']

@register.simple_tag
def fb_canvas_page(app_name=None):
    app = get_app_dict(app_name)
    return app['CANVAS-PAGE']

@register.simple_tag
def fb_domain(app_name=None):
    app = get_app_dict(app_name)
    return app['DOMAIN']

# TODO: Check request.is_secure on server. Local always True.
@register.simple_tag
def fb_canvas_url(request, app_name=None):
    app = get_app_dict(app_name)
    if request.is_secure and False:  # FIXME: For some reason always returns true.
        return app['SECURE-CANVAS-URL']
    else:
        return app['CANVAS-URL']

@register.simple_tag
def fb_redirect_url(app_name=None):
    app = get_app_dict(app_name)
    return app['REDIRECT-URL']

@register.simple_tag
def fb_first_app():
    app = settings.FACEBOOK_APPS.keys()
    return capfirst(app[0])

@register.inclusion_tag('facebook/includes/testuser_choice.html')
def fb_testuser_menu(app_name=None):
    graph = get_static_graph(app_name)
    tu = TestUsers(graph)
    testusers = tu.get_test_users()
    return {'users': testusers}

@register.simple_tag
def messages(message, user):
    return mark_safe(message.render(user))

@register.simple_tag
def messages_escaped(message, user):
    return mark_safe(escapejs(message.render(user)))

@register.simple_tag
def access_token(request):
    graph = get_graph(request)
    return mark_safe(graph.access_token)
    
@register.simple_tag(takes_context=True)
def query_page_fan(context, request):
    try:    
        is_fan = request.session['facebook']['signed_request']['page']['liked']
    except (AttributeError, KeyError):
        is_fan = False
    context['is_fan'] = is_fan
    return ''

@register.filter
@stringfilter
def post_uid(value):
    ids = value.split('_')
    return ids[-1]

@register.filter
@stringfilter
def parse_date(value):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+0000')  # 2011-07-13T10:24:18+0000
