import datetime
import string

import factory.fuzzy

from ..models import APIRequestLog


class APIRequestLogFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("users.tests.factories.UserFactory")
    username_persistent = factory.LazyAttribute(
        lambda log: getattr(log.user, "username", "Anonymous")
        if getattr(log, "user", False)
        else "Anonymous"
    )
    requested_at = factory.fuzzy.FuzzyDateTime(datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC))
    response_ms = factory.Faker("random_int", min=0)
    path = factory.Faker("uri_path")
    view = factory.LazyAttribute(lambda obj: f"test_viewset.{obj.view_method}")
    view_method = factory.fuzzy.FuzzyText(prefix="method_", length=2, chars=string.ascii_uppercase)
    remote_addr = factory.Faker("ipv4")
    host = factory.Faker("domain_name", levels=2)
    method = factory.Faker("http_method")
    query_params = factory.Faker("json", num_rows=2)
    data = factory.Faker("json", num_rows=2)
    response = factory.Faker("text")
    errors = factory.Faker("text")
    status_code = factory.fuzzy.FuzzyChoice([200, 201, 301, 302, 303, 404, 400, 403])

    class Meta:
        model = APIRequestLog
