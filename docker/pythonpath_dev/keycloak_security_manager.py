from flask import redirect, request
from flask_appbuilder.security.manager import AUTH_OID
from superset.security import SupersetSecurityManager
from flask_oidc import OpenIDConnect
from flask_appbuilder.security.views import AuthOIDView
from flask_login import login_user
from urllib.parse import quote
from flask_appbuilder.views import ModelView, SimpleFormView, expose
import logging
import urllib.parse

class OIDCSecurityManager(SupersetSecurityManager):

    def __init__(self, appbuilder):
        super(OIDCSecurityManager, self).__init__(appbuilder)
        if self.auth_type == AUTH_OID:
            self.oid = OpenIDConnect(self.appbuilder.get_app)
        self.authoidview = AuthOIDCView

class AuthOIDCView(AuthOIDView):

    @expose('/login/', methods=['GET', 'POST'])
    def login(self, flag=True):
        sm = self.appbuilder.sm
        oidc = sm.oid

        @self.appbuilder.sm.oid.require_login
        def handle_login():
            user = sm.auth_user_oid(oidc.user_getfield('email'))

            if user is None:
                info = oidc.user_getinfo(['preferred_username', 'given_name', 'family_name', 'email'])
                user = sm.add_user(info.get('preferred_username'), info.get('given_name'), info.get('family_name'),
                                   info.get('email'), sm.find_role('Gamma'))

            user_roles = oidc.user_getinfo(['roles'])['roles']
            if sm.find_role('Student') not in user.roles and 'student' in user_roles:
                user.roles.append(sm.find_role('Student'))
                sm.update_user(user)
            if sm.find_role('Staff') not in user.roles and 'staff' in user_roles:
                user.roles.append(sm.find_role('Staff'))
                sm.update_user(user)
            login_user(user, remember=False)
            return redirect('/superset/dashboard/45/')

        return handle_login()

    @expose('/logout/', methods=['GET', 'POST'])
    def logout(self):
        oidc = self.appbuilder.sm.oid

        oidc.logout()
        super(AuthOIDCView, self).logout()
        redirect_url = urllib.parse.quote_plus(request.url_root.strip('/') + self.appbuilder.get_url_for_login)

        return redirect(
            oidc.client_secrets.get('issuer') + '/protocol/openid-connect/logout?client_id='+ oidc.client_secrets.get('client_id')+'&post_logout_redirect_uri=' + 'https://bi.miem2.vmnet.top/')
