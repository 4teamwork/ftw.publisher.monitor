from ftw.publisher.monitor import _
from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.interfaces import IMonitorNotifier
from time import time
from zope.component import getAdapter
import os.path
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


def invoke_notification(obj, event):
    """Event handler for `IQueueExecutedEvent` which invokes the
    `IReportNotifier` adapter.

    """
    registry = getUtility(IRegistry)
    config = registry.forInterface(IMonitorConfigurationSchema)
    if not config.enabled or not len(config.receivers):
        return

    monitor_queue_length(obj, event.queue, config)
    monitor_failed_extractions(obj, event.queue, config)


def monitor_queue_length(obj, queue, config):
    """Verify that the queue length does not exceed the the configured threshold.
    If it exceeds, notify the subscribers.
    """
    amount_of_jobs = queue.countJobs()
    if amount_of_jobs >= config.threshold:
        reason = _(u'warning_mail_message',
                   default=u'The amount of jobs in the publisher queue of the'
                   u' senders host reached the threshold. The queue may be blocked!')
        getAdapter(obj, IMonitorNotifier)(config, queue, reason)


def monitor_failed_extractions(obj, queue, config):
    """When the publisher is configured to exctract asynchronously, the extraction
    may fail. We monitor that by making sure that empty job files are not older than
    a threshold.
    """
    now = time()
    max_age = config.max_extraction_duration_seconds
    for job in queue.getJobs():
        # size -1 means job was already executed
        # size 0  means job is awating async extraction
        # size >1 means job is ready
        if job.getSize() != 0:
            # we are only interested in jobs awaiting extraction
            continue

        try:
            age = now - os.path.getmtime(job.dataFile)
        except OSError:
            continue

        if age > max_age:
            reason = _(u'warning_mail_message_extraction_problem',
                       default=u'Extraction of a publisher job failed for ${age} seconds.'
                       u' This will probably jam the queue.',
                       mapping={'age': int(age)})
            return getAdapter(obj, IMonitorNotifier)(config, queue, reason)
