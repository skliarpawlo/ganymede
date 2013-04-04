# coding: utf-8

from testing_runtime.web.job import json_to_users
from smtplib import SMTP
from ganymede import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from testing_runtime import models
import db
import json

def notify( task_id ) :

    # gather data
    task = db.session.query( models.Task )\
    .filter( models.Task.task_id == task_id ).one()

    users = json_to_users( task.job.users )

    all_results = json.loads( task.result )

    emails = []
    for user in users :
        emails.append( user.email )

    if len( emails ) == 0 :
        return

    # format data
    htmlmsg = u"""
    <html>
    <head>
        <style>
            table
            {
                border-collapse:collapse;
            }
            table, td, th
            {
                border:1px solid gray;
            }
            th
            {
                background-color:gray;
                color:white;
            }
        </style>
    </head>
    <body>"""
    htmlmsg += u'Задание <a href="{0}">#{1} "{2}"</a> прошло неудачно.'.format( "http://" + settings.BASE_URL + "/task/log/" + str(task.task_id), task.task_id, task.job.name )
    htmlmsg += u'<table>'
    for result in all_results :
        htmlmsg += u'<tr>'
        htmlmsg += u'<td>{0}</td><td>{1}</td>'.format( result["status"], result["name"] )
        htmlmsg += u'</tr>'
    htmlmsg += u'</table>'
    htmlmsg += u'</body></html>'

    textmsg = u'Задание #{0} "{1}" прошло неудачно.\n'.format( task.task_id, task.job.name )
    for result in all_results :
        textmsg += u'{0} | {1}'.format( result["status"], result["name"] )
        textmsg += u'\n'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Ganymede - Testing Fail'
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = ",".join( emails )
    msg.attach( MIMEText( htmlmsg.encode('utf-8'), 'html', _charset='utf-8' ) )
    msg.attach( MIMEText( textmsg.encode('utf-8'), 'text', _charset='utf-8' ) )

    # send emails
    smtpcon = SMTP( settings.EMAIL_HOST, settings.EMAIL_PORT )
    smtpcon.login( settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD )
    smtpcon.sendmail( settings.EMAIL_FROM, emails, msg.as_string() )


