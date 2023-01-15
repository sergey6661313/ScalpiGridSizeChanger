bl_info = {
    "name": "ScalpiGridSizeChanger",
    "author": "Scalpi",
    "version": (1, 2),
    "blender": (3, 3, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "just keys _ and = for resize gridmap",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

# settings
max_depth = 10
min_depth = -2

# ScalpiGridSizeChanger
import bpy
current_scale = 1


def get_scale():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            return area.spaces.active.overlay.grid_scale
            
def set_scale(new_scale):
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.overlay.grid_scale = new_scale

def update_scale():
    global current_scale
    new_scale = 1

    if current_scale > 1:
        for _ in range(current_scale - 1):
            new_scale = new_scale * 2
    elif current_scale < 1:
        for _ in range(1 - current_scale):
            new_scale = new_scale * 0.5

    set_scale(new_scale)
    

class ScalpiGridSizeChangerIncreaser(bpy.types.Operator):
    """increace grid size"""
    bl_idname = "object.scalpi_grid_size_changer_inc"
    bl_label = "ScalpiGridSizeChangerInc"

    def execute(self, context):
        global current_scale
        if current_scale > max_depth: return {'FINISHED'}
        current_scale += 1
        update_scale()
        return {'FINISHED'}


class ScalpiGridSizeChangerDecreaser(bpy.types.Operator):
    """decreace grid size"""
    bl_idname = "object.scalpi_grid_size_changer_dec"
    bl_label = "ScalpiGridSizeChangerDec"

    def execute(self, context):
        global current_scale
        if current_scale < min_depth: return {'FINISHED'}
        current_scale -= 1
        update_scale()
        return {'FINISHED'}

addon_keymaps = []

def register():
    bpy.utils.register_class(ScalpiGridSizeChangerIncreaser)
    bpy.utils.register_class(ScalpiGridSizeChangerDecreaser)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        print("key binded")
        km  = kc.keymaps.new(name= "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("object.scalpi_grid_size_changer_inc", type= 'EQUAL', value= 'PRESS', shift=False)
        addon_keymaps.append((km, kmi))
        
        km  = kc.keymaps.new(name= "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("object.scalpi_grid_size_changer_dec", type= 'MINUS', value= 'PRESS', shift=False)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(ScalpiGridSizeChangerIncreaser)
    bpy.utils.unregister_class(ScalpiGridSizeChangerDecreaser)

if __name__ == "__main__":
    register()
    



