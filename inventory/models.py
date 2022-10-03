from tkinter import CASCADE
from django.db import models

# Create your models here.
class Ingredient(models.Model):
    ingredientName = models.CharField(max_length=200, unique=True, verbose_name="Ingredient")
    ingredientInStock = models.FloatField(default= 0, verbose_name="Amount in stock")
    ingredientUnit = models.CharField(max_length=10, verbose_name="Unit of measurement")
    ingredientPricePerUnit = models.FloatField(default=0, verbose_name="Price per unit")

    class Meta:
        ordering = ["ingredientName"]

    def get_absolute_url(self):
        return "/ingredients"
    
    def __str__(self):
        return f"{self.ingredientName}"

class MenuItem (models.Model):
    menuItemName = models.CharField(max_length=200, unique=True, verbose_name="Menu Item Name")
    menuItemPrice = models.FloatField(default=0, verbose_name="Menu Item Price")

    class Meta:
        ordering = ["menuItemName"]

    def get_absolute_url(self):
        return "/menu_items"
    
    def available(self):
        return all(X.enough() for X in self.reciperequirement_set.all())
    
    def __str__(self):
        return f"{self.menuItemName}"

class Purchase (models.Model):
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="Menu Item")
    timeStamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return "/purchases"

    def __str__(self):
        return f"{self.menuItem}"
    
class RecipeRequirement(models.Model):
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="Menu Item")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Required Ingredient")
    quantity = models.FloatField(default=0, verbose_name="Required Amount")

    def get_absolute_url(self):
        return "/menu_items"
    
    def enough(self):
        return self.quantity <= self.ingredient.ingredientInStock
    
    def __str__(self):
        return f"{self.menuItem.__str__()}: {self.ingredient.ingredientName} - {self.quantity}"