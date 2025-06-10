import type { PageLoad } from "../profile/$types";
import { auth } from "$lib/utils/auth.svelte";

export const load: PageLoad = async () => {
	await auth();
};
