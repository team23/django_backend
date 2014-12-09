from imagequery import Format, register_format, NewImageQuery


class BackendPreviewThumbnail(Format):
    def execute(self, query):
        return query.scale(700, 200).query_name('backend_preview_thumbnail')
register_format('backend_preview_thumbnail', BackendPreviewThumbnail)
