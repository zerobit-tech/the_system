from pprint import pprint
from re import M
from django.core.management.base import BaseCommand, CommandError
import os
from pick import pick
from pathlib import Path
import logging
logger = logging.getLogger('ilogger')
from django.views import generic
import inspect
from django.apps import apps
from django.template.loader import render_to_string


def _write_to_file(file_path, string, mode="w"):
    with open(file_path,mode) as file:
        file.write(string)
        file.write("\n\n")

def _ask_for_option_to_use(options,title="Please select one"  ):

    return pick(options, title )[0]



def _ask_for_options_to_use(options,title="Please select model fields",  min_selection_count=1):
    new_options = options
    if '*ALL' not in options:
        new_options = options + ["*ALL"]

    selected = pick(new_options, title, multiselect=True, min_selection_count=min_selection_count)

    return_list = [ field  for field,index in selected]
    if '*ALL' in return_list:
        return_list =  options
    

    return [ item for item in return_list if not str(item).strip().startswith("*")]




class Command(BaseCommand):
    """
        python manage.py write_view app_name model_name file_to_write


        needed items:
        1. Template
        2. View
        3. URL
    
    """

    help = 'Create DRF Api for a given model'

 

    # def add_arguments(self, parser):
    #     parser.add_argument('new_project_name',   type=str)
    #     parser.add_argument('old_project_name',   type=str , nargs='?', default='BaseDjangoProject')
    #     parser.add_argument(
    #         '--commit',
    #         action='store_true',
    #         help='Commit the rename in files',
    #     )


    def _print(self, data):
        if self.file_path:
            with open(self.file_path,"w") as file:
                file.write(data)
                file.write("\n\n")

        else:
            print(data)

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def add_arguments(self, parser):
        parser.add_argument('app_name',   type=str, nargs='?', default=None)
        parser.add_argument('model_name',   type=str , nargs='?', default=None  )
   
   
        parser.add_argument(
            '--output',
            help='Output file path',
            nargs='?',
            type=str,
        )

        parser.add_argument(
                '--commit',
                action='store_true',
                help='Commit the rename in files',
            )
    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def handle(self, *args, **options):
        # pprint(options)
        self.app_name = options.get('app_name', None)
        self.model_name = options.get('model_name', None)
        self.file_path =  options.get('output', None)
        self.commit =  options.get('commit', False)


        if self.app_name is None:
            options = [app.verbose_name.lower() for app in apps.get_app_configs() if app.verbose_name.startswith("The")]
            self.app_name = _ask_for_option_to_use(options,"Please select app")

        try:
            self.app = apps.get_app_config(self.app_name)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"{e}"))
            return


        if self.model_name is None:
            options = [ model.__name__ for model in self.app.get_models()]
            self.model_name = _ask_for_option_to_use(options,f"Please select model in app {self.app_name}")



        try:
            self.model  = self.app.get_model(self.model_name)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"{e}"))
            return

        # for field in self.model._meta.get_fields():
        #     print(field.name , field , type(field))

        # return

        selected_views = self.ask_to_select_views()

        for view in selected_views:
            if view.upper() == "LISTVIEW":
                self._print(ListView(self.app,self.model,view, self.commit).prepare_code())

            if view.upper() == "UPDATEVIEW":
                self._print(UpdateView(self.app,self.model,view, self.commit).prepare_code())

            if view.upper() == "DETAILVIEW":
                self._print(DetailView(self.app,self.model,view, self.commit).prepare_code())

            if view.upper() == "DELETEVIEW":
                self._print(DeleteView(self.app,self.model,view, self.commit).prepare_code())     

            if view.upper() == "CREATEVIEW":
                self._print(CreateView(self.app,self.model,view, self.commit).prepare_code())   

    def ask_to_select_views(self):
        """
         * ( ) ArchiveIndexView
            ( ) CreateView
            ( ) DateDetailView
            ( ) DayArchiveView
            ( ) DeleteView
            ( ) DetailView
            ( ) FormView
            ( ) ListView
            ( ) MonthArchiveView
            ( ) RedirectView
            ( ) TemplateView
            ( ) TodayArchiveView
            ( ) UpdateView
            ( ) View
            ( ) WeekArchiveView
            ( ) YearArchiveView
        """
        options = self.get_view_list()
        selected_views = _ask_for_options_to_use(options,"Please select view(S) to write")

  

        return selected_views

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------

    def get_view_list(self):

        return ['CreateView','DeleteView','DetailView','ListView','UpdateView']
        return [ name for name, obj in inspect.getmembers(generic) if inspect.isclass(obj) and name.endswith("View")]

 

 
 



  

     
 
 
 

