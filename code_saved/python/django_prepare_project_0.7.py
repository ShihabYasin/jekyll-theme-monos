#!/usr/bin/env python
import argparse
import os
import shutil, ast
from django.urls import resolve
################################################################################
PROJECT_NAME = 'social'
APP_NAME = 'dwitter'
VIR_ENV = 'django_v3'
add_apps = ['livereload', 'django_extensions', 'rest_framework']

curr_dir = os.getcwd()

# TODO
# 1. (done) add base.html auto Template, and in app
# 2. Plug out any app (urls , settings theke baad deya)
# Create a dummy model init, add crud stuffs auto for a model in an app
# Create static folder auto for app
# create a form func() in app


################################################################################
## Helper methods
# For django
def get_info_from_view_request(request, print_values=False):
    request_dict = {}
    request_dict["app_name"] = resolve(request.path).app_name
    request_dict["username"] = request.user.username,
    request_dict["scheme"] = request.scheme,
    request_dict["path"] = request.path,
    request_dict["method"] = request.method,
    request_dict["params"] = request.GET,  # as per method call e.g: GET
    request_dict["username"] = request.user.username,
    request_dict["is_anonymous"] = request.user.is_anonymous,
    request_dict["is_staff"] = request.user.is_staff,
    request_dict["is_superuser"] = request.user.is_superuser,
    request_dict["is_active"] = request.user.is_active

    if print_values:
        for key, values in request_dict.items():
            print(f"{key}: {values}")

    return request_dict

################################################################################


def register_app_in_project(apps_to_add, project_name):
    # print (type (apps_to_add))

    a_file = open (project_name + '/settings.py', "r")
    list_of_lines = a_file.readlines ()
    lsstr = ''
    for idx, line in enumerate (list_of_lines):
        if 'INSTALLED_APPS' in line:
            list_of_lines[idx] = line
            # print('Found')
            flag = True
            for x in apps_to_add:
                # print(x)
                for ln in list_of_lines[idx + 1:]:
                    # print(ln.strip())
                    if x in ln.strip ():
                        flag = False
                        break
                    if ']' in ln.strip ():
                        list_of_lines[idx] = lsstr + "    \n]"
                        flag = False
                        break

                if flag:
                    # Title_case = x.title()
                    # lsstr += "    '" + x + ".apps."+Title_case+"}.Config'" + ',\n'
                    lsstr += "    '" + x + "'" + ',\n'

        # list_of_lines[idx] = line + lsstr
        # break

    a_file = open (project_name + '/settings.py', "w")
    a_file.writelines (list_of_lines)
    a_file.close ()


def add_app_urls_in_project_urls(app_name, project_name):
    a_file = open (project_name + '/urls.py', "r")
    list_of_lines = a_file.readlines ()
    flag_headre = True
    for line in list_of_lines:
        if line.strip () == 'from django.urls import include, path':
            flag_headre = False

    if flag_headre:
        list_of_lines = [f'from django.urls import include, path\n\n'] + list_of_lines

    flag = True
    find_url = f"path('{app_name}/', include('{app_name}.urls')),"
    for idx, line in enumerate (list_of_lines):
        lsstr = ''
        if 'urlpatterns = [' in line:
            for ln in list_of_lines[idx + 1:]:
                if find_url in ln.strip ():
                    flag = False
                    break
                if ']' in ln.strip ():
                    break

            if flag:
                lsstr += f"    path('{app_name}/', include('{app_name}.urls')),\n"

        list_of_lines[idx] = line + lsstr

    a_file = open (project_name + '/urls.py', "w")
    a_file.writelines (list_of_lines)
    a_file.close ()


