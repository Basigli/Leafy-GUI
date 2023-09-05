def get_formatted_tags(base_path, filters=None, filter_func=None, only_historical=False):
	"""
	Retrieve all the tags starting from the path. It is also
	possible to specify filters.
	Note: it is possible to specify different "types" of
	filters. By default only the tags matching the filters
	are retrieved.
	
	Args:
		* base_path (str): base path from which we want
						   to start retrieving the tags
		* filters (list): list of filters to apply. If
						   not specified, then no filters
						   are applied
		* filter_func (func): function to apply to the filter.
							   By default the function is "equality"
							   The function should take 2 arguments:
							   the first is the full path, the second
							   is the filter value
		* only_historical (bool): only retrieve tags for which the
								   soricization is enabled
	
	Returns:
		Dict. Each element is a FormattedTag
	"""
	if filter_func is None:
		filter_func = lambda x, y: x == y
		
	def fits(full_path):
		if only_historical:
			cfg = system.tag.getConfiguration(full_path)[0]
			if not cfg.get('historyEnabled', False):
				return False
		if filters is None or len(filters) == 0:
			return True
		else:
			return all([filter_func(full_path, filt) for filt in filters])
	
	def get_tags(base_path):
		tree = {}
		for tag in system.tag.browse(base_path):
			full_path = str(tag['fullPath'])
			rel_path = full_path[full_path.index(base_path)+len(base_path):]
			name = str(tag['name'])
			is_folder = str(tag['tagType']) == 'Folder'
			
			if tag['hasChildren']:
				tree[name] = get_tags(full_path)
			else:
				if fits(full_path):
					tag_obj = frwk.framework.classes.FormattedTag(full_path, is_folder)
					tree[str(tag['name'])] = tag_obj
		return tree
	
	return get_tags(base_path)