# from django.urls import resolve, reverse
# from django.test import TestCase
# from boards.views import (
#     home_view, board_topics, new_topic
# )
# from boards.models import (
#     Board, Topic, Post
# )
# from .forms import NewTopicForm
#
# # Create your tests here.
#
# # class HomeTests(TestCase):
# #     def test_home_view_status_code(self):
# #         url = reverse('home')
# #         response = self.client.get(url)
# #         self.assertEquals(response.status_code, 200)
# #
# #     def test_home_url_resolves_home_view(self):
# #         view = resolve('/')
# #         self.assertEquals(view.func, home_view)
#
#
# # class BoardTopicsTests(TestCase):
# #     def setUp(self):
# #         Board.objects.create(name='Django', description='Django board.')
#     #
#     # def test_board_topics_view_success_status_code(self):
#     #     url = reverse('board_topics', kwargs={'pk': 1})
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 200)
#     #
#     # def test_board_topics_view_not_found_status_code(self):
#     #     url = reverse('board_topics', kwargs={'pk': 99})
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 404)
#     #
#     # def test_board_topics_url_resolves_board_topics_view(self):
#     #     view = resolve('/boards/1/')
#     #     self.assertEquals(view.func, board_topics)
#     #
#     # def test_board_topics_view_contains_link_back_to_homepage(self):
#     #     board_topics_url = reverse('board_topics', kwargs={'pk': 1})
#     #     response = self.client.get(board_topics_url)
#     #     homepage_url = reverse('home')
#     #     self.assertContains(response, 'href="{0}"'.format(homepage_url))
#     #
#     # def test_board_topics_view_contains_navigation_links(self):
#     #     board_topics_url = reverse('board_topics', kwargs={'pk': 1})
#     #     homepage_url = reverse('home')
#     #     new_topic_url = reverse('new_topic', kwargs={'pk': 1})
#     #
#     #     response = self.client.get(board_topics_url)
#     #
#     #     self.assertContains(response, 'href="{0}"'.format(homepage_url))
#     #     self.assertContains(response, 'href="{0}"'.format(new_topic_url))
#
# class NewTopicTests(TestCase):
#     def setUp(self):
#         Board.objects.create(name='Django', description='Django board.')
# #
# #     def test_new_topic_view_success_status_code(self):
# #         url = reverse('new_topic', kwargs={'pk': 1})
# #         response = self.client.get(url)
# #         self.assertEquals(response.status_code, 200)
# #
# #     def test_new_topic_view_not_found_status_code(self):
# #         url = reverse('new_topic', kwargs={'pk': 99})
# #         response = self.client.get(url)
# #         self.assertEquals(response.status_code, 404)
# #
# #     def test_new_topic_url_resolves_new_topic_view(self):
# #         view = resolve('/boards/1/new/')
# #         self.assertEquals(view.func, new_topic)
# #
# #     def test_new_topic_view_contains_link_back_to_board_topics_view(self):
# #         new_topic_url = reverse('new_topic', kwargs={'pk': 1})
# #         board_topics_url = reverse('board_topics', kwargs={'pk': 1})
# #         response = self.client.get(new_topic_url)
# #         self.assertContains(response, 'href="{0}"'.format(board_topics_url))
#
#     def test_contains_form(self):  # <- new test
#         url = reverse('new_topic', kwargs={'pk': 1})
#         response = self.client.get(url)
#         form = response.context.get('form')
#         self.assertIsInstance(form, NewTopicForm)
#
#     def test_new_topic_invalid_post_data(self):  # <- updated this one
#         '''
#         Invalid post data should not redirect
#         The expected behavior is to show the form again with validation errors
#         '''
#         url = reverse('new_topic', kwargs={'pk': 1})
#         response = self.client.post(url, {})
#         form = response.context.get('form')
#         self.assertEquals(response.status_code, 200)
#         self.assertTrue(form.errors)
import json