def create_virtual_env(virtual_env_name=VIR_ENV, path_to_link_from_another_vir_env='/home/tigerit/Desktop/intelcaffe/Django/django_v3'):
    os.system ('rm requirements.txt ')
    os.system ('rm Learning.md ')
    os.system ('rm Makefile ')

    os.system ('ln -s /home/tigerit/Desktop/intelcaffe/Django/requirements.txt .')
    os.system ('ln -s /home/tigerit/Desktop/intelcaffe/Django/Learning.md .')
    os.system ('ln -s /home/tigerit/Desktop/intelcaffe/Django/Makefile .')

    print (f'Creating virtual env: {virtual_env_name} ... ')
    if os.path.isdir (virtual_env_name):
        os.system (f'rm -rf {virtual_env_name}')

    if path_to_link_from_another_vir_env is not None:
        os.system(f'ln -s /home/tigerit/Desktop/intelcaffe/Django/django_v3 {curr_dir}')
    else:
        print(f'Creating vir env {virtual_env_name} ...')
        os.system (f'python3 -m venv {virtual_env_name}')
    print (f' ===>   PLZ ACTIVATE VIR ENV {VIR_ENV} ...  <=== ')

def create_super_user(username='test', password='test', mail='test@test.com'):
    os.system (f'DJANGO_SUPERUSER_PASSWORD={password} python manage.py createsuperuser --username {username} --email {mail} --noinput')
    print (f'\n\nSuper user created with usename: {username} , pass: {password}, mail: {mail}\n\n')


def create_a_django_project_and_app(project_name, app_name, virtual_env, requirements_file):
    if os.path.exists (virtual_env):
        os.system (f'pip install -r {requirements_file}')
        if not os.path.exists (project_name):
            os.system (f'django-admin startproject {project_name} .')
            os.system (f'mkdir {project_name}/static')
        os.system (f'python manage.py startapp {app_name}')
        os.system (f'mkdir {app_name}/static')
        os.system (f'mkdir {app_name}/static/img')
        os.system (f'python manage.py migrate')
        os.system (f'python manage.py check')
    else:
        print (f' ===>   PLZ ACTIVATE VIR ENV {virtual_env} ...  <=== ')


def create_dummy_views(app_name, project_name=PROJECT_NAME):
    '''
    Create a dummy views at url: '/' named hello_world with base_template base.html
    :param app_name:
    :param project_name:
    :return:
    '''
    with open (app_name + '/views.py', 'w') as f:
        f.writelines ("""from django.shortcuts import get_object_or_404\nfrom django.shortcuts import render

def hello_world(request):
    return render(request, 'hello_world.html', {})""")
    # Creating base template and hello_world template
    os.system (f'mkdir {app_name}/templates/')
    os.system (f'mkdir {project_name}/templates/')

    os.system (f'touch {app_name}/templates/hello_world.html')
    os.system (f'touch {project_name}/templates/base.html')

    with open (project_name + '/templates/base.html', 'w') as f:
        f.write ('<!DOCTYPE html>\n<html>\n<body>\n{% block page_content %}{% endblock %}\n</body>\n</html>\n')

    with open (app_name + f'/templates/hello_world.html', 'w') as f:
        link_str = '<a href=' + '"'+ "{% " + "url '"+app_name+":hello_world' "+ "%}" +'"'+ "> Hello World Page </a>"

        form_html_str = "{% extends 'base.html' %}\n" + "{0}\n<h1>Hello, World!</h1>\n{1}\n{2}".format("{% block page_content %}",link_str,"\n{% endblock %}")
        f.write(form_html_str)

    with open (app_name + '/urls.py', 'w') as f:
        f.writelines (
            [f"from django.urls import path\nfrom . import views # Import/Change as per need \n\n\n", f"app_name = '{app_name}'\n\nurlpatterns = [ \n    path('', views.hello_world, name='hello_world'), "
                                                                                                               "\n ]  # Add URL & Views "
                                                                                                               "as per "
                                                                                                               "need"])
    with open (project_name + '/settings.py', 'a') as f:
        f.writelines (f"""\n\n# Base Template Dir Added, Change if Need.\nTEMPLATES[0]["DIRS"].append ('{project_name}/templates/')\n""")


