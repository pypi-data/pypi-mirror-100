# -*- coding: utf-8 -*-
# Copyright 2020 Cardiff University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the `igwn_accounting.report` module
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

import datetime
import io
import json
import subprocess
import sys
from getpass import getuser
from pathlib import Path
from shutil import which
from socket import getfqdn
from unittest import mock

from dateutil import tz

import pytest

from .. import report as igwn_report
from . import utils

# -- test data --------------

DATA_FILE = Path(__file__).parent / "condor_history.txt"
RESULT_JSON = json.dumps({
    "data": [
        {"user": "user1", "tag": "tag1", "usage": 7,
         "utcdate": "2021-01-01", "resource": "OSG.Remote"},
        {"user": "user1", "tag": "tag1", "usage": 7,
         "utcdate": "2021-01-01", "resource": "TEST"},
        {"user": "user1", "tag": "tag2", "usage": 2,
         "utcdate": "2021-01-01", "resource": "OSG.Remote"},
        {"user": "user2", "tag": "tag1", "usage": 2,
         "utcdate": "2021-01-01", "resource": "OSG.Remote"},
        {"user": "user2", "tag": "tag1", "usage": 2,
         "utcdate": "2021-01-01", "resource": "TEST"},
    ],
    "meta": {
        "key": "value",
    },
}, indent=None, sort_keys=True, separators=(",", ":"))
RESULT_ASCII = """
user1 tag1 7 2021-01-01 OSG.Remote
user1 tag1 7 2021-01-01 TEST
user1 tag2 2 2021-01-01 OSG.Remote
user2 tag1 2 2021-01-01 OSG.Remote
user2 tag1 2 2021-01-01 TEST
""".strip()


@pytest.fixture
def condor_history_file(tmpdir):
    history_file = str(tmpdir.join("history.txt"))
    with open(history_file, "w") as hf:
        utils.history_from_jsonl(str(DATA_FILE), hf)
    return history_file


# -- tests ------------------

def test_comment():
    stream = io.StringIO()
    igwn_report.comment("test", file=stream)
    assert stream.getvalue() == "# test\n"


@pytest.mark.parametrize("in_, out", (
    ("2021-01-01", datetime.datetime(2021, 1, 1, tzinfo=tz.tzutc())),
    ("1609459200.0", datetime.datetime(2021, 1, 1, tzinfo=tz.tzutc())),
))
def test_parse_date(in_, out):
    assert igwn_report.parse_date(in_) == out


def test_parse_date_error():
    with pytest.raises(ValueError) as exc:
        igwn_report.parse_date("bad")
    assert str(exc.value.args[0]).startswith("Unknown string format")


@pytest.mark.parametrize("userad, tagad", [
    (igwn_report.IGWN_USER_CLASSAD, igwn_report.IGWN_TAG_CLASSAD),
    ("Owner", "AccountingGroup"),
])
def test_parse_job(userad, tagad):
    job = {
        userad: "test",
        tagad: "test.dev.pytest",
        "RemoteWallClockTime": 100.,
        "CompletionDate": 1609460000,
        "CumulativeSuspensionTime": 10.,
    }
    assert igwn_report.parse_job(job, "deepthought") == (
         "test",
         "test.dev.pytest",
         90/3600.,
         "2021-01-01",
         "deepthought",
    )


@pytest.mark.parametrize("glidein_site, jobcluster", [
    # job that didn't report 'Site'
    (None, "deepthought"),
    # distributed job that reported as a local job
    ("Unknown", "deepthought"),
    # distributed job that ran remotely
    ("REMOTE", "OSG.REMOTE"),
])
def test_parse_job_osg(glidein_site, jobcluster):
    job = {
        igwn_report.IGWN_USER_CLASSAD: "test",
        igwn_report.IGWN_TAG_CLASSAD: "test.dev.pytest",
        "CompletionDate": 0,
        "CumulativeSuspensionTime": 0.,
        "EnteredCurrentStatus": 1609460000,
        "MATCH_GLIDEIN_Site": glidein_site,
        "RemoteWallClockTime": 3600.,
    }
    assert igwn_report.parse_job(job, "deepthought") == (
         "test",
         "test.dev.pytest",
         1.,
         "2021-01-01",
         jobcluster,
    )


