import bpy
from bpy.types import Panel, Menu, UIList
import traceback
from.import (Bake2Vmd_utils)

bl_info = {
    "name": "Bake2Vmd",
    "description": "Bake physics to MMD armature animation",
    "author": "Blade Sero",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > MMD Tools Panel",
    "warning": "",
    "wiki_url": "https://github.com/bladesero/bake2vmd/blob/master/README.md",
    "tracker_url": "https://github.com/bladesero/bake2vmd/issues",
    "category": "Object" 
    }

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )   

# ------------------------------------------------------------------------
#    store properties in the active scene
# ------------------------------------------------------------------------
class BakePhysicsSettings(bpy.types.PropertyGroup):
    start_frame: bpy.props.IntProperty(name="Start Frame",description="The baking progress start frame",default = 1)
    end_frame: bpy.props.IntProperty(name = "End Frame",description="The baking progress end frame",default = 120)
    frame_step: bpy.props.IntProperty(name = "Frame Step",description="The baking progress frame step(more steps more deviations)",default = 1)

# ------------------------------------------------------------------------
#    operators
# ------------------------------------------------------------------------
class Bake2Vmd(bpy.types.Operator):
    bl_idname = "bake2vmd.bake"
    bl_label = "Bake Animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    start = IntProperty(default=1)
    end = IntProperty(default=120)
    step = IntProperty(default=1)
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        try:
            Bake2Vmd_utils.bakePhysics(self, context, self.start, self.end, self.step)
        except Exception as e:
            err_msg = traceback.format_exc()
            self.report({'ERROR'}, err_msg)
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    panel
# ------------------------------------------------------------------------
class HelloWorldPanel(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Bake to Vmd"
    bl_idname = "OBJECT_bakevmd"
    bl_space_type = 'VIEW_3D'
    bl_category = "MMDExtra"
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        obj = context.object
        toolprops=context.scene.bakevmd_settings

        row = layout.row()
        if(obj.type == 'ARMATURE'):
            row.label(text="Now bakeable!", icon='FILE_TICK')
            row = layout.row()
            row.label(text="Active object is: " + obj.name, icon='ARMATURE_DATA')
            row = layout.row()
            row.prop(toolprops, "start_frame")
            row.prop(toolprops, "end_frame")
            row = layout.row()
            row.prop(toolprops, "frame_step")
            row = layout.row()
            bakeButton = row.operator("bake2vmd.bake")
            bakeButton.start=toolprops.start_frame
            bakeButton.end=toolprops.end_frame
            bakeButton.step=toolprops.frame_step
        else:
            row.label(text="Please select MMD armature!", icon='ERROR')
            row = layout.row()
            row.label(text="Active object is: " + obj.name, icon='OBJECT_DATA')

# ------------------------------------------------------------------------
#    register
# ------------------------------------------------------------------------
def register():
    bpy.utils.register_class(BakePhysicsSettings)
    bpy.utils.register_class(Bake2Vmd)
    bpy.utils.register_class(HelloWorldPanel)
    bpy.types.Scene.bakevmd_settings = bpy.props.PointerProperty(type=BakePhysicsSettings)

def unregister():
    bpy.utils.unregister_class(BakePhysicsSettings)
    bpy.utils.unregister_class(Bake2Vmd)
    bpy.utils.unregister_class(HelloWorldPanel)
    del bpy.types.Scene.bakevmd_settings

if __name__ == "__main__":
    register()
