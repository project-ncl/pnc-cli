#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argh
from pnc_help_formatter import PNCFormatter
import products
import projects
import builds
import licenses
import environments

parser = argh.ArghParser()
parser.add_commands([products.create_product,
                     products.update_product,
                     products.get_product,
                     products.list_products,
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
                     builds.create_build_configuration,
                     builds.build,
                   #  update_build_configuration,
                     builds.list_build_configurations,
                     environments.create_environment,
                     environments.update_environment,
                     environments.delete_environment,
                     environments.get_environment,
                     environments.list_environments],
                    func_kwargs={"formatter_class": PNCFormatter})
parser.autocomplete()

if __name__ == "__main__":
    parser.dispatch()