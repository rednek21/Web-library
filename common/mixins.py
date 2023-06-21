class TitleMixin:
    html_title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['html_title'] = self.html_title
        return context
