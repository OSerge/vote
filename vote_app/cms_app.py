from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class VoteApp(CMSApp):
    app_name = "vote_app"
    name = _("VOTE")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["vote_app.urls"]


apphook_pool.register(VoteApp)