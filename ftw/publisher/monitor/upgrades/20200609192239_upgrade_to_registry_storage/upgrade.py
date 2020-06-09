from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.upgrade import UpgradeStep
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility


class UpgradeToRegistryStorage(UpgradeStep):
    """Upgrade to registry storage
    """

    def __call__(self):
        self.install_upgrade_profile()
        annotations = IAnnotations(self.portal)
        storage = annotations.get('ftw.publisher.monitor-configuration', None)

        registry = getUtility(IRegistry)
        config = registry.forInterface(IMonitorConfigurationSchema)

        config.enabled = storage.get('enabled', False)
        config.receivers = storage.get('receivers', '').split('\n')
        config.threshold = storage.get('threshold', 100)
        config.max_extraction_duration_seconds = storage.get('max_extraction_duration_seconds', 180)
