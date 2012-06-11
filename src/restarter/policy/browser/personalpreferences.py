from plone.app.users.browser.personalpreferences import UserDataPanel as AccountPanelForm


class UserDataPanel(AccountPanelForm):
    """ Implementation of personalize form that uses formlib """

    def __init__(self, context, request):
        super(UserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('rpx_identifier')

