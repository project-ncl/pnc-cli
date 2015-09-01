#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argh
from pnc_help_formatter import PNCFormatter
import products
import productversions
import projects
import buildconfigurations
import buildconfigurationsets
import buildrecords
import licenses
import environments
import runningbuilds
import productreleases

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
                   #  update_build_configuration,
                     buildconfigurations.list_build_configurations,
                     environments.create_environment,
                     environments.update_environment,
                     environments.delete_environment,
                     environments.get_environment,
                     environments.list_environments,
                     buildconfigurationsets.list_build_configuration_sets,
                     #buildconfigurationsets.add_build_configuration_to_set,
                     buildconfigurationsets.create_build_config_set,
                     buildconfigurationsets.get_build_config_set,
                     buildconfigurationsets.update_build_config_set,
                     buildconfigurationsets.delete_build_config_set,
                     buildconfigurationsets.list_build_configurations_for_set,
                     buildconfigurationsets.trigger_build_config_set,
                     buildrecords.list_build_records,
                     buildrecords.list_records_for_build_config,
                     buildrecords.list_records_for_project,
                     buildrecords.get_logs_for_record,
                     buildrecords.get_audited_config_for_record,
                     buildrecords.get_build_artifacts,
                     buildrecords.get_build_record,
                     runningbuilds.list_running_builds,
                     runningbuilds.get_running_build,
                     productreleases.list_product_releases,
                     productreleases.create_product_release,
                     productreleases.list_release_support_levels(),
                     productreleases.list_releases_for_version,
                     productreleases.get_product_release,
                     productreleases.update_product_release],
                    func_kwargs={"formatter_class": PNCFormatter})
parser.autocomplete()

if __name__ == "__main__":
    parser.dispatch()