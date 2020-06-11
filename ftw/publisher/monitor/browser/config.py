from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from ftw.publisher.monitor import _
from ftw.publisher.monitor.interfaces import IMonitorConfigurationSchema
from ftw.publisher.monitor.utils import email_addresses_validator
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import form, button
from zope.i18nmessageid import MessageFactory

PloneMSF = MessageFactory('plone')


class MonitorConfigurationForm(RegistryEditForm):
    """Stores the monitor configuration
    """
    form.extends(RegistryEditForm)
    schema = IMonitorConfigurationSchema

    label = _(u'label_monitor_configuration',
              default=u'Monitor configuration')
    description = _(u'help_monitor_configuration',
                    default=u'Publisher monitor configuration')

    def updateActions(self):
        super(RegistryEditForm, self).updateActions()
        # Remove default action from RegistryEditForm
        del self.actions['cancel']
        del self.actions['save']

    @button.buttonAndHandler(_(u'button_save', default=u'Save'), name='button_save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        elif not email_addresses_validator(data.get('receivers')):
            self.status = _(u'error_invalid_addresses',
                            default=u'At least one of the defined addresses are not valid.')
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            PloneMSF(u"Changes saved."), "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_(u'button_cancel', default=u'Cancel'), name='button_cancel')
    def handleCancel(self, action):
        """"Cancel" button handler.
        """
        portal_url = getToolByName(self.context, 'portal_url')()
        url = portal_url + '/@@publisher-config'
        self.request.response.redirect(url)

MonitorConfigurationView = layout.wrap_form(MonitorConfigurationForm, ControlPanelFormWrapper)
MonitorConfigurationView.label = _(u'label_monitor_configuration',
                                   default=u'Monitor configuration')
