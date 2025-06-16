import type { PageLoad } from "./$types";
import { auth } from "$lib/utils/auth.svelte";
import { getTrashedNotes, type NotePublic } from "@neonote/sdk";
import { request } from "$lib/utils/request";

export const load: PageLoad = async () => {
	await auth();
	const data = await getTrashedNotes();
	return { data: data.data ? data.data.notes : new Array<NotePublic>() };
};
