from django.shortcuts import render, get_list_or_404, get_object_or_404
# from utils.recipes.factory import make_recipe
from recipes.models import Recipe
from django.http import Http404
from django.db.models import Q


def home(request):
    recipes = Recipe.objects.filter(is_published=True)
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
        'title': 'Home | Recipes'
    })


def category(request, category_id):
    # recipes = Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id')
    recipes = get_list_or_404(
        Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id')
    )
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category'
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        # 'title': f'{recipe.title}, | Recipe'
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request, ):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    recipes = Recipe.objects.filter(Q(Q(title__icontains=search_term) | Q(description__icontains=search_term)), is_published=True).order_by('-id')
    return render(request, 'recipes/pages/search.html', context={
        'search_term': search_term,
        'page_title': f'Search for "{search_term}" | Recipes',
        'recipes': recipes,
    })
