from parsel import Selector

from api.models import Category


def test_category_page_should_have_properly_configured_columns(admin_client):
    fake_category_name = "fake-category-name"
    Category.objects.create(name=fake_category_name)

    response = admin_client.get("/admin/api/category/")
    selector = Selector(text=str(response.content))

    list_of_columns = [None, "Name", "Created at", "Updated at", "Start at", "End at", None]

    for index, value in enumerate(list_of_columns, 1):
        assert value == selector.css(f"#result_list > thead > tr th:nth-child({index}) div.text a::text").get()

    assert fake_category_name == selector.css("#result_list > tbody > tr > th > a::text").get()
    assert "1 category" == selector.css("#changelist-form > p::text").get().strip("\\n")
