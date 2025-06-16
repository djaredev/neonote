import { goto } from "$app/navigation";
import { userState } from "$lib/state/user.svelte";
import { whoami, authclient } from "@neonote/sdk";
import { redirect } from "@sveltejs/kit";

export async function auth() {
	if (!userState.username) {
		const res = await whoami({ client: authclient });
		if (res.data) userState.set(res.data);
	}

	if (!userState.username) {
		redirect(302, "/login");
	}
}

export async function loginAuth() {
	if (!userState.username) {
		const res = await whoami({ client: authclient });
		if (res.data) userState.set(res.data);
	}

	if (userState.username) {
		redirect(302, "/");
	}
}

export const isUnauthorizedError = (status: number): boolean => {
	if (status == 401 || status == 403) {
		return true;
	}
	return false;
};

export const logout = () => {
	userState.clear();
	goto("/login");
};

export const ensureAuthenticated = (response: Response) => {
	if (isUnauthorizedError(response.status)) {
		logout();
	}
	return response;
};
