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
                default=u'Notification enabled'),
        default=False)

    receivers = schema.List(
        title=_(u'label_receivers', default=u'Receivers'),
        description=_(u'help_receivers',
                      default=u'Enter one e-mail address per line.'),
        value_type=schema.TextLine(),
        default=[],
        required=False)

    threshold = schema.Int(
        title=_(u'label_threshold', default=u'Queue size threshold'),
        description=_(u'help_threshold',
                      default=u'If the amount jobs in the queue is bigger '
                      'than this value, a alert will be sent.'),
        default=100,
        required=True)

    max_extraction_duration_seconds = schema.Int(
        title=_(u'label_max_extraction_duration_seconds',
                default=u'Maximum extraction duration (seconds)'),
        description=_(u'help_max_extraction_duration_seconds',
                      default=u'If the asynchronous extraction takes longer than this'
                      u' amount of seconds, it is considered to not work.'
                      u' Candidates are 0-sized jobs, measurement is the age of the'
                      u' modification time of the data file.'),
        default=3 * 60,
        required=True)
