import pytest
from pnc_cli.swagger_client import ArtifactRest

__author__ = 'thauser'
from pnc_cli.swagger_client.apis import BuildrecordsApi
from pnc_cli.swagger_client.apis import ProductmilestonesApi
from test import testutils
import pnc_cli.user_config as uc


@pytest.fixture(scope='function', autouse=True)
def get_milestone_api():
    global milestone_api
    milestone_api = ProductmilestonesApi(uc.user.get_api_client())

@pytest.fixture(scope='function', autouse=True)
def get_records_api():
    global records_api
    records_api = BuildrecordsApi(uc.user.get_api_client())


def test_get_all_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'get_all')


def test_get_all(new_milestone):
    assert milestone_api.get_all(page_index=0, page_size=1000000, sort='', q='').content is not None


def test_create_new_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'create_new')


def test_create_new(new_milestone):
    milestones = [m.id for m in milestone_api.get_all(page_size=1000000).content]
    assert new_milestone.id in milestones


def test_get_all_by_product_version_id_no_version_id():
    testutils.assert_raises_valueerror(milestone_api, 'get_all_by_product_version_id', version_id=None)


def test_get_all_by_product_version_id_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'get_all_by_product_version_id', version_id=1)


def test_get_all_by_product_version_id():
    milestones = milestone_api.get_all_by_product_version_id(version_id=1, page_index=0, page_size=1000000, sort='',
                                                             q='').content
    assert milestones is not None


def test_get_specific_no_id():
    testutils.assert_raises_valueerror(milestone_api, 'get_specific', id=None)


def test_get_specific_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'get_specific', id=1)


def test_get_specific(new_milestone):
    retrieved = milestone_api.get_specific(new_milestone.id).content
    assert new_milestone.to_dict() == retrieved.to_dict()


def test_update_no_id():
    testutils.assert_raises_valueerror(milestone_api, 'update', id=None)


def test_update_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'update', id=1)


def test_update(new_milestone):
    new_milestone.download_url = "updatedUrlHere"
    milestone_api.update(id=new_milestone.id, body=new_milestone)
    updated = milestone_api.get_specific(new_milestone.id).content
    assert updated.to_dict() == new_milestone.to_dict()


def test_add_distributed_artifact_no_id():
    testutils.assert_raises_valueerror(milestone_api, 'add_distributed_artifact', id=None)


def test_add_distributed_artifact_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'add_distributed_artifact', id=1)


def test_add_distributed_artifact(new_milestone):
    test_builds = records_api.get_all(q='(buildConfigurationAudited.name=like=%cli-test%)').content
    record = test_builds[len(test_builds)-1] # latest test build
    artifact = records_api.get_built_artifacts(record.id).content[1] # first artifact
    milestone_api.remove_distributed_artifact(id=new_milestone.id, artifact_id=artifact.id)
    milestone_api.add_distributed_artifact(id=new_milestone.id, body=artifact)
    artifacts = milestone_api.get_distributed_artifacts(id=new_milestone.id).content
    assert artifact.id in [x.id for x in artifacts]


def test_get_distributed_artifacts_no_id():
    testutils.assert_raises_valueerror(milestone_api, 'get_distributed_artifacts', id=None)


def test_get_distributed_artifacts_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'get_distributed_artifacts', id=1)


def test_get_distributed_artifacts(new_milestone):
    result = milestone_api.get_distributed_artifacts(id=new_milestone.id).content
    assert result is not None


def test_get_distributed_builds_no_id():
    testutils.assert_raises_valueerror(milestone_api, 'get_distributed_builds', id=None)


def test_get_distributed_builds_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'get_distributed_builds', id=1)


def test_get_distributed_builds(new_milestone):
    result = milestone_api.get_distributed_builds(id=new_milestone.id).content
    assert result is not None


def test_remove_distributed_artifact_no_milestone_id():
    testutils.assert_raises_valueerror(milestone_api, 'remove_distributed_artifact', id=None, artifact_id=1)


def test_remove_distributed_artifact_no_artifact_id():
    testutils.assert_raises_valueerror(milestone_api, 'remove_distributed_artifact', id=1, artifact_id=None)


def test_remove_distributed_artifact_invalid_param():
    testutils.assert_raises_typeerror(milestone_api, 'remove_distributed_artifact', id=1, artifact_id=1)


def test_remove_distributed_artifact(new_milestone):
    test_builds = records_api.get_all(q='(buildConfigurationAudited.name=like=%cli-test%)').content
    record = test_builds[len(test_builds)-1] # latest test build
    artifact = records_api.get_built_artifacts(record.id).content[1] # first artifact
    milestone_api.remove_distributed_artifact(id=new_milestone.id, artifact_id=artifact.id)
    artifacts = milestone_api.get_distributed_artifacts(new_milestone.id).content
    assert artifacts is None or artifact.id not in [x.id for x in artifacts] # assert that removing the artifact either means there are no artifacts, or at least the removed artifact is not present
