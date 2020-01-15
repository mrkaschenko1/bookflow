# from django.contrib.auth.mixins import UserPassesTestMixin
# from django.core.exceptions import PermissionDenied
# from django.shortcuts import redirect
#
#
# class UserIsModeratorMixin(UserPassesTestMixin):
#
#     def test_func(self):
#
#         return self.request.user.profile.is_moderator
#
#     def handle_no_permission(self):
#         if self.raise_exception:
#             raise PermissionDenied(self.get_permission_denied_message())
#         return redirect('book_list')
#
#     def get_permission_denied_message(self):
#         return "You have not enough permissions to edit Book info"
