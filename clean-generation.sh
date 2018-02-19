#!/bin/bash

set -euo pipefail

# (Optional) PNC root URL, if updating the API spec
pnc_root="${1:-}"

#
# swagger-codegen
#

codegen_dir="swagger-codegen"

# Update local copy of API spec
local_spec="$codegen_dir/swagger.json"
if [ -n "$pnc_root" ]
then
    # PNC bugs out if a double slash is present, so ensure the input URL doesn't have a trailing slash
    spec_url="${pnc_root%/}/pnc-rest/rest/swagger.json"
    echo "Downloading new copy of $local_spec" >&2
    curl -# -Lo "$local_spec" "$spec_url"
else
    echo "Using local copy of $local_spec" >&2
fi
if ! [ -f "$local_spec" ]
then
    echo "No local copy of swagger.json. You must specify the PNC root URL parameter, so that swagger.json can be downloaded" >&2
    exit 1
fi

# Verify/download codegen jar
IFS=' ' read -r codegen_sha1 codegen_version < "$codegen_dir/swagger-codegen-cli.version"
codegen_url="https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/$codegen_version/swagger-codegen-cli-$codegen_version.jar"
codegen_filename="$codegen_dir/swagger-codegen-cli.jar"
if sha1sum -c <<< "$codegen_sha1  $codegen_filename" &>/dev/null
then
    echo "Using local copy of $codegen_filename" >&2
else
    echo "Downloading new copy of $codegen_filename" >&2
    curl -# -Lo "$codegen_filename" "$codegen_url"
fi

output_dir="pnc_cli"
log_file="$codegen_dir/swagger-codegen-cli.log"

set -x

rm -rf "$output_dir/swagger_client"

java -jar "$codegen_filename" generate \
    -l python \
    -i "$local_spec" \
    -t templates \
    -o "$output_dir" \
    &> "$log_file"

grep -E "(WARN|ERROR)" "$log_file" >&2

#
# Clean
#

# Not using xargs to create more readable trace output
{ set +x; } 2>/dev/null
while read -r delete
do
    set -x
    rm -rf "$delete"
    { set +x; } 2>/dev/null
done < "$codegen_dir/cleanup"

#
# Patch
#

# Not using xargs to create more readable trace output
{ set +x; } 2>/dev/null
while read -r patchfile
do
    set -x
    patch -p1 -i "$patchfile" >&2
    { set +x; } 2>/dev/null
done < <(find "$codegen_dir/patches" -name '*.patch' | sort)

#
# Fin
#

echo "$(readlink -e "$output_dir")"
