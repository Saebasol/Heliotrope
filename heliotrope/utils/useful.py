from heliotrope.utils.hitomi.models import HitomiGalleryInfoModel


def remove_id_and_index_id(tag_or_file_list):
    response_dict_list = []
    for value in tag_or_file_list:
        del value["id"]
        del value["index_id"]
        response_dict_list.append(value)
    return response_dict_list


def is_raw(request_args):
    if (is_true := request_args.get("raw")) and (is_true.lower() == "true"):
        return True


def parse_raw_galleryinfo_list(raw_galleryinfo_list, include_files: bool = True):
    def parse(parsed_galleryinfo_model: HitomiGalleryInfoModel):
        model_dict = {
            "language_localname": parsed_galleryinfo_model.language_localname,
            "language": parsed_galleryinfo_model.language,
            "date": parsed_galleryinfo_model.date,
            "tags": parsed_galleryinfo_model.tags,
            "japanese_title": parsed_galleryinfo_model.japanese_title,
            "title": parsed_galleryinfo_model.title,
            "id": parsed_galleryinfo_model.galleryid,
            "type": parsed_galleryinfo_model.hitomi_type,
        }
        if include_files:
            model_dict.update({"files": parsed_galleryinfo_model.files})

        return model_dict

    return list(
        map(
            parse,
            map(
                lambda raw_result: HitomiGalleryInfoModel.parse_galleryinfo(
                    raw_result, True
                ),
                raw_galleryinfo_list,
            ),
        )
    )
