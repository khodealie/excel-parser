from hierarchy_builder.repositories.device_category_repository import DeviceCategoryRepository
from hierarchy_builder.repositories.brand_repository import BrandRepository
from hierarchy_builder.repositories.series_repository import SeriesRepository

class HierarchyService:
    @staticmethod
    def get_full_hierarchy():
        categories = DeviceCategoryRepository.get_all_from_redis()
        hierarchy = {}
        for category_name, category_id in categories.items():
            brands = BrandRepository.get_brands_by_category_from_redis(category_name)
            hierarchy[category_name] = {}
            for brand_name, brand_id in brands.items():
                series_and_models = SeriesRepository.get_series_and_models_by_brand(brand_name)
                hierarchy[category_name][brand_name] = series_and_models
        return hierarchy
