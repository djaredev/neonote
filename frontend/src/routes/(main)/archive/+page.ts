import type { PageLoad } from "./$types";
import { auth } from "$lib/utils/auth.svelte";
import { getArchivedNotes, type NotePublic } from "@neonote/sdk";

export const load: PageLoad = async () => {
	await auth();
	const data = await getArchivedNotes();
	if (data.data) {
		return { data: data.data.notes };
	}
	return { data: new Array<NotePublic>() };
};
