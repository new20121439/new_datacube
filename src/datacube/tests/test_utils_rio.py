import pytest
import mock

from datacube.utils.rio import (
    activate_rio_env,
    deactivate_rio_env,
    get_rio_env,
    set_default_rio_config,
    activate_from_config,
)


def test_rio_env_no_aws():
    deactivate_rio_env()

    # make sure we start without env configured
    assert get_rio_env() == {}

    ee = activate_rio_env()
    assert isinstance(ee, dict)
    assert ee == get_rio_env()
    assert 'GDAL_DISABLE_READDIR_ON_OPEN' not in ee
    assert 'GDAL_DATA' in ee
    assert 'AWS_ACCESS_KEY_ID' not in ee

    ee = activate_rio_env(cloud_defaults=True)
    assert 'GDAL_DISABLE_READDIR_ON_OPEN' in ee
    assert ee == get_rio_env()

    deactivate_rio_env()
    assert get_rio_env() == {}


def test_rio_env_aws():
    deactivate_rio_env()

    # make sure we start without env configured
    assert get_rio_env() == {}

    with pytest.raises(ValueError):
        activate_rio_env(aws='something')

    # note: setting region_name to avoid auto-lookup
    ee = activate_rio_env(aws=dict(aws_unsigned=True,
                                   region_name='us-west-1'))

    assert ee.get('AWS_NO_SIGN_REQUEST') == 'YES'

    ee = activate_rio_env(cloud_defaults=True,
                          aws=dict(aws_secret_access_key='blabla',
                                   aws_access_key_id='not a real one',
                                   aws_session_token='faketoo',
                                   region_name='us-west-1'))

    assert 'AWS_NO_SIGN_REQUEST' not in ee
    # check secrets are sanitized
    assert ee.get('AWS_ACCESS_KEY_ID') == 'xx..xx'
    assert ee.get('AWS_SECRET_ACCESS_KEY') == 'xx..xx'
    assert ee.get('AWS_SESSION_TOKEN') == 'xx..xx'

    assert ee.get('AWS_REGION') == 'us-west-1'

    # check sanitize can be turned off
    ee = get_rio_env(sanitize=False)
    assert ee.get('AWS_SECRET_ACCESS_KEY') == 'blabla'
    assert ee.get('AWS_ACCESS_KEY_ID') == 'not a real one'
    assert ee.get('AWS_SESSION_TOKEN') == 'faketoo'

    deactivate_rio_env()
    assert get_rio_env() == {}


@mock.patch('datacube.utils.aws.botocore_default_region',
            return_value=None)
def test_rio_env_aws_auto_region(*mocks):
    aws = dict(aws_secret_access_key='blabla',
               aws_access_key_id='not a real one',
               aws_session_token='faketoo')

    with mock.patch('datacube.utils.aws.ec2_current_region',
                    return_value='TT'):
        ee = activate_rio_env(aws=aws)
        assert ee.get('AWS_REGION') == 'TT'

    with mock.patch('datacube.utils.aws.ec2_current_region',
                    return_value=None):
        ee = activate_rio_env(aws=aws)
        assert 'AWS_REGION' not in ee

        with pytest.raises(ValueError):
            activate_rio_env(aws=dict(region_name='auto'))

    deactivate_rio_env()
    assert get_rio_env() == {}


def test_rio_env_aws_auto_region_dummy():
    "Just call it we don't know if it will succeed"

    # at least it should not raise error since we haven't asked for region_name='auto'
    ee = activate_rio_env(aws={})
    assert isinstance(ee, dict)

    deactivate_rio_env()
    assert get_rio_env() == {}


def test_rio_env_via_config():
    ee = activate_from_config()
    assert ee is not None

    # Second call should not change anything
    assert activate_from_config() is None

    set_default_rio_config(aws=None, cloud_defaults=True)

    # config change should activate new env
    ee = activate_from_config()
    assert ee is not None
    assert 'GDAL_DISABLE_READDIR_ON_OPEN' in ee

    deactivate_rio_env()
    assert get_rio_env() == {}
