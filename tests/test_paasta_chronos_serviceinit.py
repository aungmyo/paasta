#!/usr/bin/env python

import mock

from paasta_tools.utils import PaastaColors
import paasta_chronos_serviceinit


def test_format_chronos_job_status_disabled():
    example_disabled_job = {
        'disabled': True,
    }
    actual = paasta_chronos_serviceinit.format_chronos_job_status(example_disabled_job)
    assert PaastaColors.red("Disabled") in actual


def test_format_chronos_job_status_enabled():
    example_disabled_job = {
        'disabled': False,
    }
    actual = paasta_chronos_serviceinit.format_chronos_job_status(example_disabled_job)
    assert PaastaColors.green("Enabled") in actual


def test_status_chronos_job_is_deployed():
    all_jobs = [{'name': 'thejobid'}]
    with mock.patch('paasta_chronos_serviceinit.format_chronos_job_status',
                    autospec=True, return_value='job_status_output'):
        actual = paasta_chronos_serviceinit.status_chronos_job('service', 'instance', 'thejobid', all_jobs)
        assert actual == 'job_status_output'


def test_status_chronos_job_is_not_deployed():
    all_jobs = []
    with mock.patch('paasta_chronos_serviceinit.format_chronos_job_status',
                    autospec=True, return_value='job_status_output'):
        actual = paasta_chronos_serviceinit.status_chronos_job('service', 'instance', 'thejobid', all_jobs)
        assert 'not setup' in actual


def test_status_chronos_job_is_duplicated():
    all_jobs = [{'name': 'thejobid'}, {'name': 'thejobid'}]
    with mock.patch('paasta_chronos_serviceinit.format_chronos_job_status',
                    autospec=True, return_value='job_status_output'):
        actual = paasta_chronos_serviceinit.status_chronos_job('service', 'instance', 'thejobid', all_jobs)
        assert 'should not happen' in actual