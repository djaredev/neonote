import type { ClientInit, HandleClientError } from "@sveltejs/kit";
import { client } from "@neonote/sdk";
import { ensureAuthenticated } from "$lib/utils/auth.svelte";
import { handleHttpError } from "$lib/utils/middlewares";

export const init: ClientInit = async () => {
	client.interceptors.response.use(ensureAuthenticated);
	client.interceptors.error.use(handleHttpError);
};

export const handleError: HandleClientError = ({ error, event, status, message }) => {
	return {
		message: "Something went wrong. Please try again."
	};
};
