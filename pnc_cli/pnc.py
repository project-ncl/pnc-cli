#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argh

from pnc_cli import bpmbuildconfigurations
from pnc_cli import buildconfigsetrecords
from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import buildrecords
from pnc_cli import environments
from pnc_cli import licenses
from pnc_cli import productmilestones
from pnc_cli import productreleases
from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import projects
from pnc_cli import repositoryconfigurations
from pnc_cli import runningbuilds
from pnc_cli import users
from pnc_cli import archives
import pnc_cli.user_config as uc
from pnc_cli import makemead





parser = argh.ArghParser()
parser.add_commands([uc.login,
                     products.create_product,
                     products.get_product,
                     products.list_products,
                     products.list_versions_for_product,
                     products.update_product,
                     productversions.create_product_version,
                     productversions.get_product_version,
                     productversions.list_product_versions,
                     productversions.update_product_version,
                     projects.create_project,
                     projects.delete_project,
                     projects.get_project,
                     projects.list_projects,
                     projects.update_project,
                     licenses.create_license,
                     licenses.delete_license,
                     licenses.get_license,
                     licenses.list_licenses,
                     licenses.update_license,
                     buildconfigurations.add_dependency,
                     buildconfigurations.build,
                     bpmbuildconfigurations.create_build_configuration_process,
                     buildconfigurations.create_build_configuration,
                     buildconfigurations.delete_build_configuration,
                     buildconfigurations.get_build_configuration,
                     buildconfigurations.get_revision_of_build_configuration,
                     buildconfigurations.list_build_configurations,
                     buildconfigurations.list_build_configurations_for_product,
                     buildconfigurations.list_build_configurations_for_product_version,
                     buildconfigurations.list_build_configurations_for_project,
                     buildconfigurations.list_dependencies,
                     buildconfigurations.list_revisions_of_build_configuration,
                     buildconfigurations.remove_dependency,
                     buildconfigurations.update_build_configuration,
                     environments.create_environment,
                     environments.delete_environment,
                     environments.get_environment,
                     environments.list_environments,
                     environments.update_environment,
                     buildconfigurationsets.add_build_configuration_to_set,
                     buildconfigurationsets.build_set,
                     buildconfigurationsets.create_build_configuration_set,
                     buildconfigurationsets.delete_build_configuration_set,
                     buildconfigurationsets.get_build_configuration_set,
                     buildconfigurationsets.list_build_configuration_sets,
                     buildconfigurationsets.list_build_configurations_for_set,
                     buildconfigurationsets.list_build_records_for_set,
                     buildconfigurationsets.list_build_set_records,
                     buildconfigurationsets.latest_build_set_records_status,
                     buildconfigurationsets.remove_build_configuration_from_set,
                     buildconfigurationsets.update_build_configuration_set,
                     buildrecords.list_artifacts,
                     buildrecords.get_audited_configuration_for_record,
                     buildrecords.get_build_record,
                     buildrecords.get_log_for_record,
                     buildrecords.list_attributes,
                     buildrecords.list_build_records,
                     buildrecords.list_built_artifacts,
                     buildrecords.list_dependency_artifacts,
                     buildrecords.list_records_for_build_configuration,
                     buildrecords.list_records_for_project,
                     buildrecords.put_attribute,
                     buildrecords.remove_attribute,
                     buildrecords.query_by_attribute,
                     runningbuilds.get_running_build,
                     runningbuilds.list_running_builds,
                     productreleases.create_release,
                     productreleases.get_release,
                     productreleases.list_product_releases,
                     productreleases.list_releases_for_version,
                     productreleases.update_release,
                     productmilestones.create_milestone,
                     productmilestones.close_milestone,
                     productmilestones.get_milestone,
                     productmilestones.list_distributed_artifacts,
                     productmilestones.list_distributed_builds,
                     productmilestones.list_milestones,
                     productmilestones.list_milestones_for_version,
                     productmilestones.update_milestone,
                     repositoryconfigurations.get_repository_configuration,
                     repositoryconfigurations.update_repository_configuration,
                     repositoryconfigurations.create_repository_configuration,
                     repositoryconfigurations.list_repository_configurations,
                     repositoryconfigurations.search_repository_configuration,
                     buildconfigsetrecords.get_build_configuration_set_record,
                     buildconfigsetrecords.list_build_configuration_set_records,
                     buildconfigsetrecords.list_records_for_build_config_set,
                     users.get_logged_user,
                     makemead.make_mead,
                     archives.generate_sources_zip])
parser.autocomplete()


def main():
    parser.dispatch()


if __name__ == "__main__":
    main()
