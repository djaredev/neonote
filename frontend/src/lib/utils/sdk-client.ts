import { client, authclient } from "@neonote/sdk";
import { ensureAuthenticated } from "$lib/utils/auth.svelte";
import { handleHttpError } from "$lib/utils/middlewares";

export const API_URL = import.meta.env.VITE_API_URL;

export const setUpSDKClient = () => {
	authclient.setConfig({ baseUrl: API_URL });
	client.setConfig({ baseUrl: API_URL });
	client.interceptors.response.use(ensureAuthenticated);
	client.interceptors.error.use(handleHttpError);
};
