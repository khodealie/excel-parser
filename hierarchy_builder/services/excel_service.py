import pandas as pd
from hierarchy_builder.repositories.device_category_repository import DeviceCategoryRepository
from hierarchy_builder.repositories.brand_repository import BrandRepository
from hierarchy_builder.repositories.series_repository import SeriesRepository
from hierarchy_builder.repositories.device_model_repository import DeviceModelRepository


class ExcelService:
    def __init__(self, excel_file):
        self.excel_file = excel_file

    def process_excel_file(self):
        xls = pd.ExcelFile(self.excel_file)
        error_message = None

        for sheet_name in xls.sheet_names:
            try:
                if '-Series' in sheet_name:
                    self._process_series_and_models(xls, sheet_name)
                elif sheet_name == 'Devices':
                    self._process_device_categories(xls, sheet_name)
                else:
                    self._process_brands(xls, sheet_name)
            except Exception as e:
                error_message = f"Error processing sheet {sheet_name}: {e}"
                break

        return error_message

    def _process_device_categories(self, xls, sheet_name):
        existing_categories_names_in_redis = list(DeviceCategoryRepository.get_all_from_redis().keys())

        df = pd.read_excel(xls, sheet_name=sheet_name)
        categories_in_sheet = df['DeviceName'].dropna().str.lower().unique().tolist()
        categories_in_sheet = [cat for cat in categories_in_sheet if cat != 'nan']

        categories_to_add = [cat for cat in categories_in_sheet if cat not in existing_categories_names_in_redis]
        categories_to_delete = [cat for cat in existing_categories_names_in_redis if cat not in categories_in_sheet]

        for category_name in categories_to_add:
            DeviceCategoryRepository.create(name=category_name)

        for category_name in categories_to_delete:
            DeviceCategoryRepository.delete(name=category_name)

    def _process_brands(self, xls, sheet_name):
        df = pd.read_excel(xls, sheet_name=sheet_name)

        if not df.empty and len(df.columns) > 0:
            category_type_header = str(df.columns[0])
            category_type = category_type_header.replace('Name', '').lower()

            brands_in_sheet = df.iloc[:, 0].dropna().str.lower().unique().tolist()
            brands_in_sheet = [brand for brand in brands_in_sheet if brand != 'nan']

            existing_brand_names_in_redis = list(
                BrandRepository.get_brands_by_category_from_redis(category_type).keys())

            brands_to_add = [brand for brand in brands_in_sheet if brand not in existing_brand_names_in_redis]
            brands_to_delete = [brand for brand in existing_brand_names_in_redis if brand not in brands_in_sheet]

            for brand_name in brands_to_add:
                BrandRepository.create(name=brand_name, category_name=category_type)

            for brand_name in brands_to_delete:
                BrandRepository.delete(name=brand_name, category_name=category_type)

    def _process_series_and_models(self, xls, sheet_name):
        df = pd.read_excel(xls, sheet_name=sheet_name)

        if not df.empty and len(df.columns) > 1:
            category_type_header = str(df.columns[0])
            category_type = category_type_header.replace('Name', '').lower()

            for _, row in df.iterrows():
                brand_name = row.iloc[0].lower() if pd.notnull(row.iloc[0]) else None
                if brand_name in [None, 'nan']:
                    continue

                existing_series_and_models = SeriesRepository.get_series_and_models_by_brand(brand_name)

                series_and_models_in_sheet = {}
                current_series_name = None
                for item in row.iloc[1:].dropna():
                    item = str(item).lower()
                    if item == 'nan':
                        continue
                    if 's' in item:
                        current_series_name = item
                        series_and_models_in_sheet[current_series_name] = []
                    elif current_series_name:
                        model_name = item
                        series_and_models_in_sheet[current_series_name].append(model_name)

                for series_name, models_in_sheet in series_and_models_in_sheet.items():
                    if series_name != 'nan':
                        if series_name not in existing_series_and_models:
                            SeriesRepository.create(name=series_name, brand_name=brand_name)
                            existing_series_and_models[series_name] = []

                    for model_name in models_in_sheet:
                        if model_name != 'nan':
                            if model_name not in existing_series_and_models.get(series_name, []):
                                DeviceModelRepository.create(name=model_name, series_name=series_name,
                                                             brand_name=brand_name)
