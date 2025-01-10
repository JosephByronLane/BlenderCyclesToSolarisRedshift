import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)




################################

# shamelessly airlifted from 
# https://blender.stackexchange.com/questions/160859/is-there-a-way-to-display-a-multi-lines-message-in-panel-popup
# though i did edit it a little bit to suit my needs

###############################


# -------------------------------------------------------------------
#   Drawing
# -------------------------------------------------------------------

class CUSTOM_UL_items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.15)

        #if item.mat exists then output it if not "null"
        split.label(text=item.mat if item.mat else "null") # avoids renaming the item by accident

        #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        split.label(text=item.name) # avoids renaming the item by accident

    def invoke(self, context, event):
        pass   


class CUSTOM_OT_popup(Operator):
    bl_idname = "rfxutils.call_popup"
    bl_label = "There were warning while exporting materials"
    bl_options = {'REGISTER'}

    key: StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.rfxutils.json_saver('INVOKE_DEFAULT',key=self.key)

        return {'FINISHED'}

    def check(self, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=1000)

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene

        rows = 7
        row = layout.row()
        row.template_list("CUSTOM_UL_items", "", scn, "custom", scn, "custom_index", rows=rows)



# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class CUSTOM_objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    coll_type: StringProperty()
    coll_id: IntProperty()
    mat: StringProperty()

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    CUSTOM_UL_items,
    CUSTOM_objectCollection,
    CUSTOM_OT_popup
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # Custom scene properties
    bpy.types.Scene.custom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.custom_index = IntProperty()


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.custom
    del bpy.types.Scene.custom_index

