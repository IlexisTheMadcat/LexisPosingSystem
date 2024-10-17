# LexisPosingSystem Documentation
Lexi's Posing System, also known as LPS, is a tool for VRChat avatars that allows users to carry and pose up to 3 clones of their avatar or other avatars they've created.
Unlike other takes on posing systems, this system uses _too many to count_ parameters to control a shared armature for the puppets. The parameters store information about the puppet transform data to allow persistence and various quality-of-life features.

Contents:
- [Quick Start](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#quick-start)
- [Usage](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#usage)
- - [Menus](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#menus)
  - - [Lexi's Posing System](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#lexis-posing-system)
    - [Settings](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#settings)
    - [Saving](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#saving)
    - [Rotation](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#rotation)
    - [Hands & Eyes](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#hands--eyes)
    - [Eyes](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#eyes)
  - Rotation Gadgets - still writing
  - Physbone Gadgets - still writing
- Important: Puppets with Modular Avatar stuff - still writing
- Important: Puppets with unsupported VRCFury - still writing
  
# Quick Start
LPS has a fairly simple setup process thanks to the required package [Modular Avatar](https://modular-avatar.nadena.dev/docs/intro). You can follow the instructions on that page to install Modular Avatar via the VRChat Creator Companion app. \
Please install this onto a copy of your avatar so that you can attend public worlds without lagging everyone in the instance.
1) Drag the prefab from the installation's Prefab folder into your avatar.
   ![Image 1](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/LPS-Readme1.png)
2) Duplicate the whole avatar and remove LPS from it. \
   Rename the copy to "Puppet Avatar" and the face to "Body" if you'd like to use the MMD facials feature. \
   Remove all components from the Puppet Avatar object as they won't be needed.
   ![Image 2](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/LPS-Readme2rev1.png)
4) Remove anything that doesn't contribute to the appearance of the avatar. \
   This is expanded on further down, but generally, an avatar that doesn't have any special tools should be useable as is.
5) Move this new puppet to the puppet slot as shown below and set its position to 0,0,0.
   ![Image 3](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/LPS-Readme3.png)
6) For the respective puppet slot, match the bone names for the calibration armature and the puppet merge target armature. **Do NOT use the merge function here!** \
   You may have to expand these armatures and check for bones that didn't get renamed properly. These can include some or all finger bones and sometimes eye bones. 
   ![Image 4](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/LPS-Readme4.png)
7) Ensure the puppet is in T-Pose, then calibrate the posing system. If the puppet is _not_ in T-Pose, move the upper arms and shoulders if needed until they are parallel with the x-axis. The posing system assumes the puppet is in T-Pose.
   ![Image 5](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/LPS-Readme5.png)
8) Revert the armature components. If you miss this, the posing system may not build properly even if the merge is not locked or is turned off.
   ![Image 6](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/LPS-Readme6.png)
9) After confirming that the components above are reverted, attach an MA Merge Armature component to your new puppet's armature.
   ![Image 7](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/LPS-Readme7.png)
10) Now link it to LPS. It is important that you set this to NOT LOCKED if you need to calibrate anything again, otherwise the puppet will mess itself up.
    ![Image 8](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/LPS-Readme8rev1.png)
11) To finalize the setup, link the posing system to your player avatar. \
    There are 4 mini-steps shown here.
    ![Image 9](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/LPS-Readme9.png)
You can now press play to test the posing system. If your avatar has special components like Modular Avatar or VRCFury anywhere in its hierarchy, continue reading to resolve potential issues.

# Usage
When you load into a world, you will experience a large lag spike as everything loads in. This is normal.
## Menus
### Lexi's Posing System
![Menu 1](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/action%20menu/LPS-Menu1.png)
1) Enable the system. When turned off, all puppets are hidden. It doesn't offer a great performance boost though.
2) Drop the currently selected puppet. It will retain this position until undropped.
3) Rotate joints on the puppet.
4) Move the puppet in its own XYZ local space. Useful for getting to hard-to-reach or mid-air spots.
5) Scale the puppet.
6) Operate the MMD facials of the puppet.
7) Operate the fingers and eyes of the puppet.
8) Settings including puppet selection.
### Settings
![Menu 2](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/action%20menu/LPS-Menu2.png)
1) Reset the puppet to T-Pose. Applies to rotation, scale, and translation.
2) Show a rig of blue bones that you grab to move the bones.
3) Show a rig of gadgets that show which directions a joint will move and their bounds.
4) Save the puppet's pose for future use.
5) Gradually increase this radial to make the puppet follow the player avatar's pose.
6) Select a puppet and toggle it on or off individually. Repeat Quick Start with puppets 2 and 3 to utilize this.
### Saving
![Menu 3](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/action%20menu/LPS-Menu4.png)
1) Begin saving a pose. Click one of the three slots to save. **WILL NOT ASK FOR CONFIRMATION.**
2) Begin loading a pose. Click one of the three slots to load. **WILL NOT ASK FOR CONFIRMATION.**
3) Slot 1.
4) Slot 2.
5) Slot 3. \
Must click either save or load for slots to do anything.
### Rotation
![Menu 4](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/action%20menu/LPS-Menu6.png)
1) Joint children.
2) XYZ joint rotation. The root rotation menu is the Hips and will rotate the entire puppet.
### Hands & Eyes
![Menu 5](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/action%20menu/LPS-Menu7.png)
1) Left/Right hands. Includes submenus for each finger. Each finger has a joint control for the three joints and a sideways movement called "spread".
2) Left/Right hand presets. Utilize this and save a lot of time in posing by choosing a preset best for the occasion. You can pose after presetting.
3) Eyes.
### Eyes
![Menu 6](https://raw.githubusercontent.com/IlexisTheMadcat/LexisPosingSystem/refs/heads/main/readme%20images/action%20menu/LPS-Menu8.png)
1) Right eye XY rotation.
2) Left eye XY rotation. \
Z is not included because eyes don't normally rotate.
