from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFCore.utils import getToolByName
from email.Header import Header
from email.MIMEText import MIMEText
from ftw.publisher.monitor import _
from ftw.publisher.monitor.interfaces import IMonitorNotifier
from zope.component import getUtility
from zope.interface import implements


class MonitorNotifier(object):
    """Default monitor notifier. Sends notification emails.
    """

    implements(IMonitorNotifier)

    def __init__(self, portal):
        self.context = portal
        self.config = None
        self.queue = None

    def __call__(self, config, queue, reason):
        self.config = config
        self.queue = queue
        self.reason = reason
        self.send_email()

    def send_email(self):
        """Sends the email
        """

        properties = getUtility(IPropertiesTool)
        mh = getToolByName(self.context, 'MailHost')
        from_addr = properties.email_from_address
        # prepare from address for header
        header_from = Header(properties.email_from_name.decode('utf-8'),
                             'iso-8859-1')
        header_from.append(u'<%s>' % from_addr.decode('utf-8'),
                           'iso-8859-1')

        # Subject
        subject = self.context.translate(self.get_subject())
        header_subject = Header(unicode(subject), 'iso-8859-1')

        html_body = self.render_template().encode('utf-8')
        msg = MIMEText(html_body, 'html', 'utf-8')
        msg['From'] = header_from
        msg['Subject'] = header_subject

        for rcpt in self.config.receivers:
            msg['To'] = rcpt
            mh.send(msg, mto=rcpt, mfrom=from_addr, subject=subject, immediate=True)

    def get_subject(self):
        return _(u'mail_subject',
                 default=u'Publisher monitor warning: ${site}',
                 mapping=dict(site=self.context.getProperty('title')))

    def get_options(self):
        """Returns a `dict` of data needed for rendering the mail template.
        """

        data = {'jobs_in_queue': self.queue.countJobs(),
                'subject': self.get_subject(),
                'portal': self.context,
                'reason': self.reason}
        return data

    def render_template(self):
        template = self.context.restrictedTraverse(
            '@@publisher-monitor-mail_notification_html')
        return template(**self.get_options())
