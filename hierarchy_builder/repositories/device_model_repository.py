from hierarchy_builder.models.device_model import DeviceModel
from hierarchy_builder.repositories.series_repository import SeriesRepository
from django_redis import get_redis_connection
import json

class DeviceModelRepository:
    PREFIX = 'series|'
    redis_con = get_redis_connection("default")

    @staticmethod
    def _redis_series_key(brand_name):
        """Constructs the Redis key for storing series related to a brand."""
        return f"{DeviceModelRepository.PREFIX}{brand_name}"

    @staticmethod
    def get_all():
        """
        Retrieves all device models from the database.

        Returns:
            QuerySet: A Django QuerySet containing all device model instances.
        """
        return DeviceModel.objects.select_related('series').all()

    @staticmethod
    def get_by_id(id):
        """
        Retrieves a single device model by its database ID.

        Parameters:
            id (int): The ID of the device model to retrieve.

        Returns:
            DeviceModel: The device model instance matching the ID, or None if not found.
        """
        return DeviceModel.objects.select_related('series').filter(id=id).first()

    @staticmethod
    def create(name, series_name, brand_name):
        """
        Creates a new device model with the given name, associated with a series by its name.
        Assumes the model does not exist in Redis and has been checked before this call.
        Adds the new model to both the database and Redis cache.

        Parameters:
            name (str): The name of the device model.
            series_name (str): The name of the Series to which the device model belongs.
            brand_name (str): The name of the Brand to which the series and model belong.

        Returns:
            DeviceModel: The newly created device model instance, or None if the series does not exist.
        """
        series = SeriesRepository.get_by_name(series_name, brand_name)
        if not series:
            raise ValueError(f"Series with name '{series_name}' for brand '{brand_name}' does not exist.")

        device_model = DeviceModel.objects.create(name=name, series=series)

        redis_key = DeviceModelRepository._redis_series_key(series.brand.name)
        models_list = json.loads(DeviceModelRepository.redis_con.hget(redis_key, series.name) or '[]')
        models_list.append(name)
        DeviceModelRepository.redis_con.hset(redis_key, series.name, json.dumps(models_list))

        return device_model

    @staticmethod
    def delete(model_name, series_name, brand_name):
        """
        Deletes a device model by its name, associated series name, and brand name.

        Parameters:
            model_name (str): The name of the device model to delete.
            series_name (str): The name of the series the device model belongs to.
            brand_name (str): The name of the brand the series belongs to.

        Returns:
            bool: True if the device model was successfully deleted, False otherwise.
        """
        device_model = DeviceModel.objects.filter(
            name=model_name,
            series__name=series_name,
            series__brand__name=brand_name
        ).first()

        if device_model:
            redis_key = DeviceModelRepository._redis_series_key(brand_name)
            models_list = json.loads(DeviceModelRepository.redis_con.hget(redis_key, series_name) or '[]')
            if model_name in models_list:
                models_list.remove(model_name)
                DeviceModelRepository.redis_con.hset(redis_key, series_name, json.dumps(models_list))

            device_model.delete()
            return True
        return False
