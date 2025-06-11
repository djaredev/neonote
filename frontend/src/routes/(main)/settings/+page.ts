import type { PageLoad } from "./$types";
import { auth } from "$lib/utils/auth.svelte";
import { redirect } from "@sveltejs/kit";

export const load: PageLoad = async () => {
	await auth();
	redirect(302, "/settings/account");
};
