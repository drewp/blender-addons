import bpy
from mathutils import Vector

class AddTrackCornersOperator(bpy.types.Operator):
    bl_idname = 'clip.add_track_corners'
    bl_label = 'Add track corners'
    bl_description = 'Create new tracks that follow the corners of the active track.'
    bl_options = {'REGISTER', 'UNDO'}

    dense_fill = bpy.props.BoolProperty(
        name="Dense fill",
        description='Make 8 points (corners and half-edges) instead of just 4',
        default=False,
    )

    @classmethod
    def _tracks(cls, context):
        clip = context.space_data.clip
        if clip:
            return clip.tracking.tracks
    
    @classmethod
    def poll(cls, context):
        tracks = AddTrackCornersOperator._tracks(context)
        if tracks:
            return tracks.active

    def _new_offset_marker(self, base_marker, norm_offset, track):
        co = base_marker.co + norm_offset
        return track.markers.insert_frame(base_marker.frame, co=co)

    def _new_track(self, tracks, name, frame):
        # wrong: always adds to camera, even if active track was
        # on another object
        return tracks.new(name, frame)

    def execute(self, context):
        tracks = self._tracks(context)
        track = tracks.active

        first_frame = min(m.frame for m in track.markers)
        for corner_index in range(4):
            new_track = self._new_track(tracks,
                                        '%s.%s' % (track.name, corner_index),
                                        first_frame)
            for marker in track.markers:
                corner = Vector(marker.pattern_corners[corner_index])
                self._new_offset_marker(marker, corner, new_track)
            print("added new track %s" % new_track.name)
        if self.dense_fill:
            for c1, c2 in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                new_track = self._new_track(tracks,
                                            '%s.%s-%s' % (track.name, c1, c2),
                                            first_frame)
                for marker in track.markers:
                    corner1 = Vector(marker.pattern_corners[c1])
                    corner2 = Vector(marker.pattern_corners[c2])
                    self._new_offset_marker(marker,
                                            corner1.lerp(corner2, .5), new_track)
                print("added new dense track %s" % new_track.name)
                    
        return {'FINISHED'}
        
def register():
   bpy.utils.register_module(__name__)
  
def unregister():
    bpy.utils.unregister_module(__name__)
  
if __name__ == '__main__':
    register()

