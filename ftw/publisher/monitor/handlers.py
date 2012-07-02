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
        return getAdapter(obj, IMonitorNotifier)(config, event.queue)
