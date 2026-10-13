// Tóm tắt thiết kế từng màn sau khi chạy solve-map: npx tsx tools/check-maps.ts [mapId...]
import {maps,BR} from '../src/systems';
const ids=process.argv.slice(2);
for(const m of Object.values(maps).filter(m=>!ids.length||ids.includes(m.id))){const d=(m as any).design||{};
 console.log(`${m.id.padEnd(7)} ${m.name.padEnd(22)} field ${m.field?.w}x${m.field?.h} · ${m.starts.length} squad(s) · ${m.bosses.length} boss · scale ${m.bosses[0].scale} · ink ${m.baseInk} · win ${d.winInk} · 3★ ${d.threeStarInk} (${d.threeStarBrush?BR[d.threeStarBrush].name:'?'})`);}