@pytest.mark.parametrize(("mockoutput", "version"), [
    (b"$CondorVersion: 8.8.5 Sep 04 2019 4.5.6\nsomething else 1.2.3",
     "8.8.5"),
    (b"8.8.5 condor something", "8.8.5"),
    (b"HTCondor 10.11.123rc1", "10.11.123rc1"),
])
@mock.patch("subprocess.check_output")
def test_get_condor_version_number(mock, mockoutput, version):
    mock.return_value = mockoutput
    assert igwn_report.get_condor_version_number() == version


@mock.patch("socket.getfqdn")
@mock.patch("shutil.which", return_value="/test/condor_history")
@mock.patch("subprocess.run")
@pytest.mark.parametrize("fqdn", ["sched.test", "sched2.test"])
def test_get_history_subprocess_call(sprun, _, getfqdn, fqdn):
    # configure getfqdn mock
    getfqdn.return_value = fqdn

    # run the subprocess function
    igwn_report._get_history_subprocess(
        "sched.test",
        "Owner == test",
        ["A", "B"],
        "ClassAd > 12345",
        "pool.test",
    )

    expected = [
        "/test/condor_history",
        "-since", "ClassAD > 12345",
        "-constraint", "Owner == test",
        "-pool", "pool.test",
        "-af", "A", "B",
    ]
    if fqdn == "sched.test":  # -name is only used if necessary
        expected = expected[:5] + ["-name", "sched.test"] + expected[5:]

    assert sprun.called_once_with(
        expected,
        stdout=subprocess.PIPE,
        check=True,
    )


@mock.patch("subprocess.check_output", return_value=b"condor version 1.2.3")
@mock.patch.object(sys, "argv", ["a", "b", "c"])
@mock.patch.object(Path, "exists")
@mock.patch("datetime.datetime")
@pytest.mark.parametrize("has_condor_version, condor_version", [
    (False, None),
    (True, "condor version 1.2.3"),
])
def test_get_run_metadata(
        mock_datetime,
        mock_path_exists,
        mock_sys_argv,
        has_condor_version,
        condor_version,
):
    # finalise mocks
    mock_datetime.utcnow.return_value = "some date"
    mock_path_exists.return_value = has_condor_version
    # check function formats data correctly
    assert igwn_report.get_run_metadata() == {
        "collector_name": "igwn-accounting-report",
        "collector_version": igwn_report.__version__,
        "user": getuser(),
        "host": getfqdn(),
        "system_condor_version": condor_version,
        "python_version": sys.version,
        "cmd": "a b c",
        "utcdate": "some date",
    }


# end-to-end test with fake data


def mock_get_history(*args, **kwargs):
    with DATA_FILE.open("r") as file:
        for line in file:
            yield json.loads(line)


@pytest.mark.parametrize("fmt, expected", (
    ("ascii", RESULT_ASCII),
    ("json", RESULT_JSON),
))
@mock.patch("igwn_accounting.report._get_history_python", mock_get_history)
@mock.patch(
    "igwn_accounting.report.get_run_metadata",
    return_value={"key": "value"},
)
def test_main(_, fmt, expected, tmpdir):
    output = tmpdir.join("output.txt")
    igwn_report.main([
        "--cluster", "TEST",
        "--scheduler", "test.sched",
        "--utc", "2021-01-01",
        "--output-file", str(output),
        "--format", fmt,
    ])
    # check output matches
    assert output.read().strip() == expected


@pytest.mark.skipif(
    which("condor_history") is None,
    reason="no condor_history exe",
)
@mock.patch(
    "igwn_accounting.report.get_run_metadata",
    return_value={"key": "value"},
)
def test_main_condor_history_file(_, tmpdir, condor_history_file):
    """Check that the whole thing works with --condor-history-file

    This allows a fairly robust check of the full system, including
    a real-world test of the _get_history_subprocess function
    """
    output = tmpdir.join("output.txt")
    igwn_report.main([
        "--cluster", "TEST",
        "--scheduler", "test.sched",
        "--utc", "2021-01-01",
        "--output-file", str(output),
        "--format", "ascii",
        "--condor-history-file", str(condor_history_file),
    ])
    assert output.read().strip() == RESULT_ASCII
