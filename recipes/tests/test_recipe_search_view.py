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

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This Recipe test title one'
        title2 = 'This Recipe test title two'
        recipe1 = self.make_recipe(title=title1, slug='One', author_data={'username': 'one'})
        recipe2 = self.make_recipe(title=title2, slug='Two', author_data={'username': 'two'})
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=This')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])
        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
