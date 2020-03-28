import subprocess, os
import bpy

class PasteStencil(bpy.types.Operator):
    """Paste system clipboard into a new stencil brush"""
    bl_idname = "brush.paste_stencil"
    bl_label = "Paste Stencil"

    def execute(self, context):
        png = subprocess.check_output([
          'xclip', 
          '-selection', 'clipboard', 
          '-target', 'image/png', 
          '-o']) 
        for count in range(10000):
            outPath = os.path.join(bpy.app.tempdir, 'paste-%d.png' % count)
            if not os.path.exists(outPath):
                break
        else:
            raise ValueError('out of filenames')
        with open(outPath, 'wb') as f:
            f.write(png)
        tx = bpy.data.textures.new('paste0', 'IMAGE')
        tx.image = bpy.data.images.load(outPath)
        print('loaded %s' % outPath)
        slot = bpy.data.brushes['TexDraw'].texture_slot
        slot.texture = tx
        slot.tex_paint_map_mode = 'STENCIL'
            
        return {"FINISHED"}


def register():
    bpy.utils.register_class(PasteStencil)

def unregister():
    bpy.utils.unregister_class(PasteStencil)

bl_info = {
    'name': 'Paste Stencil',
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "Brush",
    "category": "Paint",
}
    
if __name__ == "__main__":
    register()
    bpy.ops.brush.paste_stencil()
