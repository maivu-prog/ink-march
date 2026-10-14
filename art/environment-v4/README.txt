INK MARCH - ENVIRONMENT V4

23 static GLBs in public/assets/models/env/. Authoring unit = one bean soldier's height (72 game units). Y-up, front +Z. Ground assets use base-centred pivots; ravines/cliffs use a surface anchor and extend below it.
Hill, plateau and ramp heights stay at or below 0.3 authoring units. The renderer raises troops and resamples ink to follow these surfaces.
8 seamless 512x512 textures; 6 transparent 128x128 terrain badges.
Generator: art/blender/build_environment_v4.py (reuses adjacent bean-v2 geometry/palette helpers). All visuals are generated locally in Blender; the .blend contains the complete editable asset set.
Regenerate: blender --background --factory-startup --threads 4 --python art/blender/build_environment_v4.py -- <game-project-root>
Review locally: /environment-review.html

Validation: production build passed; 58 asset/camera/surface tests plus 4 focused gameplay regressions passed. Live Camp Muster test won 3 stars (3/3 camps).
