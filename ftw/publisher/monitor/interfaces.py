from ftw.publisher.monitor import _
from zope import schema
from zope.interface import Interface


class IMonitorNotifier(Interface):
    """A `IMonitorNotifier` adapter is executed before the queue is executed
    (`BeforeQueueExecutionEvent`) and runs the monitor checks.
    """


class IMonitorConfigurationSchema(Interface):
    """Schema interface for monitor configuration.
    """

    enabled = schema.Bool(
        title=_(u'label_notification_enabled',
                default=u'Notification enabled'))

    receivers = schema.Text(
        title=_(u'label_receivers', default=u'Receivers'),
        description=_(u'help_receivers',
                      default=u'Enter one e-mail address per line.'),
        required=False)

    threshold = schema.Int(
         title=_(u'label_threshold', default=u'Queue size threshold'),
         description=_(u'help_threshold',
                       default=u'If the amount jobs in the queue is bigger '
                       'than this value, a alert will be sent.'),
         min=1,
         default=100,
         required=True)
