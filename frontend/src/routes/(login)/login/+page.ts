import type { PageLoad } from "./$types";
import { loginAuth } from "$lib/utils/auth.svelte";
import { getNotes, type NotePublic } from "@neonote/sdk";

export const load: PageLoad = async () => {
	await loginAuth();
};
