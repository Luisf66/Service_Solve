from django.test import TestCase
from reviews.forms.review_form import ReviewForm


class ReviewFormTest(TestCase):

    def test_form_valido_com_rating_e_comment(self):
        form = ReviewForm(data={'rating': 5, 'comment': 'Excelente serviço!'})
        self.assertTrue(form.is_valid())

    def test_form_valido_sem_comment(self):
        form = ReviewForm(data={'rating': 3, 'comment': ''})
        self.assertTrue(form.is_valid())

    def test_form_invalido_sem_rating(self):
        form = ReviewForm(data={'rating': '', 'comment': 'Bom serviço'})
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_campos_corretos(self):
        form = ReviewForm()
        self.assertIn('rating', form.fields)
        self.assertIn('comment', form.fields)

    def test_form_rating_widget_min_max(self):
        form = ReviewForm()
        widget_attrs = form.fields['rating'].widget.attrs
        self.assertEqual(widget_attrs.get('min'), 1)
        self.assertEqual(widget_attrs.get('max'), 5)

    def test_form_comment_widget_rows(self):
        form = ReviewForm()
        widget_attrs = form.fields['comment'].widget.attrs
        self.assertEqual(widget_attrs.get('rows'), 3)