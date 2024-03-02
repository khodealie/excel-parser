from hierarchy_builder.models.brand import Brand
from hierarchy_builder.repositories.device_category_repository import DeviceCategoryRepository
from django.core.cache import cache


class BrandRepository:
    PREFIX = 'brand|'

    @staticmethod
    def _redis_hash_key(category_name):
        """
        Constructs the Redis hash key for a given category.
        """
        return f"{BrandRepository.PREFIX}{category_name}"

    @staticmethod
    def get_brands_by_category_from_redis(category_name):
        """
        Retrieves all brands for a given category from the Redis cache.

        Parameters:
            category_name (str): The name of the category for which to retrieve brands.

        Returns:
            dict: A dictionary where keys are brand names and values are their corresponding IDs, for the specified category.
        """
        hash_key = BrandRepository._redis_hash_key(category_name)
        brand_dict = cache.hgetall(hash_key)

        # Convert byte strings to strings (Redis stores data as bytes)
        return {key.decode('utf-8'): int(value) for key, value in brand_dict.items()}

    @staticmethod
    def get_all():
        """
        Retrieves all brands from the database.
        """
        return Brand.objects.select_related('category').all()

    @staticmethod
    def get_by_name(name):
        """
        Retrieves a brand by its name.

        Parameters:
            name (str): The name of the brand to retrieve.

        Returns:
            Brand: The brand instance matching the name, or None if not found.
        """
        return Brand.objects.filter(name=name).first()

    @staticmethod
    def get_by_id(id):
        """
        Retrieves a brand by its ID.
        """
        return Brand.objects.select_related('category').filter(id=id).first()

    @staticmethod
    def create(name, category_name):
        """
        Creates a new brand with the given name and associated category. If the specified category
        does not exist, it creates the category. Adds the new brand to both the database and
        Redis cache.

        Parameters:
            name (str): The name of the brand.
            category_name (str): The name of the category to which the brand belongs.

        Returns:
            Brand: The newly created brand instance.
        """
        # Ensure the category exists or create a new one if it doesn't
        category = DeviceCategoryRepository.get_by_name(category_name)
        if not category:
            category = DeviceCategoryRepository.create(category_name)

        # Directly create the new brand in the database
        brand = Brand.objects.create(name=name, category=category)

        # Add the new brand to the Redis cache
        hash_key = BrandRepository._redis_hash_key(category_name)
        cache.hset(hash_key, name, brand.id)

        return brand

    @staticmethod
    def delete(name, category_name):
        """
        Deletes a brand by its name and category.

        Parameters:
            name (str): The name of the brand to delete.
            category_name (str): The name of the category the brand belongs to.

        Returns:
            bool: True if the brand was successfully deleted, False otherwise.
        """
        brand = Brand.objects.filter(name=name, category__name=category_name).first()
        if brand:
            hash_key = BrandRepository._redis_hash_key(brand.category.name)
            cache.hdel(hash_key, name)
            brand.delete()
            return True
        return False
