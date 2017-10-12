import bpy

bl_info = {"name": "My Render Test Addon", "category": "Render"}

def register():
    print("Hello World")
    bpy.utils.register_class(ColorItem)
    bpy.utils.register_class(UiPanel)
    bpy.utils.register_class(ExampleRenderEngine)

    bpy.types.Scene.color = bpy.props.PointerProperty(type=ColorItem)
    
def unregister():
    print("Goodbye World")
    bpy.utils.unregister_class(ExampleRenderEngine)
    bpy.utils.unregister_class(UiPanel)
    bpy.utils.unregister_class(ColorItem)
    del bpy.types.Scene.color

class ColorItem(bpy.types.PropertyGroup):
    color = bpy.props.FloatVectorProperty(
                 name = "Color Picker",
                 subtype = "COLOR",
                 size = 4,
                 min = 0.0,
                 max = 1.0,
                 default = (0.5,0.5,0.5,1.0)
                 )

class UiPanel(bpy.types.Panel):
    bl_label = "Render"
    bl_idname = "OBJECT_NAME"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Enter Number", icon='WORLD_DATA')

        row = layout.row()
        row.prop(context.scene.color, "color")

class ExampleRenderEngine(bpy.types.RenderEngine):
    bl_idname = 'TestRenderer'
    bl_label = "TestRenderer"
 
    def render(self,scene):
        sx = scene.render.resolution_x
        sy = scene.render.resolution_y

        result = self.begin_result(0, 0, sx, sy)
        layer = result.layers[0].passes["Combined"]      
        rect = [scene.color.color] * sx * sy
        layer.rect = rect
        self.end_result(result)