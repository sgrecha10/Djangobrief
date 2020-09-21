from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse

# Create your views here.
def index(request):

    typelist = [1, 2, 'anna']
    typestr = ''
    typeint = 123213

    listfilters = [
        ('length', ('typelist', 'typestr')),
    ]


    part1 = '{% extends "base.html" %}{% block title %}Templates{% endblock %}{% block content %}<div class="row"><div class="col-sm-12"><h1>Template</h1><table class="table table-hover">'
    part3 = '</table></div></div>{% endblock %}'

    myfilter = 'pluralize:"а,и"'

    part2 = '{% for row in listfilters %}' \
            '<tr>' \
                '<td>data | {{ row.0 }}</td>' \
                '<td>' \
                    '<ul>' \
                    '{% for item in row.1 %}' \
                        '<li>' \
                            '<div>{{ item }}</div>' \
                            '<div>{{ typestr|'+myfilter+' }}</div>' \
                        '</li>' \
                    '{% endfor %}' \
                    '</ul>' \
                '</td>' \
            '</tr>' \
            '{% endfor %}'



    page = part1 + part2 + part3

    template = Template(page)
    context = {'listfilters': listfilters, 'typelist': typelist, 'typestr': typestr, 'typeint': typeint}
    return HttpResponse(template.render(Context(context)))
