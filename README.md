LPS: v1.2.1 \
LPS-OSC: v1.0.3 \
For LPS versions: v1.2.1
# LexisPosingSystem Documentation
Lexi's Posing System, also known as LPS, is a tool for VRChat avatars that allows users to carry and pose up to 3 clones of their avatar or other avatars they've created.
Unlike other takes on posing systems, this system uses _too many to count_ parameters to control a shared armature for the puppets. The parameters store information about the puppet transform data to allow persistence and various quality-of-life features. \
This posing system can be purchased here: https://ilexisthemadcat.booth.pm/items/6215800 \
Demo video: [[VRChat] Lexi's Posing System Demo (March 2025)](https://youtu.be/avXMTtn-ZQQ)

This posing system is meant for building to TEST! There will be absolutely NO NEED TO UPLOAD! Other people can't see what you're doing even on an uploaded build. Just move the LPS object off the avatar to upload updates to the avatar itself. Please note that VRChat still imposes hard component limits to test builds too. Your avatar will have to have under 92 physbone components to clone and build to test. Advanced setups can yield more room for physbones. 

Community Server: https://discord.gg/ilexissloft \
Please stop by if you have any questions about setup or want to suggest something. Select Lexi's Assets in onboarding and scroll down the channels for #storefront!

LPS version updates are announced on [Twitter/X](https://x.com/IlexisTheMadcat) and [BlueSky](https://bsky.app/profile/ilexisthemadcat.bsky.social). \
See [Statistics](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#statistics) at the bottom of this page for performance drop notices.

Contents: (Protip: [|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) takes you back here!)
- [Quick Start](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#quick-start)
  - [1) Drag prefab into scene](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#1-drag-prefab-into-scene)
  - [2) Duplicate avatar](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#2-duplicate-avatar)
  - [3) Remove excess objects](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#3-remove-excess-objects)
  - [4) Drag duplicate into LPS](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#4-drag-duplicate-into-lps)
  - [5) Match bone names](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#5-match-bone-names)
  - [6) Calibration](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#6-calibration)
  - [7) Reset calibrators](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#7-reset-calibrators)
  - [8) Attach MA Merge Armature](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#8-attach-ma-merge-armature)
  - [9) Link puppet to LPS](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#9-link-puppet-to-lps)
  - [10) Link LPS to avatar](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#10-link-lps-to-avatar)
  - [11) Position aim joint pointer](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#11-position-aim-joint-pointer)
  - [12) Clean up](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#12-clean-up)
- [Usage](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#usage)
  - [Menus](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#menus)
    - [Lexi's Posing System](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexis-posing-system)
    - [Settings](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#settings)
    - [Saving](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#saving)
      - [Folders](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#folders)
      - [Save slots](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#save-slots)
    - [Manipulation](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#manipulation)
    - [Rotation](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#rotation)
    - [Hands](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#hands)
    - [Eyes](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#eyes)
  - [Gadgets](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#gadgets)
    - [Rotation Gadgets](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#rotation-gadgets)
    - [Aim Joint Gadgets](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#aim-joint-gadgets)
    - [Physbone Gadgets](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#physbone-gadgets)
    - [Move Gadget](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#move-gadget)
- [Advanced Setup](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#advanced-setup)
  - [Puppets with Modular Avatar](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#puppets-with-modular-avatar) (Important)
  - [Puppets with unsupported VRCFury](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#puppets-with-vrcfury) (Important)
  - [Manual Calibration](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#manual-calibration)
  - [Gadget Scaling](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#gadget-scaling) (Important if the puppet is big or small)
  - [FX Layer Cloning](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#fx-layer-cloning)
    - [MMD Facials Note](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#mmd-facials-note)
- [Statistics](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#statistics)
- [OSC Program](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#osc-program)

# Quick Start
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Video guide: [LPS Installation](https://youtu.be/CJR3EyofTH4)

**LPS comes with a variant prefab that has VRChat's robot pre-loaded. If you just want to test the asset for now, skip to step 10!**

Start by duplicating your scene. You don't want to potentially mess up your main avatar. \
LPS has a fairly simple setup process thanks to the required package [Modular Avatar](https://modular-avatar.nadena.dev/docs/intro). You can follow the instructions on that page to install Modular Avatar via the VRChat Creator Companion app. 
### 1) Drag prefab into scene
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Drag the prefab from the installation's Prefab folder into your avatar.
![image](https://github.com/user-attachments/assets/4d46eb41-2956-406c-b49c-9176c6ab0735)
### 2) Duplicate avatar
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Duplicate the whole avatar and remove LPS from it. \
Rename the copy to "Puppet Avatar" and the face to "Body" if you'd like to use the MMD facials feature. See [MMD Facials Note](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#mmd-facials-note) \
Remove all components from the Puppet Avatar object as they won't be needed. \
![image](https://github.com/user-attachments/assets/645fa450-ac6b-4565-bb7b-60c26cb063fc)
### 3) Remove excess objects
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Remove anything that doesn't contribute to the appearance of the avatar. \
This is expanded on further down, but generally, an avatar that doesn't have any special tools should be useable as is.
### 4) Drag duplicate into LPS
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Move this new puppet to the puppet slot as shown below and set its position to 0,0,0. \
![image](https://github.com/user-attachments/assets/55179e4c-48f6-46fc-a659-ddeacff93949)
### 5) Match bone names
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) For the respective puppet slot, match the bone names for the calibration armature and the puppet merge target armature. **Do NOT use the merge function here!** \
You may have to expand these armatures and check for bones that didn't get renamed properly. These can include some or all finger bones and sometimes eye bones. \
![image](https://github.com/user-attachments/assets/4957fb73-fcef-4c9b-a323-4ffbde47ed23)
### 6) Calibration
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Ensure the puppet is in T-Pose, then calibrate the posing system. If the puppet is _not_ in T-Pose, move the upper arms and shoulders if needed until they are parallel with the x-axis. The posing system assumes the puppet is in T-Pose upon build. \
![image](https://github.com/user-attachments/assets/eed7c274-1a09-4269-a175-78f0b8908895)
- Review [Manual Calibration](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#manual-calibration) and [Gadget Scaling](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#gadget-scaling) for some customization.
### 7) Reset calibrators
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Revert the armature components. This is important!! If you miss this, the posing system may not build properly or the puppets' offsets could get recalculated every time it's updated (which is very bad). \
![image](https://github.com/user-attachments/assets/e776ecb1-3b0c-4f10-aabb-e74db1a5d16c)
### 8) Attach MA Merge Armature
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) After confirming that the components above are reverted, attach an MA Merge Armature component to your new puppet's armature. \
![image](https://github.com/user-attachments/assets/e7f1efdd-19b0-465c-a32b-d54137f08a85)
### 9) Link puppet to LPS
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Now link it to LPS. It is important that you set this to NOT LOCKED if you need to calibrate anything again, otherwise the puppet will mess itself up. \
Also you should unlock it before you preview calibrations. If it's still locked and you preview, your puppet's joints may misplace themselves. \
![image](https://github.com/user-attachments/assets/5d302225-46d1-47f7-ac00-fd5f0ec83515)
### 10) Link LPS to avatar
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) To finalize the setup, link the posing system to your player avatar. \
There are 4 mini-steps shown here. \
![image](https://github.com/user-attachments/assets/c394a864-1153-4919-983a-1dbf448402f5)
### 11) Position aim joint pointer
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) The Menu Pointer object was added in v1.1.0. Position this exactly where you placed your VRC viewpoint, then activate the constraint. This pointer allows you to look at a joint and edit it on demand using just one page in the Rotation menu. Adjust the length of the contact under this object to suit your needs. \
![image](https://github.com/user-attachments/assets/09b04bc6-1b91-4363-aa43-03c3b35c9603)
### 12) Clean up
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Cleanup time! Search "Cylinder 1 (approx)" in the hierarchy search bar and turn all those off to hide the approximation preview handles on the player model as they aren't used. To hide (or unhide) the system, toggle the "Puppet Avatar Container" object. The system will not automatically toggle on things that aren't supposed to be toggled off. If you have Gesture Manager installed via VCC, you can press play to test the posing system. If your avatar has special components like Modular Avatar or VRCFury anywhere in its hierarchy, check important notes in the [contents](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) to resolve potential issues. __Build and Test__ in the VRChat SDK to use the posing system!

# Usage
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) When you load into a world, you will experience a large lag spike as everything loads in. This is normal. \
Please do not load an LPS avatar in a public or group instance (test builds are local so this shouldn't matter). It is recommended to load in a private instance. No one can see your LPS progress unless you use VRChat's VRC+ print out camera or share your screen/stream camera.
## Menus
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Menu items are described in counter-clockwise order from the top. \
In v1.1.0, some new icons were introduced after documentation was edited. Some menu icons shown here may not match exactly with the final product.
### Lexi's Posing System
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Main menu of LPS. \
![image](https://github.com/user-attachments/assets/759a5e97-1f04-44fd-a7c8-38a5aa5bb639)
- [Settings](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#settings)
- [Finger joints](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#hands)
- [Eye gaze controls](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#eyes)
- MMD Face controls
- Select and scale the puppet
- [Manipulate the puppet](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#manipulation)
- Drop the puppet
- Enable the puppet
### Settings
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Control various parts of LPS. \
![image](https://github.com/user-attachments/assets/bc890386-dff1-4f95-ad39-1cff5f83d267)
- Hold for 2 seconds to reset the pose.
- Press and hold to carry all puppets, release to drop all. This is to make multi-puppet scene setup more convenient.
- Gradually increase this radial to make the puppet follow the player avatar's pose. [(Video)](https://x.com/IlexisTheMadcat/status/1830530510415646992)
- [Saving](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#saving) (OSC-exclusive)
- Show a rig of [rotation gadgets](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#rotation-gadgets) that show which directions a joint will move and their bounds.
- Show a rig of [blue bones](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#physbone-gadgets) that you can grab to move the bones. Initializes enabled when in VR.
- Show and enable a rig of [ball joints](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#aim-joint-gadgets) that you can look at to control them via the [Manipulation](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#manipulation) menu. Initializes enabled when on desktop.
### Saving
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Using the [OSC Program](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#osc-program), this lets you import and export poses into JSON format. Each folder follows the same [save slots](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#save-slots) format, with each one having a different set of slot numbers.
#### Folders
![image](https://github.com/user-attachments/assets/f210486a-de7f-47b8-8227-3682709792ba)
- For hand saves, off: left hand, on: right hand
- Pose saves (includes ALL joint rotations and MMD controls)
- Hand saves (includes all finger joints.)
- Face saves (includes MMD controls)
- Scene saves include pose and [local translation](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#move-gadget) data for all 3 puppets.
#### Save slots
![image](https://github.com/user-attachments/assets/497520a3-72f5-49a6-9c76-8d3ccb47e7e1)
- Begin saving a pose. Click one of the three slots to save.
- Begin loading a pose. Click one of the three slots to load.
- 6x: Save slots. Press and hold for 2 seconds to load or save. You'll see it happen when the save/load icon turns off.
   - When save or load are not selected, when held, these buttons preview their respective save slot. The working pose will be restored when released.
   - Scenes currently cannot be previewed, but you can press undo on each affected puppet to restore its previous pose.
### Manipulation
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Manipulate the puppet, including [local translation](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#move-gadget), [aim joint control](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#aim-joint-gadgets) and [bone rotation](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#rotation). Most of the submenus are similar to this one and follow a standard layout. \
![image](https://github.com/user-attachments/assets/e44c241c-6fb0-4f40-83ae-9d52131d544b)
- Undo (OSC-exclusive)
- Submenu/bone name
- Pivot the joint
- Twist the joint, if applicable
- [Move the puppet](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#move-gadget)
- [Rotation](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#rotation)
- Enable to freeze the aim joint tracker
- Redo (OSC-exclusive)
### Rotation
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Rotate the joints of your puppets. \
![image](https://github.com/user-attachments/assets/9a6c58b2-f31f-4423-94fc-7eed63ad473e)
- Undo (OSC-exclusive)
- Selected joint name, manual XYZ joint rotation. The Hips rotation menu will rotate the entire puppet.
- Pivot the joint
- Twist the joint, if applicable
- Right joint child
- Middle joint child
- Left joint child
- Redo (OSC-exclusive)
### Hands
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Control the fingers of each hand. \
![image](https://github.com/user-attachments/assets/fcb118ab-3643-4269-b147-71a80720dbed)
- Undo (OSC-exclusive)
- Copy Right to Left
- Right hand presets
- Right hand fingers
- Left hand fingers
- Left hand fingers
- Copy Left to Right
- Redo (OSC-exclusive)
### Eyes
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Eye submenu. \
![image](https://github.com/user-attachments/assets/55c3db93-3266-4b8c-b946-0408192b685e)
- Undo (OSC-exclusive)
- Copy Right to Left
- Right eye X rotation
- Right eye Y rotation
- Left eye Y rotation
- Left eye X rotation
- Copy Left to Right
- Redo (OSC-exclusive)
## Gadgets
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) LPS includes various gadgets to enable various posing methods and views.
### Rotation Gadgets
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) The rotation gadgets appear when you select Show All Gadgets in the settings menu or when you select a joint to rotate in the menu. \
![image](https://github.com/user-attachments/assets/f7f6789e-ec58-49f4-8418-800e061216ea) \
The Y axis is labeled, but the others are the same way, just in different colors.
1) Rotation cursor
2) Rotation bounds
3) Rotation guide ring
- In LPS, rotation is achieved by putting the X, Y, and Z axes in hierarchical order. X moves XYZ, Y moves YZ, and Z only moves Z. This can be a bit quirky to manage for certain poses, but if you're in VR, you can use the physbone handles below.
- The rotation bounds show the bounds within which the bones can rotate. This posing system is designed to be anatomically accurate while also being forgiving and letting creativity go wild. 
### Aim Joint Gadgets
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) The aim joint gadgets are blue balls that glow when you look at them. \
When the ball is glowing, you can edit the joint it's attached to with the rotation menu. You can also lock it to look away without deselecting it. \
Video showcase: [Ilexis Nakamori @ Twitter/X](https://x.com/IlexisTheMadcat/status/1889223329443410112) \
![image](https://github.com/user-attachments/assets/1c33209b-578e-4815-b0fc-c8f7ab526cc8)
### Physbone Gadgets
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) These blue bars represent the bones you can grab to pose the avatar. These can be hidden in the settings menu. \
![image](https://github.com/user-attachments/assets/b3f1c13d-78ba-43d7-a837-f949dd56c12b)
1) Polar handle, longer of the two. This pitches the joint along two leverage axes.
2) Twist handle, shorter of the two. This twists the joint along the twisting axis.
   - Some joints, namely shoulders and toes, don't have twist handles because those bones can't twist.
- You can grab polar and twist handles to automatically rotate the joint to your desired orientation. These let you move two or even all three axes simultaneously, making it much more practical to use in VR. The joints lag because the animator increments the parameters, limiting its ability to track the physbone handles instantly. 
### Move Gadget
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) This gadget lets you translate the puppet in its local space. \
Video showcase: [Ilexis Nakamori @ Twitter/X](https://x.com/IlexisTheMadcat/status/1847747604659999004) \
![image](https://github.com/user-attachments/assets/d68972cc-59c8-4f90-929e-879b2ba2b689)
1) Grabbable ball
2) Pick-up contacts
3) Y axis
4) Z axis
5) X axis
- To translate the puppet, grab the middle ball and pull it towards an axis. If you have Axis Lock on, the ball will lock itself to the first axis you touch, granting easier control over its movement. This behavior is toggleable. When toggled off, it can move on all axes simultaneously. Due to the nature of VRChat's contacts, moving on the Z axis along with any other will be tricky. It's best to do \[XY] and \[Z] in separate motions.
- The gadget follows your head by default. You can drop it in the world to get it out of your way. If you want to move it in local or world space, make a fist at one of the endpoints. Unfist to drop the gadget.
# Advanced Setup
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Important and/or helpful notes when setting up LPS.
## Puppets with Modular Avatar
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) If your puppet has any components that belong to Modular Avatar, please read this section.
### Manual bake avatar
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) Modular Avatar comes with a feature that lets you bake all of its components into a _copy_ of your avatar. Everything this feature does to your avatar is done on a duplicate of your avatar, and all merged files are in their own folder that you can find by looking for its playable layers/parameters asset/etc in the created avatar descriptor. \
To start, right-click your avatar with Modular Avatar components, expand Modular Avatar, and click "Manual bake avatar". This will perform the actions described above. \
![image](https://github.com/user-attachments/assets/cd39d053-30e4-4ca3-8fae-54d9b4abeb38) \
You can use the FX layer and parameters created by baking in the [FX Layer Cloning](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#fx-layer-cloning) section.
### No baking
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) If you don't want to bother with baking, you can look through these and make sure they're set up right. If the puppet isn't working right on build, try baking.
1) **MA Merge Armature** \
   These components may need to be updated to fit the puppet's armature instead of the player model. If you neglect this step, the puppet's clothes will do ghostly things! \
   ![image](https://github.com/user-attachments/assets/67a73144-7a04-4d50-8052-43819c480c00)
2) **MA Blendshape Sync** \
   These components are still referencing your player model's objects. These generally don't need to be edited, but if you're making a static puppet that hasn't cloned your FX layer, or you've animated them independently from your own avatar, you can just delete these or fix their references. \
   ![image](https://github.com/user-attachments/assets/f849c0db-74d3-48b1-876c-1463d0a7ec5a)
3) **MA Bone Proxy** \
   These components are still referencing the player model's objects. You'll need to dig through the puppet to find the bone it was targeting before. \
   ![image](https://github.com/user-attachments/assets/96a74c04-708e-4e3a-8a1b-b4a8bc8d80ad)
4) **Unwanted MA components** \
   These components should be removed from the puppet avatar as they could interfere negatively with the upload process. \
   ![image](https://github.com/user-attachments/assets/c5379e19-0be4-45c3-abfc-449f15a30de9) \
   If your puppet has any of these, check if their path mode is set to Absolute. If so, override the root to the Puppet Avatar object. \
   ![image](https://github.com/user-attachments/assets/54351a0c-6e12-461f-a936-048d19fe3f5a) \
   All other Modular Avatar components should be fine as they are.
## Puppets with VRCFury
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) VRCFury is not supported. It doesn't allow armatures to be linked to those apart from the player avatar, and it doesn't allow calibration in edit mode, making setup much more complicated and cumbersome. Attempting to include VRCFury components may lead to build issues as Modular Avatar and VRCFury fight over armatures and animations. \
![image](https://github.com/user-attachments/assets/9888d5e4-856b-40f8-86c6-5c639944c075)
## Manual Calibration
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) If your puppet is in a T-Pose and you calibrate and some joints look misaligned, You can go through the puppet's calibration armature and rotate these dongles to make fine adjustments to the rest positions of the T-Pose state. Whatever the case may be, the puppet's arms and shoulders must be straight and parallel to the X axis (LPS Y axis), while the legs are straight and parallel to the Y axis (LPS Z axis). Expand the calibration armature to reveal all dongles. Use the animation you saw in step 6 of the Quick Start guide to show the rotation gadgets. Don't record any new keyframes. \
![image](https://github.com/user-attachments/assets/1d81d9e0-58c5-4c13-bfaf-8866daf91a10)
## Gadget Scaling
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) If your avatar is relatively larger or smaller than LPS's default configuration, you may want to scale the provided gadgets. To do this, preview the animation for the puppet you want to scale the gadgets for, then change the scale of the Gadget Scale object under the respective puppet manipulator. \
![image](https://github.com/user-attachments/assets/c3bdd3a8-d55c-406f-bccd-324fc97b37bc)
## FX Layer Cloning
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) You can make your puppet an exact copy of your avatar at runtime. To do this, add the MA Merge Animator component to the Puppet Avatar object, then input your avatar's FX layer into the "Animator to merge" slot. The puppet should then react to all the toggles in your FX layer. \
![image](https://github.com/user-attachments/assets/acaaad33-e568-495c-adac-bc18de80396b) \
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) If you are choosing to set up a different avatar as your puppet, also add the MA Parameters component and insert the avatar's parameters asset into the "Parameters to merge" slot. This will import all of those parameters into the component. To save parameter space which you may need to do to upload, uncheck "Synced" for all of the parameters. No one can see the puppet anyway. \
![image](https://github.com/user-attachments/assets/e4f4f386-000e-4332-8037-9498efd4f663)
### MMD Facials Note
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) If your puppet does NOT have _MMD dedicated_ facial blendshapes, LPS will overwrite your FX layer gesture values with the MMD values, which will reset whatever custom idle face you've made in-game. To disable this behavior and the MMD controls for this puppet, simply rename your Puppet Avatar object to anything else. The more advanced solution is to use Blender to duplicate (create new from mix) blendshapes and rename the blendshapes you intend to use for gestures, as LPS only animates Japanese MMD blendshapes. \
If you want to add Japanese MMD blendshapes to your model, you may use [this MMD facials chart](https://www.deviantart.com/xoriu/art/MMD-Facial-Expressions-Chart-341504917) as your reference.
# Statistics
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) LPS takes up a lot of an avatar's maximum allowed number of VRC Physbones and Contacts, so it's better to clone, or build your clone on, a simpler avatar. \
Physbones: 37/256 \
Contacts: 168/256

Constraints take a good bit of CPU to run. VRChat released optimized constraints so the effect is not as bad, but all of these constraints are required for LPS to function and aren't there just to be lazy. \
VRC Constraints: 305 total 
- Parent constraints: 242
- Rotation constraints: 62
- Scale constraints: 1

Recommended Hardware:
- CPU: AMD Ryzen 7 5800X/X3D / Intel Core i7-11700K
- GPU: NVidia GTX 3060 / AMD 6600-XT

World: [Minesweeper](https://vrchat.com/home/world/wrld_48f47d66-8686-4fe9-92d5-ab4a00068b68/info) \
FPS drop on recommended hardware: ~130 -> ~45

Needless to say, LPS is not optimized. But for what it can do, and its intended purpose in photography, I'd say it's still worth it. \
Also, LPS is meant to be installed on a copy of your avatar and not on your primary upload, so you'll be able to choose when LPS is present.

# OSC Program
[|^|](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation) An OSC program is available for download in Releases. It extends the posing system's ability to save and load pose data with JSON files. It lets you transfer your saves anywhere, you can share with friends or communities, and it allows using save information on test builds! You no longer have to upload your LPS builds to save pose data. The program will automatically connect to a running instance of LPS and switch the system from local to OSC mode. 
- LPS can communicate with the OSC program to save pose parameters to json files. It also supports saving just the hands and just the faces separately with their own save slots allocated.
  - To load a file into a save slot, navigate to the directory in the config file ("`.../Documents/Lexi's Posing System`" by default) and move the json file into a slot folder. If that directory doesn't exist, try previewing an empty save slot and it will be created. The file can be named whatever, the program will read it. It will not read multiple files in the slot folder, only one of them. If a file is not in that folder, LPS can generate one once saving to it. If there *is* one in the folder, LPS will overwrite it without warning! You can check if a file is loaded in that slot by turning off saving/loading and clicking a save slot, beginning a quick peek preview.
  - File saves are categorized into 4 folders: Poses, Faces, Hands, and Scenes, with their indicators being 0 (`.lpspose`), 1 (`.lpsface`), 2 (`.lpshand`), and 3 (`.lpsscene`) respectively. The save type will be displayed at the beginning of the json file. LPS-OSC will refuse to load files with mismatched indicators. If you force the indicator to match, it may not load properly!
<img width="1040" height="360" alt="image" src="https://github.com/user-attachments/assets/6de9e9a8-0a1e-470b-b5d8-affdd4cf035f" />
  
# End
[Return to top](https://github.com/IlexisTheMadcat/LexisPosingSystem/blob/main/README.md#lexisposingsystem-documentation)
