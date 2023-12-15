from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
# from recipes.models import Recipe


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_load_the_correct_view(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_the_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(
            response,
            'recipes/pages/search.html'
        )

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'),)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=<Teste>')
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot',
            response.content.decode('utf-8')
        )
