from ftw.publisher.monitor import _
from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.interfaces import IMonitorNotifier
from zope.component import getAdapter


def invoke_notification(obj, event):
    """Event handler for `IQueueExecutedEvent` which invokes the
    `IReportNotifier` adapter.

    """
    config = IMonitorConfigurationSchema(obj)
    if not config.enabled or not len(config.get_receivers()):
        return

    amount_of_jobs = event.queue.countJobs()
    if amount_of_jobs >= config.threshold:
        reason = _(u'warning_mail_message',
                   default=u'The amount of jobs in the publisher queue of the'
                   u' senders host reached the threshold. The queue may be blocked!')
        return getAdapter(obj, IMonitorNotifier)(config, event.queue, reason)
