import type { ClientInit } from "@sveltejs/kit";
import { client } from "@neonote/sdk";
import { ensureAuthenticated } from "$lib/utils/auth.svelte";

export const init: ClientInit = async () => {
	console.log("init");
	client.interceptors.response.use(ensureAuthenticated);
};
