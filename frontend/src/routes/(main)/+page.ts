import type { PageLoad } from "./$types";
import { auth } from "$lib/utils/auth.svelte";
import { getNotes, type NotePublic } from "@neonote/sdk";

export const load: PageLoad = async () => {
	await auth();
	const data = await getNotes();
	return { data: data.data ? data.data.notes : new Array<NotePublic>() };
};
