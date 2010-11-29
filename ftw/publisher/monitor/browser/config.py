from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.publisher.monitor import _
from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from persistent.dict import PersistentDict
from plone.fieldsets.form import FieldsetsEditForm
from zope.annotation.interfaces import IAnnotations
from zope.app.component.hooks import getSite
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
import re


ANNOTATIONS_KEY = 'ftw.publisher.monitor-configuration'


def email_addresses_validator(value):
    """Validator for validating the e-mail addresses field.
    `value` is a string of carriage-return-seperated bulk of e-mail addresses.
    Returns `True` if all addresses are valid, otherwise `False`.

    >>> from ftw.publisher.monitor.browser import config
    >>> validate = config.email_addresses_validator

    Some tests:

    >>> validate('hugo.boss@web.de')
    True
    >>> validate('''hugo.boss@web.de
    ... hugo.boss@web.de''')
    True
    >>> validate('1my@mail.de')
    True
    >>> validate('info@4teamwork.ch')
    True
    >>> validate('my-very.special-mail@ver.y.spec.ial.do.main.com')
    True

    Local E-Mail addresses work too:

    >>> validate('me@home.local')
    True
    >>> validate('me@local')
    False

    """

    if value == None:
        return True

    expr = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=" +\
                          "?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?" +\
                          "\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$",
                      re.IGNORECASE)

    addresses = value.strip().split('\n')
    for addr in addresses:
        addr = addr.strip()
        if not expr.match(addr):
            return False
    return True


class MonitorConfigurationAdapter(SchemaAdapterBase):
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
