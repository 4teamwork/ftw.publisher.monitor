from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase


class MonitorConfigLink(ViewletBase):
    """Viewlet for adding a link to the ftw.publisher.sender viewlet manager
    which is shown in the publisher control panel.
    """

    render = ViewPageTemplateFile('link.pt')
