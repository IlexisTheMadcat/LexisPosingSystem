# LexisPosingSystem Documentation
Lexi's Posing System, also known as LPS, is a tool for VRChat avatars that allows users to carry and pose up to 3 clones of their avatar or other avatars they've created.
Unlike other takes on posing systems, this system uses _too many to count_ parameters to control a shared armature for the puppets. The parameters store information about the puppet transform data to allow persistence and various quality-of-life features. \
This posing system can be purchased here: https://ilexisthemadcat.booth.pm/items/6215800

Community Server: https://discord.gg/ilexissloft \
Please stop by if you have any questions about setup or want to suggest something. Select Lexi's Assets in onboarding and scroll down the channels for #💬lexis-posing-system!

LPS version updates will be announced in the Discord server. Known bugs or planned features will be represented as open issues in this repository.

Contents:
- [Quick Start](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#quick-start)
- [Usage](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#usage)
  - [Menus](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#menus)
    - [Lexi's Posing System](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#lexis-posing-system)
    - [Settings](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#settings)
    - [Saving](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#saving)
    - [Rotation](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#rotation)
    - [Hands & Eyes](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#hands--eyes)
    - [Eyes](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#eyes)
  - [Rotation Gadgets](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#rotation-gadgets)
  - [Physbone Gadgets](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#physbone-gadgets)
  - [Move Gadget](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#move-gadget)
- [Advanced Setup](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#advanced-setup)
  - [Puppets with Modular Avatar](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#puppets-with-modular-avatar) (Important)
  - [Puppets with unsupported VRCFury](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#puppets-with-unsupported-vrcfury) (Important)
  - [Manual Calibration](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#manual-calibration)
  - [Gadget Scaling](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#gadget-scaling) (Important if the puppet is big or small)
  - [FX Layer Cloning](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#fx-layer-cloning)

# Quick Start
LPS has a fairly simple setup process thanks to the required package [Modular Avatar](https://modular-avatar.nadena.dev/docs/intro). You can follow the instructions on that page to install Modular Avatar via the VRChat Creator Companion app. \
Please install this onto a separate copy of your avatar so that you can attend public worlds without lagging everyone in the instance.
1) Drag the prefab from the installation's Prefab folder into your avatar.
   ![image](https://github.com/user-attachments/assets/4d46eb41-2956-406c-b49c-9176c6ab0735)
2) Duplicate the whole avatar and remove LPS from it. \
   Rename the copy to "Puppet Avatar" and the face to "Body" if you'd like to use the MMD facials feature. \
   Remove all components from the Puppet Avatar object as they won't be needed.
   ![image](https://github.com/user-attachments/assets/645fa450-ac6b-4565-bb7b-60c26cb063fc)
3) Remove anything that doesn't contribute to the appearance of the avatar. \
   This is expanded on further down, but generally, an avatar that doesn't have any special tools should be useable as is.
4) Move this new puppet to the puppet slot as shown below and set its position to 0,0,0.
   ![image](https://github.com/user-attachments/assets/55179e4c-48f6-46fc-a659-ddeacff93949)
5) For the respective puppet slot, match the bone names for the calibration armature and the puppet merge target armature. **Do NOT use the merge function here!** \
   You may have to expand these armatures and check for bones that didn't get renamed properly. These can include some or all finger bones and sometimes eye bones. 
   ![image](https://github.com/user-attachments/assets/4957fb73-fcef-4c9b-a323-4ffbde47ed23)
6) Ensure the puppet is in T-Pose, then calibrate the posing system. If the puppet is _not_ in T-Pose, move the upper arms and shoulders if needed until they are parallel with the x-axis. The posing system assumes the puppet is in T-Pose upon build.
   ![image](https://github.com/user-attachments/assets/eed7c274-1a09-4269-a175-78f0b8908895)
   - Review [Manual Calibration](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#manual-calibration) and [Gadget Scaling](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#gadget-scaling) for some customization.
7) Revert the armature components. If you miss this, the posing system may not build properly even if the merge isn't locked or is turned off.
   ![image](https://github.com/user-attachments/assets/e776ecb1-3b0c-4f10-aabb-e74db1a5d16c)
8) After confirming that the components above are reverted, attach an MA Merge Armature component to your new puppet's armature.
   ![image](https://github.com/user-attachments/assets/e7f1efdd-19b0-465c-a32b-d54137f08a85)
9) Now link it to LPS. It is important that you set this to NOT LOCKED if you need to calibrate anything again, otherwise the puppet will mess itself up.
    ![image](https://github.com/user-attachments/assets/5d302225-46d1-47f7-ac00-fd5f0ec83515)
10) To finalize the setup, link the posing system to your player avatar. \
    There are 4 mini-steps shown here.
    ![image](https://github.com/user-attachments/assets/c394a864-1153-4919-983a-1dbf448402f5)
11) ![image](https://github.com/user-attachments/assets/fbfe872b-efb2-4e01-bfa7-9e7727b43f8f) As of v1.1.0, the Menu Pointer object was added. Position this exactly where you placed your VRC viewpoint, then activate the constraint. This pointer allows you to look at a joint and edit it on demand using just one page in the Rotation menu. Adjust the length of the contact under this object to suit your needs. \
    ![image](https://github.com/user-attachments/assets/09b04bc6-1b91-4363-aa43-03c3b35c9603)

13) Cleanup time! Search "Cylinder 1 (approx)" in the hierarchy search bar and turn all those off to hide the approximation preview handles on the player model as they aren't used. To hide (or unhide) the system, toggle the "Puppet Avatar Container" object. The system will not automatically toggle on things that aren't supposed to be toggled off. If you have Gesture Manager installed via VCC, you can press play to test the posing system. If your avatar has special components like Modular Avatar or VRCFury anywhere in its hierarchy, check important notes in the [contents](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#lexisposingsystem-documentation) to resolve potential issues.

# Usage
When you load into a world, you will experience a large lag spike as everything loads in. This is normal.
## Menus
### Lexi's Posing System
![image](https://github.com/user-attachments/assets/48665cc2-5331-465c-9c8f-fef6486b5307)
1) Enable the system. When turned off, all puppets are hidden. It doesn't offer a great performance boost though.
2) Drop the currently selected puppet. It will retain this position until undropped.
3) Rotate joints on the puppet.
4) Move the puppet in its own XYZ local space. Useful for getting to hard-to-reach or mid-air spots.
5) Scale the puppet.
6) Operate the MMD facials of the puppet.
7) Operate the fingers and eyes of the puppet.
8) Settings including puppet selection.
### Settings
![image](https://github.com/user-attachments/assets/4580f738-5c4e-48b7-8b5b-4807ffa43092)
1) Reset the puppet to T-Pose. Applies to rotation, scale, and translation.
2) ![image](https://github.com/user-attachments/assets/fbfe872b-efb2-4e01-bfa7-9e7727b43f8f) Show and enable a rig of ball joints that you can look at to control them via the Rotation menu. Initializes enabled when on desktop.
   - Video showcase: [Ilexis Nakamori @ Twitter/X](https://x.com/IlexisTheMadcat/status/1889223329443410112)
3) Show a rig of blue bones that you can grab to move the bones. Initializes enabled when loaded in VR.
   - Image showcase: [Ilexis Nakamori @ Twitter/X](https://x.com/IlexisTheMadcat/status/1826079313751330868)
4) Show a rig of gadgets that show which directions a joint will move and their bounds.
   - ⚠️ Warning: This option induces a heavy drop in graphics performance. It is not meant to be on all the time.
6) Save the puppet's pose for future use.
7) Gradually increase this radial to make the puppet follow the player avatar's pose.
   - Video showcase: [Ilexis Nakamori @ Twitter/X](https://x.com/IlexisTheMadcat/status/1830530510415646992)
8) Select a puppet and toggle it on or off individually. Repeat Quick Start with puppets 2 and 3 to utilize this.
   - Video showcase: [Ilexis Nakamori @ Twitter/X](https://x.com/IlexisTheMadcat/status/1844836318800384248)
### Saving
![image](https://github.com/user-attachments/assets/78630688-ae48-49bf-b839-224588e8fcbe) \
This feature lets you save poses to your avatar's saved settings. These aren't transferrable between avatars or to/from test builds.
1) Begin saving a pose. Click one of the three slots to save. **WILL NOT ASK FOR CONFIRMATION.**
2) Begin loading a pose. Click one of the three slots to load. **WILL NOT ASK FOR CONFIRMATION.**
3) Slot 1.
4) Slot 2.
5) Slot 3. 
- Must click either save or load for slots to do anything.
- Video showcase: [Ilexis Nakamori @ Twitter/X](https://x.com/IlexisTheMadcat/status/1830112245851779523)
### Rotation
![image](https://github.com/user-attachments/assets/84316260-098c-4008-bb19-3e2e8f5a385f)
1) Joint children.
2) Selected joint name, appears in the center via Rich Text in-game. Has no menu function.
- The first submenu of the Rotation menu controls the joint you are looking directly at, if you have Aim Joint Gadgets enabled.
3) ![image](https://github.com/user-attachments/assets/fbfe872b-efb2-4e01-bfa7-9e7727b43f8f) Twist the joint, if applicable.
4) ![image](https://github.com/user-attachments/assets/fbfe872b-efb2-4e01-bfa7-9e7727b43f8f) Pivot the joint.
5) Manual XYZ joint rotation. The Hips rotation menu will rotate the entire puppet.
- Some joints do not have all of XYZ or have both controllers because they don't move in those directions. 
### Hands & Eyes
![image](https://github.com/user-attachments/assets/70652e51-02c9-4fdc-a31e-1a65d50dbac7)
1) Left/Right hands. Includes submenus for each finger. Each finger has a joint control for the three joints and a sideways movement called "spread".
2) Left/Right hand presets. Utilize this and save a lot of time in posing by choosing a preset best for the occasion. You can pose after presetting.
3) Eyes.
### Eyes
![image](https://github.com/user-attachments/assets/dae6f163-648f-46dd-ba29-e3231594a84c)
1) Right eye XY rotation.
2) Left eye XY rotation. 
- Z is not included because eyes don't normally twist.
## Rotation Gadgets
The rotation gadgets appear when you select Show All Gadgets in the settings menu or when you select a joint to rotate in the menu. \
![image](https://github.com/user-attachments/assets/f7f6789e-ec58-49f4-8418-800e061216ea) \
The Y axis is labeled, but the others are the same way, just in different colors.
1) Rotation cursor
2) Rotation bounds
3) Rotation guide ring
- In LPS, rotation is achieved by putting X, Y, and Z axes in hierarchical order. X moves XYZ, Y moves YZ, and Z only moves Z. This can be a bit quirky to manage for certain poses, but if you're in VR, you can use the physbone handles below.
- The rotation bounds show the bounds within which the bones can rotate. This posing system is designed to be anatomically accurate while also being forgiving and letting creativity go wild. 
## Physbone Gadgets
These blue bars represent the bones you can grab to pose the avatar. These can be hidden in the settings menu. \
![image](https://github.com/user-attachments/assets/b3f1c13d-78ba-43d7-a837-f949dd56c12b)
1) Polar handle, longer of the two. This pitches the joint along two leverage axes.
2) Twist handle, shorter of the two. This twists the joint along the twisting axis.
- You can grab polar and twist handles to automatically rotate the joint to your desired orientation. These let you move two or even all three axes simultaneously, making it much more practical to use in VR. The joints lag because the animator increments the parameters, limiting its ability to track the physbone handles instantly.
- Some joints, namely shoulders and toes, don't have twist handles because those bones can't twist.
## Move Gadget
This gadget lets you translate the puppet in its local space. \
![image](https://github.com/user-attachments/assets/d68972cc-59c8-4f90-929e-879b2ba2b689)
1) Grabbable ball
2) Pick-up contacts
3) Y axis
4) Z axis
5) X axis
- To translate the puppet, grab the middle ball and pull it towards an axis. If you have Axis Lock on, the ball will lock itself to the first axis you touch, granting easier control over its movement. This behavior is toggleable. When toggled off, it can move on all axes simultaneously. Due to the nature of VRChat's contacts, moving on the Z axis along with any other will be tricky. It's best to do \[XY] and \[Z] in separate motions.
- The gadget follows your head by default. You can drop it in the world to get it out of your way. If you want to move it in local or world space, make a fist at one of the endpoints. Unfist to drop the gadget.
- Video showcase: [Ilexis Nakamori @ Twitter/X](https://x.com/IlexisTheMadcat/status/1847747604659999004)
# Advanced Setup
## Puppets with Modular Avatar
If your puppet has any components that belong to Modular Avatar, please read this section.
1) **MA Merge Armature** \
   These components may need to be updated to fit the puppet's armature instead of the player model. If you neglect this step, the puppet's clothes will do ghostly things! \
   ![image](https://github.com/user-attachments/assets/67a73144-7a04-4d50-8052-43819c480c00)
2) **MA Blendshape Sync** \
   These components are still referencing your player model's objects. These generally don't need to be edited, but if you're making a static puppet that hasn't cloned your FX layer, or you've animated them independently from your own avatar, you can just delete these or fix their references. \
   ![image](https://github.com/user-attachments/assets/f849c0db-74d3-48b1-876c-1463d0a7ec5a)
