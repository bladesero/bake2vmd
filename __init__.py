import bpy
import traceback
from bake2vmd import Bake2Vmd_utils

bl_info = {
    "name": "Bake2Vmd",
    "description": "Bake physics to MMD armature animation",
    "author": "Blade Sero",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "Properties > Object",
    "warning": "This is an unstable version",
    "wiki_url": "https://github.com/bladesero/bake2vmd/blob/master/README.md",
    "tracker_url": "https://github.com/bladesero/bake2vmd/issues",
    "category": "Object" }

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
class BakePhysicsSettings(PropertyGroup):
    
    start_frame = IntProperty(
        name = "Start Frame",
        description="The baking progress start frame",
        default = 1,
        )
        
    end_frame = IntProperty(
        name = "End Frame",
        description="The baking progress end frame",
        default = 120,
        )
    
    frame_step = IntProperty(
        name = "Frame Step",
        description="The baking progress frame step(more steps more deviations)",
        default = 1,
        )

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
class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Bake to Vmd"
    bl_idname = "OBJECT_bakevmd"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        toolprops=context.scene.bakevmdToolProps

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
    bpy.utils.register_module(__name__)
    bpy.types.Scene.bakevmdToolProps = PointerProperty(type=BakePhysicsSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.bakevmdToolProps