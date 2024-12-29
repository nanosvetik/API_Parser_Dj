import requests

def get_area_id(area_name):
    """
    Возвращает ID региона по его названию.
    Если регион не найден, возвращает None.
    """
    response = requests.get('https://api.hh.ru/areas')
    areas = response.json()

    def find_area(areas, target_name):
        for area in areas:
            if area['name'].lower() == target_name.lower():
                return area['id']
            if 'areas' in area:
                result = find_area(area['areas'], target_name)
                if result:
                    return result
        return None

    return find_area(areas, area_name)