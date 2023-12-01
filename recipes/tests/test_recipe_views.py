from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
#from recipes.models import Recipe


class RecipeViewTest(RecipeTestBase):
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
        #Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'There is no Recipes in here!!!',
            response.content.decode('utf-8')
        )


    def test_recipe_home_template_loads_recipe(self):
        #self.make_recipe(preparation_time=5, author_data={'first_name': 'Daviiziinn'}, category_data={'name': 'Café da Manhã'})
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertEqual(response_context_recipes.first().title, 'Recipe Title')
        #self.assertIn('5 Minutos', response_content)
        #self.assertIn('Daviiziinn', response_content)
        #self.assertIn('Café da Manhã', response_content)
        self.assertEqual(len(response_context_recipes), 1)


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

    def test_recipe_category_template_loads_recipe(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

        
    def test_recipe_detail_view_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
        
    
    def test_recipe_detail_view_return_404_if_no_recipe(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It loads one recipe'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        context = response.context['recipe']
        self.assertIn(needed_title, content)
        self.assertEqual(context.id, 1)
    

    

