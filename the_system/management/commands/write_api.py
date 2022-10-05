from django.core.management.base import BaseCommand, CommandError
import os
from pick import pick
from pathlib import Path
import logging
logger = logging.getLogger('ilogger')
 
import inspect
from django.apps import apps

class Command(BaseCommand):
    """
        python manage.py write_api app_name model_name file_to_write
    
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
            with open(self.file_path,"a") as file:
                file.write(data)
                file.write("\n\n")

        else:
            print(data)

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def add_arguments(self, parser):
        parser.add_argument('app_name',   type=str)
        parser.add_argument('model_name',   type=str ,  )
        parser.add_argument('file_path',   type=str , nargs='?', default=None)
   
    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def handle(self, *args, **options):
        self.app_name = options.get('app_name', None)
        model_name = options.get('model_name', None)
        self.file_path =  options.get('file_path', None)
        try:
            app = apps.get_app_config(self.app_name)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"{e}"))
            return

        try:
            model  = app.get_model(model_name)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"{e}"))
            return

        # for field in model._meta.get_fields():
        #     self.stdout.write(self.style.SUCCESS(f"{field.name}"))
        
        self._write_serializer(model)

        selected_views,lookup_field = self._write_view(model)
        self._write_url(self.app_name,model.__name__,selected_views,lookup_field)
        # for app in apps.get_app_configs():
        #     self.stdout.write(self.style.SUCCESS(f"{app.verbose_name}"))
        #     for model in app.get_models():
        #         self.stdout.write(self.style.NOTICE(f"\t{model}"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _ask_fields_to_use(seld,model,title="Please select model fields", options = None,min_selection_count=1):
        field_name = options or [field.name for field in model._meta.get_fields()]
        selected = pick(field_name, title, multiselect=True, min_selection_count=min_selection_count)
 
        return [ field for field,index in selected]

    def _get_serializer_validation_method(self):
        return [f"\tdef validate(self, data):",
            "\t\tif data['serializer_field'] != 'valid':",
            "\t\t\t#raise serializers.ValidationError({'validation_failed':error_message})",
            "\t\t\tpass",
            f"\t\treturn data"

        ]
    def _get_validation_method(self,field_name):
        return [f"\tdef validate_{field_name}(self, {field_name}):",
            "\t\t#raise serializers.ValidationError(error_message)",
            f"\t\treturn {field_name}"

        ]
    
    def _write_serializer(self,model):

        self._print(f"# Writing serializer == START ==")

        serializer_fields = self._ask_fields_to_use(model,"Please select model fields for serializer")
        readonly_fields = self._ask_fields_to_use(model,"Please select readonly field",serializer_fields,min_selection_count=0)
        validation_fields = self._ask_fields_to_use(model,"Please select field for validation",serializer_fields,min_selection_count=0)

        model_name = model.__name__
        

     
        string = ['from rest_framework import  serializers',
        f"from {self.app_name}.models import {model_name}",
        "import logging",
        f"logger = logging.getLogger('ilogger')",
        f"class {model_name}Serializer(serializers.ModelSerializer):",
        f"\tclass Meta:",
        f"\t\tmodel = {model_name}",
        f"\t\tfields = ( ",
        ] 

        field_string=[]

        for field in serializer_fields:
            field_string.append(f"\t\t\t\t'{field}',")  

        
        string = string + field_string
        string.append("\t\t)")


        if not readonly_fields:
            string.append("\n\t\tread_only_fields=None # Need tuple")
        else:
            string.append("\n\t\tread_only_fields= ( ")
            field_string=[]

            for field in readonly_fields:
                field_string.append(f"\t\t\t\t'{field}',")  

            
            string = string + field_string
            string.append("\t\t)")


      

        for field in validation_fields:
            string.append("\n\n")
            string = string+self._get_validation_method(field)
        
        string.append("\n\n")
        string = string+self._get_serializer_validation_method( )
        #print(string)

        self._print("\n".join(string))

 
        self._print(f"# Writing serializer == FINISH ==")

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def effify(self,non_f_str: str):
        return eval(f'f"""{non_f_str}"""')

 

    def _ask_for_option_to_use(seld,options,title="Please select api view"  ):
 
        return pick(options, title )[0]

    def _ask_for_options_to_use(seld,options,title="Please select model fields",  min_selection_count=1):
 
        selected = pick(options, title, multiselect=True, min_selection_count=min_selection_count)
 
        return [ field for field,index in selected]


  
    def get_view_list(self):
        return [ ]


    def _write_view(self,model):
        
        fields =   [field.name for field in model._meta.get_fields()]

        # lookup_field = self._ask_for_view_to_use()
        

        selected_views = self._ask_for_options_to_use(self.get_view_list(),title="Please select api view" ,min_selection_count=0)
        lookup_field = self._ask_for_option_to_use(fields,"CreateAPIView: Please select look up field") or "pk"
        client_field= self._ask_for_option_to_use(fields,"CreateAPIView: Please select client field")  

        for view_name in selected_views:
            self._print(f"# Writing {view_name} == START ==")

            if view_name == "CreateAPIView":
                self._write_CreateAPIView(model,lookup_field,client_field,view_name)

            if view_name == "ListAPIView":
                self._write_ListAPIView(model,lookup_field,client_field,view_name)

            if view_name == "ListCreateAPIView":
                self._write_ListCreateAPIView(model,lookup_field,client_field,view_name)

            if view_name == "RetrieveAPIView":
                self._write_RetrieveAPIView(model,lookup_field,client_field,view_name)

            if view_name == "UpdateAPIView":
                self._write_UpdateAPIView(model,lookup_field,client_field,view_name)

            # if view_name == "GenericAPIView":
            #     self._write_GenericAPIView(model,lookup_field,client_field)
            
            
            self._print( f"# Writing {view_name} == FINISH ==")


            # if view_name == "RetrieveUpdateAPIView":
            #     self._write_RetrieveUpdateAPIView(model)



            # if view_name == "DestroyAPIView":
            #     self._write_DestroyAPIView(model,lookup_field,client_field)


            # if view_name == "RetrieveDestroyAPIView":
            #     self._write_RetrieveDestroyAPIView(model)



            # if view_name == "RetrieveUpdateDestroyAPIView":
            #     self._write_RetrieveUpdateDestroyAPIView(model)




 
        # current_dir = Path(__file__).resolve().parent
        # with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
        #     final_data = eval(f'f"""{template.readlines()}"""')
        #     print(final_data)
        return selected_views,lookup_field
    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_GenericAPIView(self,model,lookup_field,client_field,view_name):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__
        lookup_field = self._ask_for_option_to_use(fields,"Please select look up field") or "pk"


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_ListAPIView(self,model,lookup_field,client_field,view_name):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_ListCreateAPIView(self,model,lookup_field,client_field,view_name):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_RetrieveAPIView(self,model,lookup_field,client_field,view_name):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_RetrieveDestroyAPIView(self,model):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_RetrieveUpdateAPIView(self,model):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_RetrieveUpdateDestroyAPIView(self,model):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))


    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_UpdateAPIView(self,model,lookup_field,client_field,view_name):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_DestroyAPIView(self,model):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__
        lookup_field = self._ask_for_option_to_use(fields,"Please select look up field") or "pk"


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_CreateAPIView(self,model,lookup_field,client_field,view_name):
        fields =   [field.name for field in model._meta.get_fields()]
        model_name = model.__name__
        # lookup_field = self._ask_for_option_to_use(fields,"CreateAPIView: Please select look up field") or "pk"


        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/views/create_view.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def _write_url(self,app_name,model,selected_views,lookup_field):
        self._print(f"# Writing URL == START ==")
        url_paths = [ ]
        for view in selected_views:
            path_parm_needed = self._need_path_parm(view)

            path_name = view.replace("APIView","").lower()
            parameter = ""
            if path_parm_needed:
                if lookup_field=="uuid":
                    parameter =f"<uuid:uuid>/"
                else:
                    parameter =f"<{lookup_field}>/"

            path = f"path(\"{model.lower()}/{path_name}/{parameter}\", views_api.{model}{view}.as_view(), name=\"{path_name}\")"

            url_paths.append(f"\n{path}")

        url_paths = ",\t".join(url_paths)

        current_dir = Path(__file__).resolve().parent
        with open(os.path.join(current_dir,"code_templates/api/urls/base.txt")) as template:
            final_string= "\n".join(template.readlines())
            final_data = eval(f'f"""{final_string}"""')
            self._print(final_data.replace("\n\n","\n"))

        self._print(f"# Writing URL == FINISH ==")


    def _need_path_parm(self,view_name):
        needed_for =['UpdateAPIView',"RetrieveAPIView"]
        return view_name in needed_for