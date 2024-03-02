from hierarchy_builder.models.series import Series
from hierarchy_builder.repositories.brand_repository import BrandRepository
from django.core.cache import cache
import json


class SeriesRepository:
    PREFIX = 'series|'

    @staticmethod
    def _redis_series_key(brand_name):
        """Constructs the Redis key for storing series related to a brand."""
        return f"{SeriesRepository.PREFIX}{brand_name}"

    @staticmethod
    def get_series_and_models_by_brand(brand_name):
        """
        Retrieves all series and their models for a given brand from Redis.

        Parameters:
            brand_name (str): The name of the brand.

        Returns:
            dict: A dictionary with series names as keys and lists of model names as values.
        """
        hash_key = SeriesRepository._redis_series_key(brand_name)
        series_data = cache.hgetall(hash_key)

        # Deserialize model data from JSON
        return {series.decode('utf-8'): json.loads(models) for series, models in series_data.items()}

    @staticmethod
    def get_all():
        """
        Retrieves all series from the database.

        Returns:
            QuerySet: A Django QuerySet containing all series instances, with related brand data.
        """
        return Series.objects.select_related('brand').all()

    @staticmethod
    def get_by_name(name, brand_name):
        """
        Retrieves a series by its name and the name of its associated brand.

        Parameters:
            name (str): The name of the series to retrieve.
            brand_name (str): The name of the brand to which the series belongs.

        Returns:
            Series: The series instance matching the name and brand, or None if not found.
        """
        brand = BrandRepository.get_by_name(brand_name)
        if not brand:
            return None

        return Series.objects.filter(name=name, brand=brand).first()

    @staticmethod
    def get_by_id(id):
        """
        Retrieves a single series by its database ID, including related brand data.

        Parameters:
            id (int): The ID of the series to retrieve.

        Returns:
            Series: The series instance matching the ID, or None if not found.
        """
        return Series.objects.select_related('brand').filter(id=id).first()

    @staticmethod
    def create(name, brand_name):
        """
        Creates a new series with the given name and associated brand, identified by brand name.
        Assumes the series does not exist in Redis and has been checked before this call.
        Adds the new series to both the database and Redis cache.

        Parameters:
            name (str): The name of the series.
            brand_name (str): The name of the Brand to which the series belongs.

        Returns:
            Series: The newly created series instance, or None if the brand does not exist.
        """
        brand = BrandRepository.get_by_name(brand_name)
        if not brand:
            raise ValueError(f"Brand with name '{brand_name}' does not exist.")

        # Create the new series in the database
        series = Series.objects.create(name=name, brand=brand)

        # Add the new series to the Redis cache with an initial empty list of models
        hash_key = SeriesRepository._redis_series_key(brand.name)
        cache.hset(hash_key, series.name, json.dumps([]))

        return series

    @staticmethod
    def delete(series_name, brand_name):
        """
        Deletes a series by its name and the associated brand's name.

        Parameters:
            series_name (str): The name of the series to delete.
            brand_name (str): The name of the brand the series belongs to.

        Returns:
            bool: True if the series was successfully deleted, False otherwise.
        """
        series = Series.objects.filter(name=series_name, brand__name=brand_name).first()
        if series:
            hash_key = SeriesRepository._redis_series_key(series.brand.name)
            cache.hdel(hash_key, series_name)
            series.delete()
            return True
        return False
