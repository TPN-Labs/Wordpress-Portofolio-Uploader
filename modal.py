from difflib import SequenceMatcher

def select_photo_from_options(all_photos, photo_name):
    similar_scores = []
    for photo_result in all_photos:
        result_name = photo_result.accessible_name
        similar_name_ratio = SequenceMatcher(None, result_name, photo_name).ratio()
        similar_scores.append(similar_name_ratio)

    photo_index = similar_scores.index(max(similar_scores)) + 1
    if len(all_photos) > 1:
        print("Found " + str(len(all_photos)) + " photos. Selecting photo " + str(photo_index) + ". Similarity scores: " + str(similar_scores))
    return True, photo_index
