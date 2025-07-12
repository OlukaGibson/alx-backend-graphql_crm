from graphene_django.filter import DjangoFilterConnectionField
from .filters import CustomerFilter

class Query(graphene.ObjectType):
    hello = graphene.String()
    all_customers = DjangoFilterConnectionField(CustomerType, filterset_class=CustomerFilter)

    def resolve_hello(root, info):
        return "Hello, GraphQL!"


from graphene_django.types import DjangoObjectType
from .models import Customer, Product, Order
import graphene
from django.core.exceptions import ValidationError
from django.db import transaction

# Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

# Mutations
class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer, message="Customer created")

# Define other mutations: BulkCreateCustomers, CreateProduct, CreateOrder...

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    # Add the other mutations...


import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"


import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene

class UpdateLowStockProducts(graphene.Mutation):
    class Output:
        success = graphene.Boolean()
        updated_products = graphene.List(lambda: ProductType)

    def mutate(root, info):
        from crm.models import Product
        low_stock = Product.objects.filter(stock__lt=10)
        updated = []
        for product in low_stock:
            product.stock += 10
            product.save()
            updated.append(product)
        return UpdateLowStockProducts(success=True, updated_products=updated)

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