def create_dummy_appmodels_in_app(app_name):
    # Create Dummy app Models

    dummy_model_name = app_name.capitalize ()
    with open (app_name + '/models.py', 'w') as f:
        f.writelines (f"""from django.db import models

class Item (models.Model):
    title = models.CharField (max_length=100)
    description = models.TextField ()
    technology = models.CharField (max_length=20)
    image = models.FilePathField (path="/img")""")


def register_appmodels_in_app(app_name):
    def depth_ast(root):
        return 1 + max (map (depth_ast, ast.iter_child_nodes (root)), default=0)

    # Registering app classes in project
    p = ast.parse (open (f"{app_name}/models.py", "r").read ())
    classes = [node.name for node in ast.walk (p) if isinstance (node, ast.ClassDef) and node.name != 'Meta']
    print (f'Registering Class: {classes} from app {app_name}')
    ls_to_write = []
    with open (app_name + '/admin.py', 'w') as f:
        ls_to_write.append (f"from django.contrib import admin\n")
        for item in classes:
            ls_to_write.append (f"from .models import {item}\n")
        ls_to_write.append (f"\n\n\n\n")
        for item in classes:
            ls_to_write.append (f"class {item}ModelAdmin(admin.ModelAdmin):\n    model = {item}\n")
        ls_to_write.append (f"\n\n\n\n")
        for item in classes:
            ls_to_write.append (f"admin.site.register({item}, {item}ModelAdmin)\n")

        f.writelines (ls_to_write)  # Add URL & Views as per need"])


def plug_appurls_and_app_in_project(project_name, app_name):
    register_app_in_project (apps_to_add=[app_name], project_name=project_name)

    # Add app urls to projects urls
    write = True
    with open (project_name + '/urls.py', 'r') as f:
        for line in f:
            # print(line.strip())
            if "from django.urls import include" == line.strip ():
                write = False
            if not write and f"urlpatterns.append(path('', include('{app_name}.urls')))" in line:
                return

    with open (project_name + '/urls.py', 'a') as f:
        if write:
            f.writelines (["\nfrom django.urls import include\n", f"urlpatterns.append(path('', include('{app_name}.urls')))\n"])
        else:
            f.writelines ([f"\nurlpatterns.append(path('', include('{app_name}.urls')))\n"])


def clear_dir(virtual_env, project_name, app_name):  # CLEAR DIR for fresh run
    print('Clearing ... ')
    try:
        shutil.rmtree (virtual_env)
    except:
        pass
    try:
        os.remove ('manage.py')
    except:
        pass
    try:
        os.remove ('db.sqlite3')
    except:
        pass
    try:
        os.remove ('nohup.out')
    except:
        pass
    try:
        shutil.rmtree (project_name)
    except:
        pass
    try:
        shutil.rmtree (app_name)
    except:
        pass


def set_new_project_new_app(virtual_env=VIR_ENV, app_name=APP_NAME):
    this_script = os.path.basename (__file__)
    vir_env_path = os.path.join (os.getcwd (), virtual_env)
    print(f"\n\nINFO:   Change PROJECT_NAME = {PROJECT_NAME}, APP_NAME = {APP_NAME} , given default values in {this_script} if need.\n\n")
    print (f'Create virtual env {virtual_env} and activate it. Choose 1 if you did it already.')

    choice = int (input ('1 or 0 ? '))
    if choice == 1:
        os.system (f'python3  {this_script} --stage create_project_and_app --appname {app_name}')
        os.system (f'python3 {this_script} --stage create_views --appname {app_name}')
        os.system (f'python3 {this_script} --stage create_models --appname {app_name}')
        os.system (f'python3 {this_script} --stage register_app_models_in_app_admin --appname {app_name}')
        os.system (f'python3 {this_script} --stage app_migrate --appname {app_name}')
        os.system (f'python manage.py check')

        os.system (f'python3 {this_script} --stage create_super_user --appname {app_name}')
        os.system (f'python3 {this_script} --stage run --appname {app_name}')
    else:
        os.system (f'python3  {this_script} --stage init --appname {app_name}')
        print (f'\n\nINFO:   Activate vir env {virtual_env} and Run: python3 {this_script} --new new\n\n')

