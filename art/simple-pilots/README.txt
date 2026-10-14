INK MARCH — APPROVED SIMPLE PILOTS

Models: sword (1,568 triangles, 9 meshes), goblin (1,508 triangles, 7 meshes).
Each GLB embeds one 512x512 palette texture and contains Idle, Walk, Attack, Death clips.
Art direction: rounded toy/bean bodies, short feet, simple expressive faces, large weapons.
Blender source: ink-march-simple-pilots.blend. Texture image is packed in the .blend and GLBs.
Generation source: ../blender/build_simple_pilots.py.
Reference concepts: ../concepts/sword_concept_simple.png and goblin_concept_simple.png.

Game integration chooses assets/models/simple/sword.glb and goblin.glb in models.ts,
and assets/portraits/simple/<id>.png in main.ts. The original model files are preserved.
Only the two approved pilot characters were updated. Current gameplay/UI changes are preserved.

Validation: production build, existing model/camera checks, and two new GLB checks passed.
Animation is articulated object-hierarchy animation, not a skinned skeleton or automatic image-to-3D conversion.
