
class Animal:

   def __init__(self, category):
      self.category = category

   def get_category(self):
      print(self.category)

a = Animal('Dog')
a.get_category()
