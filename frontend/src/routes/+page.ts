import type { PageLoad } from "./$types";
import { auth } from "$lib/utils/auth.svelte";
import { getNotes, type NotePublic } from "@neonote/sdk";
import { notes } from "$lib/state/note.svelte";

export const load: PageLoad = async () => {
	await auth();

	// let viewNotes: Array<NotePublic> = [];

	async function loadata() {
		const res = await getNotes();

		if (res.data) {
			notes.notes = res.data.notes;
		}
	}

	await loadata();
	// return { viewNotes };
};
