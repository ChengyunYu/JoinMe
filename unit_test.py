import unittest

# The class we want to test
from Model.EventModel import EventModel as EventModel
from Model.UserModel import UserModel as UserModel
import Controller.EventController as EventController
import Controller.UserController as UserController

class Test(unittest.TestCase):
    date = '2018-10-31'
    event_1 = EventModel(1, 'event_title_1', 'tags_1', 'description_1', 'image_1', [], [], date, 'location_1', '5')
    user_1 = UserModel(1, 'real_name_1', 'nickname_1', 'gender_1', 'email_1', 'location_1', 'tags_1', 'description_1', [], [])
    # test event model
    def test_post_event(self):
        event_id_1 = EventController.post_event(self.user_1, self.event_1)

        self.assertIsNotNone(event_id_1)
        
    def test_edit_event(self):
        
    
#     def test_expire:
        
#     def test_remove_user:
        
#     def test_join_event:
    
#     def test_host_event:
    
#     def test_hosted_event:
        
#     def test_get_hosted_event:
        
    # test user model
    def test_add_user(self):
        UserController.delete_user('nickname_1', 'email_1')
        self.assertEqual(UserController.add_user(self.user_1), 'SUCCESS')
        self.assertEqual(UserController.add_user(self.user_1), 'DUPLICATE')
        UserController.delete_user('nickname_1', 'email_1')
        
    def test_delete_user(self):
        self.assertEqual(UserController.delete_user('nickname_1', 'email_1'), 'SUCCESS')
        self.assertEqual(UserController.delete_user('fake_nickname_1', 'fake_email_1'), 'SUCCESS')

#     def test_edit_user:
        
        
#     def test_retrieve_user:
        
if __name__ == '__main__':
    # log_file = 'unittest_log.txt'
    # f = open(log_file, 'a')
    # runner = unittest.TextTestRunner(f)
    # unittest.main(testRunner=runner)
    # f.close()
    unittest.main()