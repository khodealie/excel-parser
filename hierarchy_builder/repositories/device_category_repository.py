from hierarchy_builder.models.device_category import DeviceCategory
from django.core.cache import cache


class DeviceCategoryRepository:
    REDIS_HASH_KEY = 'device_category'

    @staticmethod
    def get_all_from_redis():
        """
        Retrieves all device categories from the Redis hash.

        Returns:
            dict: A dictionary where keys are category names and values are their corresponding IDs.
        """
        # Fetch the entire hash map from Redis
        category_dict = cache.hgetall(DeviceCategoryRepository.REDIS_HASH_KEY)

        # Convert byte strings to strings and return
        return {key.decode('utf-8'): int(value) for key, value in category_dict.items()}

    @staticmethod
    def get_all():
        """
        Retrieves all device categories from the database.

        Returns:
            QuerySet: A Django QuerySet containing all device category instances.
        """
        return DeviceCategory.objects.all()

    @staticmethod
    def get_by_name(category_name):
        """
        Retrieves a device category by its name from the database.

        Parameters:
            category_name (str): The name of the category to retrieve.

        Returns:
            DeviceCategory: The device category instance matching the name, or None if not found.
        """
        return DeviceCategory.objects.filter(name=category_name).first()

    @staticmethod
    def get_by_id(id):
        """
        Retrieves a single device category by its database ID.

        Parameters:
            id (int): The ID of the device category to retrieve.

        Returns:
            DeviceCategory: The device category instance matching the ID, or None if not found.
        """
        return DeviceCategory.objects.filter(id=id).first()

    @staticmethod
    def create(name):
        """
        Creates a new device category with the given name. This method assumes the category
        does not exist in Redis and has been checked before this call. It adds the new category
        to both the database and Redis cache.

        Parameters:
            name (str): The name of the device category.

        Returns:
            DeviceCategory: The newly created device category instance.
        """
        # Attempt to create a new device category in the database
        category, created = DeviceCategory.objects.get_or_create(name=name)
        cache.hset(DeviceCategoryRepository.REDIS_HASH_KEY, name, category.id)

        return category

    @staticmethod
    def delete(name):
        """
        Deletes a device category by its name. If the category exists and is deleted, it also removes the corresponding entry from the Redis hash.

        Parameters:
            name (str): The name of the device category to delete.

        Returns:
            bool: True if the category was deleted, False otherwise.
        """
        category = DeviceCategory.objects.filter(name=name).first()
        if category:
            category.delete()
            cache.hdel(DeviceCategoryRepository.REDIS_HASH_KEY, name)
            return True
        return False