gg = "{'szlobov': {'firstName': 'Serhii', 'lastName': 'Zlobov', 'company': 'DataArt', 'position': 'Python Developer', 'urn_id': 'ACoAAAbV-QoBaQ_FGurzwd4m7BiMCHYAqBWLvIk', 'displayPictureUrl': '', 'location': 'Ukraine'}, 'artemsklar': {'firstName': 'Artem', 'lastName': 'Skliar', 'company': ' AnvilEight', 'position': 'Python developer ', 'urn_id': 'ACoAAA0M_bIBca7m_dFTyh2RelrYpQqab0XFK4o', 'displayPictureUrl': '', 'location': 'Ukraine'}, 'anna-shlepak-3103a3121': {'firstName': 'Anna', 'lastName': 'Shlepak', 'company': ' Luxoft', 'position': 'Python Developer ', 'urn_id': 'ACoAAB4is_wBD2pjrmbJCOcNsyWF_IPXNDWj68I', 'displayPictureUrl': '', 'location': 'Ukraine'}, 'volodindmitriy121': {'firstName': 'Dmitriy', 'lastName': 'Volodin', 'company': 'разработчик – Quantum_Inc', 'position': 'Python', 'urn_id': 'ACoAACF7P_sBzxEqZgi0pNTgnuzTvuoY9SIQLic', 'displayPictureUrl': '', 'location': 'Ukraine'}, 'shpergl': {'firstName': 'Shpergl', 'lastName': 'Oleksander', 'company': 'GlobalLogic', 'position': 'Senior Python Developer', 'urn_id': 'ACoAABjohcwB6wG4qn6rTJqujwnPzUEiJir9yUM', 'displayPictureUrl': '', 'location': 'Ukraine'}, 'andrey-karbanovich-a099195a': {'firstName': 'Andrey', 'lastName': 'Karbanovich', 'company': '', 'position': 'Full Stack (Python/JS/Swift) developer – AnvilEight', 'urn_id': 'ACoAAAyYH2kBWC92I0tzq4imdVqxtJgzE5OuQR0', 'displayPictureUrl': '', 'location': 'Ukraine'}, 'dmitry-vasilishin-378044117': {'firstName': 'Dmitry', 'lastName': 'Vasilishin', 'company': '', 'position': 'Middle Python Developer – Ciklum', 'urn_id': 'ACoAAB0EEQwBylJuGFYmfRs9Bpd4SQV0AeByvKc', 'displayPictureUrl': '', 'location': 'Ukraine'}, 'vova-dranyy-727445a8': {'firstName': 'Vova', 'lastName': 'Dranyy', 'company': 'Remote work', 'position': 'Python Developer', 'urn_id': 'ACoAABbYmc8Bql6khVgNXrnZQPkAq9Tjt7zmZok', 'displayPictureUrl': '', 'location': 'Ukraine'}, 'антон-поляков-8aa578188': {'firstName': 'Антон', 'lastName': 'Поляков', 'company': '', 'position': 'Python backend developer', 'urn_id': 'ACoAACw47gIBDYv8iFfYZgAOFSvQvyYU-cpI3SQ', 'displayPictureUrl': '', 'location': 'Ukraine'}, 'illia-boichuk': {'firstName': 'Illia', 'lastName': 'Boichuk', 'company': '', 'position': 'Python developer – LaSoft', 'urn_id': 'ACoAACXfX2sB-VG4PL-b3RpZ1T0nrpiLbitufJo', 'displayPictureUrl': '', 'location': 'Ukraine'}}"


# def list_of_str_to_dict(dict):
#    for index, item in enumerate(dict):
#        json_acceptable_string = item.replace(": ", " : ")
#        json_acceptable_string = json_acceptable_string.replace("'", "\"")
#        dict[index] = json_acceptable_string
#    return json.loads(json.dumps(dict))

print(type(json.loads(gg)))

