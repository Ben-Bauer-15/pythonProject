from django.conf.urls import url
from . import views


urlpatterns = [
    #main landing page
    url(r'^$', views.index),

    #page for signup form
    url(r'^signup$', views.signup),

    #page for login form
    url(r'^login$', views.login),

    #page for creating a workout
    url(r'^create$', views.create),

    # POST route for creating a workout
    url(r'^create_workout$', views.create_workout),

    #page for recording a workout
    url(r'^record$', views.record),

    #view your workout history
    url(r'^history$', views.history),

    #view a particular workout
    url(r'^view/(?P<id>\d+)$', views.view),

    #view all users
    url(r'^users$', views.users),

    #view a particular user
    url(r'^user/(?P<id>\d+)', views.user),

    #mini template for adding a set in views.create
    url(r'^add_set$', views.add_set),

    #mini template for adding an exercise
    url(r'^add_exercise$', views.add_exercise),

    #POST route for adding a new user
    url(r'^new_user$', views.new_user),

    #POST route for validating with ajax
    url(r'^process_ajax$', views.process_ajax),

    #POST route for signing in an already registered user
    url(r'^signin$', views.signin),

    #route for logging out
    url(r'^logout$', views.logout)

] 