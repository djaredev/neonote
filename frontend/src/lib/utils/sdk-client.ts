import { client, authclient } from "@neonote/sdk";
import { ensureAuthenticated } from "$lib/utils/auth.svelte";
import { handleHttpError } from "$lib/utils/middlewares";
import { PUBLIC_DEV_API_URL, PUBLIC_PROD_API_URL, PUBLIC_ENVIRONMENT } from "$env/static/public";

export const API_URL = PUBLIC_ENVIRONMENT === "dev" ? PUBLIC_DEV_API_URL : PUBLIC_PROD_API_URL;

export const setUpSDKClient = () => {
	authclient.setConfig({ baseUrl: API_URL });
	client.setConfig({ baseUrl: API_URL });
	client.interceptors.response.use(ensureAuthenticated);
	client.interceptors.error.use(handleHttpError);
};
