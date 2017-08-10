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
		try:
			context.space_data.cursor_location, context.space_data.region_3d.view_location
			if not bpy.ops.view3d.cursor3d.poll() or not bpy.ops.view3d.view_center_cursor.poll(): return False
		except: return False
		return True
	
	def execute(self, context):
		c_sd, c_upv = context.space_data, context.user_preferences.view
		pre_cursor_location, c_sd.cursor_location = c_sd.cursor_location.copy(), c_sd.region_3d.view_location.copy()
		pre_use_mouse_depth_cursor, c_upv.use_mouse_depth_cursor = c_upv.use_mouse_depth_cursor, True
		bpy.ops.view3d.cursor3d('INVOKE_DEFAULT'), bpy.ops.view3d.view_center_cursor('INVOKE_DEFAULT')
		c_sd.cursor_location, c_upv.use_mouse_depth_cursor = pre_cursor_location, pre_use_mouse_depth_cursor
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
