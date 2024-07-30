class SearchDTO:
    def __init__(self, query_text, page, per_page, order_by):
        self.query_text = query_text
        self.page = page
        self.per_page = per_page
        self.order_by = order_by
