def add_recent_actions(request, key):
	
	if not 'recent_actions' in request.session or not request.session['recent_actions']:
		request.session['recent_actions'] = [[str(key), str( request.get_full_path())]]
	else:
		saved_list = request.session['recent_actions']
		 
		value  =  [str(key), str( request.get_full_path())]

		if value in saved_list:
			print(">>>>>>>>>>>>>>>>>>>>>>> value ",value   )
			saved_list.remove(value)
		else:
			print(">>>>>>>>>>>>>>>>>>>>>>> value not ", value ,saved_list  )


		saved_list.append(value)
		saved_list.reverse()
		request.session['recent_actions'] = saved_list


class AddRecentActionMixin:
	action_key=None

	def dispatch(self, *args, **kwargs):
		if self.get_action_key():
			add_recent_actions(self.request,self.get_action_key() )
		return super().dispatch(*args, **kwargs) 

	def get_action_key(self):
		return self.action_key