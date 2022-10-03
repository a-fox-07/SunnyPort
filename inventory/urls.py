from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('ingredients/', views.IngredientsView.as_view(), name="ingredients"),
    path('ingredients/new', views.CreateIngredientView.as_view(), name="create_ingredient"),
    path('ingredients/<pk>/update', views.UpdateIngredientView.as_view(), name="update_ingredient"),
    path('ingredients/<pk>/delete', views.DeleteIngredientView.as_view(), name="delete_ingredient"),
    path('menu_items/', views.MenuItemView.as_view(), name="menu_items"),
    path('menu_items/new', views.CreateMenuItemView.as_view(), name="create_menu_item"),
    path('menu_items/<pk>/update', views.UpdateMenuItemView.as_view(), name="update_menu_item"),
    path('menu_items/<pk>/delete', views.DeleteMenuItemView.as_view(), name="delete_menu_item"),
    path('recipe_requirements/', views.RecipeRequirementsView.as_view(), name="recipe_requirements"),
    path('recipe_requirements/new', views.CreateRecipeRequirementView.as_view(), name="create_recipe_requirement"),
    path('recipe_requirements/<pk>/update', views.UpdateRecipeRequirementView.as_view(), name="update_recipe_requirement"),
    path('recipe_requirements/<pk>/delete', views.DeleteRecipeRequirementView.as_view(), name="delete_recipe_requirement"),
    path('purchases/', views.PurchasesView.as_view(), name="purchases"),
    path('purchases/new', views.CreatePurchaseView.as_view(), name="create_purchase"),
    path('purchases/<pk>/delete', views.DeletePurchaseView.as_view(), name="delete_purchase"),
    path('financial/', views.FinancialView.as_view(), name='financial'),
    path('signup/' , views.SignUp.as_view(), name="signup"),
    path('logout/', views.logout_request, name="logout"),
    path("account/", include("django.contrib.auth.urls")),
]