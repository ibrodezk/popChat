from .models import PopUser
import random
def save_profile(backend, user, response, *arg , **kwargs):
    print("response")
    print(response)
    print("user")
    print(user)
    print("backend")
    print(backend)
    PopUser.objects.create(username="bsd" + str(random.randint(1,1000001)), email="asd")
    print("hello im in save profile")