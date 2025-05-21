import { type NotePublic } from "@neonote/sdk";
export const notes = $state({
	notes: new Array<NotePublic>()
});
