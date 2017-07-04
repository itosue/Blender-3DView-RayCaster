import bpy, bpy_extras.view3d_utils, mathutils.geometry

bl_info = {
	'name' : "3DView RayCaster",
	'author' : "saidenka",
	'version' : (1, 0),
	'blender' : (2, 7, 8),
	'location' : "3D View > Alt + MiddleMouseClick",
	'description' : "",
	'warning' : "",
	'wiki_url' : "",
	'tracker_url' : "",
	'category' : "3D View"
}

class view_ray_cast(bpy.types.Operator):
	bl_idname = 'view3d.view_ray_cast'
	bl_label = "Center View to Ray Cast"
	bl_description = "Center View to Ray Cast from Mouse Position"
	bl_options = set()
	
	@classmethod
	def poll(cls, context):
		try: context.scene, context.space_data, context.space_data.region_3d
		except: return False
		return True
	
	def invoke(self, context, event):
		self.mouse_region_position = (event.mouse_region_x, event.mouse_region_y)
		return self.execute(context)
	
	def execute(self, context):
		
		def click_to_3d(context, mouse_region_position):
			region, rv3d, coord = context.region, context.space_data.region_3d, mouse_region_position
			origin = bpy_extras.view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
			direction = bpy_extras.view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
			return origin, direction
		origin, direction = click_to_3d(context, self.mouse_region_position)
		
		is_succeeded, loc, no, i, ob, mat = context.scene.ray_cast(origin, direction)
		if is_succeeded:
			new_cursor_location = loc.copy()
		else:
			def get_best_cursor_location(context, origin, direction):
				pt = context.space_data.region_3d.view_location.copy()
				line_p1 = origin + (direction * -10000)
				line_p2 = origin + (direction * 10000)
				return mathutils.geometry.intersect_point_line(pt, line_p1, line_p2)[0]
			new_cursor_location = get_best_cursor_location(context, origin, direction)
		
		def temporary_view_center_cursor(new_loc):
			pre_loc, context.space_data.cursor_location = context.space_data.cursor_location.copy(), new_loc
			bpy.ops.view3d.view_center_cursor()
			context.space_data.cursor_location = pre_loc
		temporary_view_center_cursor(new_cursor_location)
		
		return {'FINISHED'}

addon_keymaps = []

def append_keymap_item():
	kc = bpy.context.window_manager.keyconfigs.addon
	if not kc: return
	km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
	kmi = km.keymap_items.new('view3d.view_ray_cast', 'MIDDLEMOUSE', 'PRESS', alt=True)
	addon_keymaps.append((km, kmi))

def remove_keymap_item():
	for km, kmi in addon_keymaps: km.keymap_items.remove(kmi)
	addon_keymaps.clear()

def register():
	bpy.utils.register_module(__name__)
	append_keymap_item()

def unregister():
	bpy.utils.unregister_module(__name__)
	remove_keymap_item()

if __name__ == '__main__':
	register()
