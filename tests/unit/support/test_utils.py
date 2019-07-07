import os
import re
from dataclasses import dataclass
from datetime import date
from datetime import timedelta

from dateutil import relativedelta

from django_graphql_playground.support import utils


def test_should_extract_db_properties_given_url():
    result = utils.extract_db_properties_from_url(
        "postgres://czazgirubdxrxw:8d5d635df6f2a226b1a1f81541cfcd20fadf8617fff383f553e39330392de901@ec2-54-243-47-196.compute-1.amazonaws.com:5432/dau6saplk4ri6e"
    )
    assert result.target == "postgres"
    assert result.user == "czazgirubdxrxw"
    assert result.password == "8d5d635df6f2a226b1a1f81541cfcd20fadf8617fff383f553e39330392de901"
    assert result.hostname == "ec2-54-243-47-196.compute-1.amazonaws.com"
    assert result.port == "5432"
    assert result.database_name == "dau6saplk4ri6e"
