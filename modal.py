from difflib import SequenceMatcher

def select_photo_from_options(all_photos, photo_name):
    photo_is_found = False
    photo_index = 1
    for photo_result in all_photos:
        result_name = photo_result.accessible_name
        similar_name_ratio = SequenceMatcher(None, result_name, photo_name).ratio()
        if similar_name_ratio > 0.9:
            photo_is_found = True
            if len(all_photos) > 1:
                print("Selected photo number: " + str(photo_index) + ": similarity ratio: " + str(similar_name_ratio))
            break
        photo_index += 1
    return photo_is_found, photo_index
