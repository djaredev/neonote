import type { ClientInit } from "@sveltejs/kit";
import { client } from "@neonote/sdk";
import { ensureAuthenticated } from "$lib/utils/auth.svelte";
import { handleError } from "$lib/utils/middlewares";

export const init: ClientInit = async () => {
	client.interceptors.response.use(ensureAuthenticated);
	client.interceptors.error.use(handleError);
};
