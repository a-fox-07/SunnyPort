from operator import not_
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm, PurchaseForm, RecipeRequirementForm
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.urls import reverse_lazy

# Create your views here.
# Home view, contains profit display

class Home (TemplateView):
    template_name = "inventory/home.html"
    
    

# Ingredient Views

class IngredientsView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredients.html"

class CreateIngredientView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "inventory/add_ingredient.html"

class UpdateIngredientView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "inventory/update_ingredient.html"

class DeleteIngredientView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/delete_ingredient.html"
    success_url = "/ingredients"

# Menu Item Views

class MenuItemView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/menu_items.html"

class CreateMenuItemView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "inventory/add_menu_item.html"

class UpdateMenuItemView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "inventory/update_menu_item.html"

class DeleteMenuItemView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "inventory/delete_menu_item.html"
    success_url = "/menu_items"

# Recipe Requirement Views

class RecipeRequirementsView(LoginRequiredMixin, ListView):
    model = RecipeRequirement
    template_name = "inventory/recipe_requirements.html"

class CreateRecipeRequirementView(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    form_class = RecipeRequirementForm
    template_name = "inventory/add_recipe_requirement.html"

class UpdateRecipeRequirementView(LoginRequiredMixin, UpdateView):
    model = RecipeRequirement
    form_class = RecipeRequirementForm
    template_name = "inventory/update_recipe_requirement.html"

class DeleteRecipeRequirementView(LoginRequiredMixin, DeleteView):
    model = RecipeRequirement
    template_name = "inventory/delete_recipe_requirement.html"
    success_url = "/menu_items"

# Purchase Views

class PurchasesView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchases.html"

class CreatePurchaseView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "inventory/add_purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_available"] = [X for X in MenuItem.objects.all() if X.available()]
        return context

    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menuItem=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.ingredientInStock -= requirement.quantity
            required_ingredient.save()

        purchase.save()
        return redirect("/purchases")

class DeletePurchaseView(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = "inventory/delete_purchase.html"
    success_url = "/purchases"

# Finacial View

class FinancialView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/financial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = Purchase.objects.all()
        revenue = 0
        food_expense = 0
        for transaction in Purchase.objects.all():
            revenue += transaction.menuItem.menuItemPrice
            for recipe_requirement in transaction.menuItem.reciperequirement_set.all():
                food_expense += recipe_requirement.ingredient.ingredientPricePerUnit * recipe_requirement.quantity
        
        context["revenue"] = revenue
        context["food_expense"] = food_expense
        context["profit"] = revenue - food_expense
        
        return context

# Signup / Logout Views

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def logout_request(request):
    logout(request)
    return redirect("home")