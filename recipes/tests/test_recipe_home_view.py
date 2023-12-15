from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
# from recipes.models import Recipe


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(
            response.status_code,
            200
        )

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(
            response,
            'recipes/pages/home.html'
        )

    def test_recipe_home_template_shows_no_recipe_found_if_no_recipes(self):
        # Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'There is no Recipes in here!!!',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipe(self):
        # self.make_recipe(preparation_time=5, author_data={'first_name': 'Daviiziinn'}, category_data={'name': 'Café da Manhã'})
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        # response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertEqual(response_context_recipes.first().title, 'Recipe Title')
        # self.assertIn('5 Minutos', response_content)
        # self.assertIn('Daviiziinn', response_content)
        # self.assertIn('Café da Manhã', response_content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('There is no Recipes in here!!!', response.content.decode('utf-8'))
