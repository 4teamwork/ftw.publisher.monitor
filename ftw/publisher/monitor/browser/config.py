from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.publisher.monitor import _
from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.utils import email_addresses_validator
from persistent.dict import PersistentDict
from plone.fieldsets.form import FieldsetsEditForm
from zope.annotation.interfaces import IAnnotations
from zope.app.component.hooks import getSite
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements


ANNOTATIONS_KEY = 'ftw.publisher.monitor-configuration'


class MonitorConfigurationAdapter(SchemaAdapterBase, object):
    """Stores the monitor configuration
    """

    adapts(IPloneSiteRoot)
    implements(IMonitorConfigurationSchema)

    def __init__(self, context):
        super(MonitorConfigurationAdapter, self).__init__(self)
        self.annotations = IAnnotations(context)
        self.storage = self.annotations.get(ANNOTATIONS_KEY, None)
        if not isinstance(self.storage, PersistentDict):
            self.annotations[ANNOTATIONS_KEY] = PersistentDict()
            self.storage = self.annotations.get(ANNOTATIONS_KEY)

    def is_enabled(self):
        return self.storage.get('enabled', False) and True or False

    def set_enabled(self, value):
        self.storage['enabled'] = value and True or False

    enabled = property(is_enabled, set_enabled)

    def get_receivers_plain(self):
        return self.storage.get('receivers', '')

    def get_receivers(self):
        """Get receivers as list
        """
        data = self.storage.get('receivers', '')
        if data:
            return data.split('\n')
        else:
            return []

    def set_receivers_plain(self, value):
        self.storage['receivers'] = value

    receivers = property(get_receivers_plain, set_receivers_plain)

    def get_threshold(self):
        return self.storage.get('threshold', 100)

    def set_threshold(self, value):
        self.storage['threshold'] = int(value)

    threshold = property(get_threshold, set_threshold)

    def get_max_extraction_duration_seconds(self):
        return self.storage.get('max_extraction_duration_seconds', 3 * 60)

    def set_max_extraction_duration_seconds(self, value):
        self.storage['max_extraction_duration_seconds'] = int(value)

    max_extraction_duration_seconds = property(get_max_extraction_duration_seconds,
                                               set_max_extraction_duration_seconds)


class MonitorConfigurationForm(FieldsetsEditForm):
    """Monitor configuration form
    """

    template = ViewPageTemplateFile('config.pt')

    label = _(u'label_monitor_configuration',
              default=u'Monitor configuration')
    description = _(u'help_monitor_configuration',
                    default=u'Publisher monitor configuration')

    form_name = label
    form_fields = form.FormFields(IMonitorConfigurationSchema)

    def __init__(self, *args, **kwargs):
        super(MonitorConfigurationForm, self).__init__(*args, **kwargs)
        self.status = None

    @form.action(_(u'button_save', default=u'Save'))
    def handle_edit_action(self, action, data):
        """"Save" button handler.
        """
        if not email_addresses_validator(data.get('receivers')):
            self.status = _(u'error_invalid_addresses',
                            default=u'At least one of the defined addresses '
                            'are not valid.')
        else:
            # call the super handle_edit_action, but the method is
            # wrapped in a @form.action(), so we need to extract it...
            super_action = FieldsetsEditForm.handle_edit_action
            super_action_method = super_action.success_handler
            return super_action_method(self, action, data)

    @form.action(_(u'button_cancel', default=u'Cancel'))
    def handle_cancel(self, action, data):
        """"Cancel" button handler.
        """
        portal = getSite()
        portal_url = getToolByName(self.context, 'portal_url')()
        url = portal_url + '/@@publisher-config'
        return portal.REQUEST.RESPONSE.redirect(url)
