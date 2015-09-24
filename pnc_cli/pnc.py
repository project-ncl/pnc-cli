#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argh

from pnc_cli import productmilestones
from pnc_cli import products
from pnc_cli import productversions
from pnc_cli import projects
from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import buildconfigsetrecords
from pnc_cli import buildrecords
from pnc_cli import licenses
from pnc_cli import environments
from pnc_cli import runningbuilds
from pnc_cli import productreleases
from pnc_cli import buildrecordsets
from pnc_cli import users

parser = argh.ArghParser()
parser.add_commands([products.create_product,
                     products.update_product,
                     products.get_product,
                     products.list_products,
                     products.list_versions_for_product,
                     productversions.create_product_version,
                     productversions.list_product_versions,
                     productversions.get_product_version,
                     productversions.update_product_version,
                     projects.create_project,
                     projects.delete_project,
                     projects.update_project,
                     projects.get_project,
                     projects.list_projects,
                     licenses.create_license,
                     licenses.update_license,
                     licenses.delete_license,
                     licenses.get_license,
                     licenses.list_licenses,
                     buildconfigurations.create_build_configuration,
                     buildconfigurations.build,
                     # update_build_configuration,
                     buildconfigurations.get_build_configuration,
                     buildconfigurations.update_build_configuration,
                     buildconfigurations.delete_build_configuration,
                     buildconfigurations.list_dependencies,
                     buildconfigurations.add_dependency,
                     buildconfigurations.remove_dependency,
                     buildconfigurations.list_build_configurations,
                     buildconfigurations.list_build_configurations_for_product,
                     buildconfigurations.list_build_configurations_for_product_version,
                     # buildconfigurations.list_revisions_of_build_configuration,
                     # buildconfigurations.get_revision_of_build_configuration,
                     environments.create_environment,
                     environments.update_environment,
                     environments.delete_environment,
                     environments.get_environment,
                     environments.list_environments,
                     buildconfigurationsets.list_build_configuration_sets,
                     buildconfigurationsets.add_build_configuration_to_set,
                     buildconfigurationsets.create_build_configuration_set,
                     buildconfigurationsets.get_build_configuration_set,
                     buildconfigurationsets.list_build_records_for_set,
                     buildconfigurationsets.update_build_configuration_set,
                     buildconfigurationsets.delete_build_config_set,
                     buildconfigurationsets.list_build_configurations_for_set,
                     buildconfigurationsets.build_set,
                     buildrecords.list_build_records,
                     buildrecords.list_records_for_build_configuration,
                     buildrecords.list_records_for_project,
                     buildrecords.get_log_for_record,
                     buildrecords.get_audited_configuration_for_record,
                     buildrecords.list_build_artifacts,
                     buildrecords.get_build_record,
                     runningbuilds.list_running_builds,
                     runningbuilds.get_running_build,
                     productreleases.list_product_releases,
                     productreleases.create_release,
                     productreleases.list_releases_for_version,
                     productreleases.get_release,
                     productreleases.update_release,
                     productmilestones.list_milestones,
                     productmilestones.list_milestones_for_version,
                     productmilestones.create_milestone,
                     productmilestones.get_milestone,
                     productmilestones.update_milestone,
                     buildconfigsetrecords.list_build_configuration_set_records,
                     buildconfigsetrecords.get_build_configuration_set_record,
                     buildconfigsetrecords.get_records_for_build_config_set,
                     buildrecordsets.list_build_record_sets,
                     buildrecordsets.get_build_record_set,
                     users.create_user,
                     users.list_users,
                     users.update_user,
                     users.get_user])
parser.autocomplete()


def main():
    parser.dispatch()


if __name__ == "__main__":
    parser.dispatch()
