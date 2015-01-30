import contextlib
import sys
import mock

from fig.cli import command

sys.path.append('../')
import paasta_tools
from paasta_tools import setup_marathon_job
from paasta_tools import marathon_tools

fake_service_name = 'fake_complete_service'
fake_instance_name = 'fake_instance'
fake_appid = 'fake--complete--service.gitdeadbeef.configdeadbeef2'
fake_service_config = {'container': {'docker': {'portMappings': [{'protocol': 'tcp', 'containerPort': 8888, 'hostPort': 0}], 'image': u'localhost/fake_docker_url', 'network': 'BRIDGE'}, 'type': 'DOCKER', 'volumes': [{u'hostPath': u'/nail/etc/habitat', u'containerPath': u'/nail/etc/habitat', u'mode': u'RO'}, {u'hostPath': u'/nail/etc/datacenter', u'containerPath': u'/nail/etc/datacenter', u'mode': u'RO'}, {u'hostPath': u'/nail/etc/ecosystem', u'containerPath': u'/nail/etc/ecosystem', u'mode': u'RO'}, {u'hostPath': u'/nail/etc/runtimeenv', u'containerPath': u'/nail/etc/runtimeenv', u'mode': u'RO'}, {u'hostPath': u'/nail/etc/region', u'containerPath': u'/nail/etc/region', u'mode': u'RO'}, {u'hostPath': u'/nail/etc/superregion', u'containerPath': u'/nail/etc/superregion', u'mode': u'RO'}, {u'hostPath': u'/nail/etc/topology_env', u'containerPath': u'/nail/etc/topology_env', u'mode': u'RO'}, {u'hostPath': u'/nail/srv', u'containerPath': u'/nail/srv', u'mode': u'RO'}, {u'hostPath': u'/etc/boto_cfg', u'containerPath': u'/etc/boto_cfg', u'mode': u'RO'}]}, 'instances': 1, 'mem': 300, 'args': [], 'backoff_factor': 2, 'cpus': 0.25, 'uris': ['file:///root/.dockercfg'], 'backoff_seconds': 1, 'id': fake_appid, 'constraints': None}

@when(u'we create a complete app')
def step_impl(context):
    with contextlib.nested(
        mock.patch('paasta_tools.marathon_tools.create_complete_config'),
        mock.patch('paasta_tools.marathon_tools.MarathonConfig'),
    ) as (
        mock_create_complete_config,
        mock_MarathonConfig,
    ):
        mock_MarathonConfig.return_value = mock.MagicMock(get=mock.Mock(return_value=context.marathon_config))
#        mock_MarathonConfig.get.return_value = context.marathon_config
        mock_create_complete_config.return_value = fake_service_config
        print marathon_tools.get_config()
        return_tuple = setup_marathon_job.setup_service(
            fake_service_name,
            fake_instance_name,
            context.client,
            context.marathon_config,
            fake_service_config,
        )
        assert return_tuple[0] == 0
        assert 'deployed' in return_tuple[1]


@then(u'we should see it in the list of apps')
def step_impl(context):
    assert fake_appid in marathon_tools.list_all_marathon_app_ids(context.client)


@then(u'we can run get_app on it')
def step_impl(context):
    assert context.client.get_app(fake_appid)
