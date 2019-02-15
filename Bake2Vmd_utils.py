import bpy
import mmd_tools
import mmd_tools.core.model as mmd_model
import logging

class MMDPhysicsError(Exception):
    pass

def bakePhysics(self,context,start,end,step):
    root = mmd_model.Model.findRoot(context.active_object)
    if(root==None):
        self.report({'INFO'}, 'Not a MMD armature!')
    if(not root.mmd_root.is_built):
        self.report({'INFO'}, 'Physics is not built!')
        raise MMDPhysicsError('Physics Error')
        
    rig = mmd_model.Model(root)
    arm = rig.armature()
    rigidbodyGroup=[]
    boneGroup=[]
    rigidbodyGroup=rig.rigidBodies()
    bpy.ops.object.posemode_toggle()
    for rb in rigidbodyGroup:
        print(rb)
        boneGroup.append(rb.mmd_rigid.bone)
        bpy.ops.object.mode_set(mode='POSE')
        pbone=arm.data.bones.get(rb.mmd_rigid.bone, None)
        if(int(rb.mmd_rigid.type)==1 or int(rb.mmd_rigid.type)==2):
            pbone.select=True
    
    #bake it
    bpy.ops.nla.bake(frame_start=start \
    , frame_end=end \
    , step=step \
    , only_selected=True \
    , visual_keying=True \
    , clear_constraints=True \
    , clear_parents=False \
    , use_current_action=True \
    , bake_types={'POSE'})
    return { 'FINISHED' }