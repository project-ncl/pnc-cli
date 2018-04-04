
from pnc_cli.swagger_client import BpmApi
from pnc_cli.swagger_client import BuildrecordpushApi
from pnc_cli.swagger_client import BuildrecordsApi
from pnc_cli.swagger_client import BuildsApi
from pnc_cli.swagger_client import BuildconfigsetrecordsApi
from pnc_cli.swagger_client import BuildconfigurationsApi
from pnc_cli.swagger_client import BuildconfigurationsetsApi
from pnc_cli.swagger_client import EnvironmentsApi
from pnc_cli.swagger_client import LicensesApi
from pnc_cli.swagger_client import ProductmilestonesApi
from pnc_cli.swagger_client import ProductreleasesApi
from pnc_cli.swagger_client import ProductsApi
from pnc_cli.swagger_client import ProductversionsApi
from pnc_cli.swagger_client import ProjectsApi
from pnc_cli.swagger_client import RepositoryconfigurationsApi
from pnc_cli.swagger_client import RunningbuildrecordsApi
from pnc_cli.swagger_client import UsersApi
import pnc_cli.user_config as uc


class PncApi:
    
    def __init__(self):
        self._user = None
        
        self._bpm = None
        self._build_push = None
        self._builds = None
        self._builds_running = None
        self._build_groups = None
        self._build_configs = None
        self._build_group_configs = None
        self._environments = None
        self._licenses = None
        self._product_milestones = None
        self._product_releases = None
        self._products = None
        self._product_versions = None
        self._projects = None
        self._repositories = None
        self._running_builds = None
        self._users = None

    @property
    def user(self):
        if self._user is None:
            self._user = uc.get_user()
        return self._user

    @property
    def bpm(self):
        if not self._bpm:
            self._bpm = BpmApi(self.user.get_api_client())
        return self._bpm

    @property
    def build_push(self):
        if not self._build_push:
            self._build_push = BuildrecordpushApi(self.user.get_api_client())
        return self._build_push

    @property
    def builds(self):
        if not self._builds:
            self._builds = BuildrecordsApi(self.user.get_api_client())
        return self._builds

    @property
    def builds_running(self):
        if not self._builds_running:
            self._builds_running = BuildsApi()
        return self._builds_running

    @property
    def build_groups(self):
        if not self._build_groups:
            self._build_groups = BuildconfigsetrecordsApi(self.user.get_api_client())
        return self._build_groups

    @property
    def build_configs(self):
        if not self._build_configs:
            self._build_configs = BuildconfigurationsApi(self.user.get_api_client())
        return self._build_configs

    @property
    def build_group_configs(self):
        if not self._build_group_configs:
            self._build_group_configs = BuildconfigurationsetsApi(self.user.get_api_client())
        return self._build_group_configs

    @property
    def environments(self):
        if not self._environments:
            self._environments = EnvironmentsApi(self.user.get_api_client())
        return self._environments

    @property
    def licenses(self):
        if not self._licenses:
            self._licenses = LicensesApi(self.user.get_api_client())
        return self._licenses

    @property
    def product_milestones(self):
        if not self._product_milestones:
            self._product_milestones = ProductmilestonesApi(self.user.get_api_client())
        return self._product_milestones

    @property
    def product_releases(self):
        if not self._product_releases:
            self._product_releases = ProductreleasesApi(self.user.get_api_client())
        return self._product_releases

    @property
    def products(self):
        if not self._products:
            self._products = ProductsApi(self.user.get_api_client())
        return self._products

    @property
    def product_versions(self):
        if not self._product_versions:
            self._product_versions = ProductversionsApi(self.user.get_api_client())
        return self._product_versions

    @property
    def projects(self):
        if not self._projects:
            self._projects = ProjectsApi(self.user.get_api_client())
        return self._projects

    @property
    def repositories(self):
        if not self._repositories:
            self._repositories = RepositoryconfigurationsApi(self.user.get_api_client())
        return self._repositories

    @property
    def running_builds(self):
        if not self._running_builds:
            self._running_builds = RunningbuildrecordsApi(self.user.get_api_client())
        return self._running_builds

    @property
    def users(self):
        if not self._users:
            self._users = UsersApi
        return self._users

pnc_api = PncApi()
