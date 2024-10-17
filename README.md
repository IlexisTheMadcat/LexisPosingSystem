# LexisPosingSystem
Lexi's Posing System, also known as LPS, is a tool for VRChat avatars that allows users to carry and pose up to 3 clones of their avatar or other avatars they've created.
Unlike other takes on posing systems, this system uses _too many to count_ parameters to control a shared armature for the puppets. The parameters store information about the puppet transform data to allow persistence and various quality-of-life features.

Contents:
- [Quick Start](https://github.com/IlexisTheMadcat/LexisPosingSystem/tree/main?tab=readme-ov-file#quick-start)
- [Puppets with Modular Avatar stuff](...) still writing
- [Puppets with unsupported VRCFury](...) still writing
# Quick Start
LPS has a fairly simple setup process thanks to the required package [Modular Avatar](https://modular-avatar.nadena.dev/docs/intro). You can follow the instructions on that page to install Modular Avatar via the VRChat Creator Companion app. 
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
