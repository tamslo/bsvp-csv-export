def build_video(url, description):
    return '<a href="{}" class="movie" title="{}" target="_blank">{}</a>'.format(url, description, description)

def export_video(prod_fields, tooltips):
    videos = []
    index = 1
    index_present = True

    while(index_present):
        url_field = "YT" + str(index)
        description_field = "YTDESC" + str(index)
        if url_field in prod_fields and description_field in prod_fields:
            url = prod_fields[url_field]
            description = prod_fields[description_field]
            if url != "" and description != "":
                videos.append(build_video(url, description))
                index += 1
            else:
                index_present = False
        else:
            index_present = False

    return "<br/>".join(videos)
