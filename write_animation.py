import bpy
from pathlib import Path

bl_info = {
    "name": "Write animation",
    "blender": (2, 91, 0),
    "location": "Render > Write animation",
}


class WriteAnimation(bpy.types.Operator):
    """Write a new webm next to the blend file"""
    bl_idname = "render.write_animation" # Unique identifier for buttons and menu items to reference.
    bl_label = "Write animation" # Display name in the interface.
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if not bpy.data.filepath.replace('.', ''):
            raise ValueError('Please save the file somewhere first.')
        output_base = Path(bpy.data.filepath.replace('.blend', ''))
        for num in range(1, 1000):
            output_path = Path(f'{output_base}_{num}.webm')
            if output_path.exists():
                continue
            break
        else:
            raise NotImplementedError()

        render = context.scene.render

        render.filepath = str(output_path)
        render.image_settings.file_format = 'FFMPEG'
        render.ffmpeg.format = 'WEBM'
        render.ffmpeg.codec = 'WEBM'
        render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
        render.image_settings.color_mode = 'RGBA'
        bpy.ops.render.render('INVOKE_DEFAULT', animation=True)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(WriteAnimation)


def unregister():
    bpy.utils.unregister_class(WriteAnimation)


if __name__ == "__main__":
    register()
