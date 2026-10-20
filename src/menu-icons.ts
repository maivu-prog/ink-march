/** Transparent Blender renders share the actual troop materials and lighting. */
const emblem=(name:string)=>`<img class="menu-emblem menu-${name}" src="./assets/ui/menu-toys-v3/${name}.png" alt="" aria-hidden="true" draggable="false" width="64" height="64">`;
export const menuIcon={summon:emblem('summon'),brushes:emblem('brushes'),battle:emblem('battle'),squad:emblem('squad'),training:emblem('training')};
