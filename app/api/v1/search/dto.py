class SearchDTO:
    def __init__(self, query_text, page, per_page, case_sensitive, exact_text):
        self.query_text = query_text
        self.page = page
        self.per_page = per_page
        self.case_sensitive = case_sensitive
        self.exact_text = exact_text