3) **MA Bone Proxy**
   These components are still referencing the player model's objects. You'll need to dig through the puppet to find the bone it was targeting before. \
   ![image](https://github.com/user-attachments/assets/96a74c04-708e-4e3a-8a1b-b4a8bc8d80ad)
4) **Unwanted MA components**
   These components should be removed from the puppet avatar as they could interfere negatively with the upload process. \
   ![image](https://github.com/user-attachments/assets/0c062369-c0ed-432b-a1e9-701bb0f4d8eb) \
   All other Modular Avatar components should be fine as they are. \
## Puppets with VRCFury
VRCFury is not supported. It doesn't allow armatures to be linked to those apart from the player avatar, and it doesn't allow calibration in edit mode, making setup much more complicated and cumbersome. Attempting to include VRCFury components may lead to build issues as Modular Avatar and VRCFury fight over armatures and animations. \
![image](https://github.com/user-attachments/assets/9888d5e4-856b-40f8-86c6-5c639944c075)
## Manual Calibration
If your puppet is in a T-Pose and you calibrate and some joints look misaligned, You can go through the puppet's calibration armature and rotate these dongles to make fine adjustments to the rest positions of the T-Pose state. Whatever the case may be, the puppet's arms and shoulders must be straight and parallel to the X axis (LPS Y axis), while the legs are straight and parallel to the Y axis (LPS Z axis). Expand the calibration armature to reveal all dongles. Use the animation you saw in step 6 of the Quick Start guide to show the rotation gadgets. Don't record any new keyframes. \
![image](https://github.com/user-attachments/assets/1d81d9e0-58c5-4c13-bfaf-8866daf91a10)
## Gadget Scaling
If your avatar is relatively larger or smaller than LPS's default configuration, you may want to scale the provided gadgets. To do this, preview the animation for the puppet you want to scale the gadgets for, then change the scale of the Gadget Scale object under the respective puppet manipulator. \
![image](https://github.com/user-attachments/assets/c3bdd3a8-d55c-406f-bccd-324fc97b37bc)
## FX Layer Cloning
You can make your puppet an exact copy of your avatar at runtime. To do this, add the MA Merge Animator component to the Puppet Avatar object, then input your avatar's FX layer into the "Animator to merge" slot. The puppet should then react to all the toggles in your FX layer. \
![image](https://github.com/user-attachments/assets/acaaad33-e568-495c-adac-bc18de80396b)

# End
[Return to top](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#lexisposingsystem-documentation)
