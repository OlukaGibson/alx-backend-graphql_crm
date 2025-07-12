import graphene
from crm.models import Product
from graphene_django.types import DjangoObjectType

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(ProductType)
    success = graphene.Boolean()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated = []

        for product in low_stock_products:
            product.stock += 10  # Simulate restocking
            product.save()
            updated.append(product)

        return UpdateLowStockProducts(success=True, updated_products=updated)

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
