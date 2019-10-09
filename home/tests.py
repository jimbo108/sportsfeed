from django.test import TestCase



class HomeTest(TestCase):

    def test_home_renders_correct_template(self):
        response = self.client.get('/home/')
        self.assertTemplateUsed(response, 'home.html') 