# -------------------------------------------------------------------------------------------
class ListView:
    def __init__(self, app,model , view_name, commit) -> None:
        self.app = app
        self.model = model
        self.view_name = view_name

        self.app_name = app.verbose_name
        self.model_name = model.__name__    


        self.current_dir = Path(__file__).resolve().parent
        self.code = []
        self.template_suffix ="_list"
        self.commit = commit


    def is_choice_field(self, field_name):
        try:
            field = self.model._meta.get_field(field_name)
            return True if field.choices else False
        except:
            return False

    def prepare_code(self):
        self.get_select_fields()
        self.get_filter_fields()
        self.prepare_table_headings()
        self.prepare_table_data()
        self.write_template()
        self.write_filter()
        self.write_view()


        return "\n".join(self.code)

    def get_select_fields(self):
        options = [field.name for field in self.model._meta.get_fields()]
        self.selected_fields = _ask_for_options_to_use(options, f"Please select fields for {self.view_name }:")

        

        
    def get_filter_fields(self):
        options = self.selected_fields
        self.filter_fields = _ask_for_options_to_use(options, f"Please select filter fields for {self.view_name }:")
        self.filter_fields = ",".join([f"'{field}'" for field in self.filter_fields])

    def write_template(self):

        commit_file_path = os.path.join(self.app_name.lower(),"templates",self.app_name.lower(),f"{self.model_name.lower()}{self.template_suffix}.html" )


        self.code.append("#  writing template ========== start ====================\n\n")

        self._template_code = []
        STATIC_URL="{STATIC_URL}"
        with open(os.path.join(self.current_dir,f"code_templates/django/{self.view_name.lower()}/template.html")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self.code.append(final_data.replace("\n\n","\n").replace("#@","{{").replace("@#","}}"))
            self._template_code.append(final_data.replace("\n\n","\n").replace("#@","{{").replace("@#","}}"))
        self.code.append("#  writing template ========== end ====================\n\n\n\n")

        if self.commit:
            _write_to_file(commit_file_path, "\n".join(self._template_code))


    def write_filter(self):
        self.code.append("#  writing filter ========== start ====================\n\n")
        commit_file_path = os.path.join(self.app_name.lower(),"filters.py" )

        self._filter_code = []
        with open(os.path.join(self.current_dir,f"code_templates/django/{self.view_name.lower()}/filter.py")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self.code.append(final_data.replace("\n\n","\n"))
            self._filter_code.append(final_data.replace("\n\n","\n"))
        self.code.append("#  writing filter ========== end ====================\n\n\n\n")

        if self.commit:
            _write_to_file(commit_file_path, "\n".join(self._filter_code),mode="a")

    def write_view(self):
        self.code.append("#  writing View ========== start ====================\n\n")
        commit_file_path = os.path.join(self.app_name.lower(),"views.py" )

        _temp_code = []
        with open(os.path.join(self.current_dir,f"code_templates/django/{self.view_name.lower()}/view.py")) as template:
            final_string= "\n".join(template.readlines()).strip()
            final_data = eval(f'f"""{final_string}"""')
            self.code.append(final_data.replace("\n\n","\n"))
            _temp_code.append(final_data.replace("\n\n","\n"))

        self.code.append("#  writing view ========== end ====================\n\n\n\n")
        if self.commit:
            _write_to_file(commit_file_path, "\n".join(_temp_code),mode="a")


    def prepare_table_headings(self):
        """
        <th  class=" ">{% trans "provider" %}</th>
        """
        table_headings = []

        for field in self.selected_fields:
            heading = f"<th  class=\"\">{{% trans \"{field}\" %}}</th>"
            table_headings.append(heading)

        self.table_headings = "\n".join(table_headings)

    def prepare_table_data(self):
        """
        <td  class=" ">{{ smsmessage.provider }}  </td >
                                
                          
        """
        table_headings = []

        for field in self.selected_fields:
            if self.is_choice_field(field):
                field_val = f"{self.model_name.lower()}.get_{field}_display"

            else:
                field_val = f"{self.model_name.lower()}.{field}"

            field_val = "{"+field_val+"}"
            heading = f"<td  class=\"\">{{{field_val}}}</td >"
            table_headings.append(heading)

        self.table_data = "\n".join(table_headings)
        #print(self.table_data)



# -------------------------------------------------------------------------------------------
class  DetailView( ListView):
    """

    
    """

    def prepare_code(self):
        self.template_suffix ="_detail"
        self.get_select_fields()
        self.prepare_table_data()
        self.get_id_field()
        self.write_template()
        self.write_view()
        return "\n".join(self.code)

    def get_id_field(self):
        options = [field.name for field in self.model._meta.get_fields()]

        self.id_field = _ask_for_option_to_use(options, f"Please select id field   for {self.view_name }")
    def prepare_table_data(self):
        original_string = "<tr><td>{% blocktrans with title=\"{field_name}\"|fill_dots:30 %} {{title}}{% endblocktrans %}<strong> {{{field_value}}}</strong></td></tr>"
        table_headings = []

        for field in self.selected_fields:

            if self.is_choice_field(field):
                field_val = f"object.get_{field}_display"
            else:
                field_val = f"object.{field}"

            try:
                field_label= self.model._meta.get_field(field).verbose_name.title()
            except:
                field_label = field


            #print("original_string",original_string)
            #heading = original_string.format(field_name=field,field_value= field_val)
            heading = "<tr><td>{% blocktrans with title=\""+field_label+"\"|fill_dots:30 %} {{title}}{% endblocktrans %}<strong> {{"+field_val+"}}</strong></td></tr>"
            table_headings.append(heading)

        self.table_data = "\n".join(table_headings)
        #print(self.table_data)

# -------------------------------------------------------------------------------------------
class  DeleteView( DetailView):
    def prepare_code(self):
        self.template_suffix ="_confirm_delete"
        self.get_select_fields()
        self.prepare_table_data()
        self.get_id_field()
        self.write_template()
        self.write_view()
        return "\n".join(self.code)

# -------------------------------------------------------------------------------------------
class UpdateView(DetailView):
    """

    
    """

    def prepare_code(self):
        self.template_suffix ="_update_form"

        self.get_select_fields()
        self.get_clean_fields()
        self.prepare_clean_fields_method()
        self.get_id_field()
        self.write_template()
        self.write_form()
        self.write_view()
        return "\n".join(self.code)



    def get_clean_fields(self):
        self.clean_fields = _ask_for_options_to_use(self.selected_fields, f"Please select field for {self.view_name } clean method")

    def prepare_clean_fields_method(self):
        self.clean_field_methods = []

        for field in self.clean_fields:
            self.clean_field_methods.append(self.prepare_clean_field_method(field))

    def prepare_clean_field_method(self,field_name):
        with open(os.path.join(self.current_dir,f"code_templates/django/{self.view_name.lower()}/form_clean_field_method.py")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            return final_data.replace("\n\n","\n")

    def write_form(self):
        commit_file_path = os.path.join(self.app_name.lower(),"forms.py" )
        _temp_code = []
        self.code.append("#  writing form ========== start ====================\n\n")
        self.form_fields =  ",".join([f"'{field}'" for field in self.selected_fields])
        self.clean_field_methods = "\n".join(self.clean_field_methods)

        with open(os.path.join(self.current_dir,f"code_templates/django/{self.view_name.lower()}/forms.py")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self.code.append(final_data.replace("\n\n","\n"))
            _temp_code.append(final_data.replace("\n\n","\n"))

        self.code.append("#  writing form ========== end ====================\n\n\n\n")

 
        if self.commit:
            _write_to_file(commit_file_path, "\n".join(_temp_code),mode="a")

# -------------------------------------------------------------------------------------------
class CreateView(UpdateView):
    """

    
    """

    def prepare_code(self):
        self.template_suffix ="_add_form"
        self.get_select_fields()
        self.get_clean_fields()
        self.prepare_clean_fields_method()
   
        self.write_template()
        self.write_form()
        self.write_view()
        return "\n".join(self.code)
