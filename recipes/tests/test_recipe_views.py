from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe, Category, User


class RecipeViewTest(TestCase):
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
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'There is no Recipes in here!!!',
            response.content.decode('utf-8')
        )


    def test_recipe_home_template_loads_recipe(self):
        category = Category.objects.create(name='categoria')
        author = User.objects.create_user(
            first_name='User',
            last_name='Name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(
            title="Recipe Title",
            description="Recipe Description",
            slug="recipe-slug",
            preparation_time=10,
            preparation_time_unit="Minutos",
            servings=5,
            servings_unit="Porções",
            preparation_steps="Recipe Preparations Steps",
            preparation_steps_is_html=False,
            is_published=True,
            category=category,
            author=author,
        )
        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertEqual(response_context_recipes.first().title, 'Recipe Title')
        self.assertIn('10 Minutos', response_content)
        self.assertEqual(len(response_context_recipes), 1)
        ...


    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse(
            'recipes:category', 
            kwargs={'category_id': 1})
        )
        self.assertIs(
            view.func, 
            views.category
        )

    
    def test_recipe_category_view_returns_404_if_no_recipe(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 100}))
        self.assertEqual(response.status_code, 404)

    
    def test_recipe_detail_view_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
        
    
    def test_recipe_detail_view_return_404_if_no_recipe(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 100}))
        self.assertEqual(response.status_code, 404)
    

    