def create_serializers(app_name):
    pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser ("Give stage count.")
    parser.add_argument ('-s', "--stage", help="Provide setup Stage to be executed.", type=str)
    parser.add_argument ('-a', "--appname", help="Provide app name.", type=str)
    parser.add_argument ('-n', "--new", help="Create new project , new app.", type=str) # e.g: python3 django_prepare_project_0.4.py --new new
    parser.add_argument ('-r', "--script", help="Provide script name as dir.filename_without_extension e.g: blog.scripts.etl", type=str)
    args = parser.parse_args ()

    # Create a total new proj with app
    if args.new == 'new':    # e.g: python3 django_prepare_project_0.4.py --new new
        os.system (f'chmod u+x {os.path.basename (__file__)}')
        set_new_project_new_app ()
        exit (0)

    if args.stage is None:
        print ('Plz provide setup stage e.g. python3 django_prepare_project.py --stage 1 --appname itemsapp')
        exit (0)

    if args.appname is None:
        print ('Plz provide appname e.g. python3 django_prepare_project.py --stage 1 --appname itemsapp')
        exit (0)

    APP_NAME = args.appname
    run_setup_stage = str (args.stage)
    script = str (args.script)

    # Init setups: ===>  ... OK ...
    if run_setup_stage == 'init':
        os.system (f'chmod u+x {os.path.basename (__file__)}')
        clear_dir (virtual_env=VIR_ENV, project_name=PROJECT_NAME, app_name=APP_NAME)  # CLEAR DIR for fresh run
        create_virtual_env (virtual_env_name=VIR_ENV)


    # Crates Project and app, add app, register app in projects settings  ===>  ... OK ...
    elif run_setup_stage == 'create_project_and_app':
        create_a_django_project_and_app (project_name=PROJECT_NAME, app_name=APP_NAME, virtual_env=VIR_ENV, requirements_file='requirements.txt')
        register_app_in_project (apps_to_add=add_apps + [APP_NAME], project_name=PROJECT_NAME)  # register default apps + new app in project settings
        add_app_urls_in_project_urls (app_name=APP_NAME, project_name=PROJECT_NAME)  # register app urls

    # Create dummy app views
    elif run_setup_stage == 'create_views':  # ===>  ... OK ...
        create_dummy_views (app_name=APP_NAME)
        print ('Dummy views creation done ... ')

    # Create dummy app models, after model creation, do register_app_models_in_admin
    elif run_setup_stage == 'create_models':  # ===>  ... OK ...
        create_dummy_appmodels_in_app (app_name=APP_NAME)
        print ('Dummy models creation done ... ')

    # Register app models in project  python3 django_prepare_project_0.4.py --stage register_app_models_in_app_admin --appname blog
    elif run_setup_stage == 'register_app_models_in_app_admin':  # ===>  ... OK ...
        register_appmodels_in_app (app_name=APP_NAME)

    # Make app migrations and do migrations, for whole project migration use --appname '' e,g:  python3 django_prepare_project_0.4.py --stage app_migrate --appname ''
    elif run_setup_stage == 'app_migrate':  # ===>  ... OK ...
        os.system ('python manage.py syncdata')
        os.system (f'python manage.py makemigrations {APP_NAME}')
        os.system ('python manage.py migrate')

    # Create super user
    elif run_setup_stage == 'create_super_user':  # ===>  ... OK ... e.g:   python3 django_prepare_project_0.4.py --stage create_super_user  --appname ''
        create_super_user ()

    # Run Project       e.g: python3 django_prepare_project_0.6.py --stage run  --appname ''
    elif run_setup_stage == 'run':  # ===>  ... OK ...
        os.system ('xterm -e nohup python manage.py livereload')  # Reload debug mode
        os.system ('python manage.py runserver')

    # Run ETL Script
    elif run_setup_stage == 'run_script':  # ===>  ... OK ...
        os.system (f'python manage.py runscript -v3 {script}')  # e.g: python3 django_prepare_project_0.6.py --stage run_script --appname '' --script blog.scripts.etl
