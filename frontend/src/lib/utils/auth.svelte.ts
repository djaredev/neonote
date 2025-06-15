import { userState } from "$lib/state/user.svelte";
import { whoami } from "@neonote/sdk";
import { redirect } from "@sveltejs/kit";

export async function auth() {
	if (!userState.username) {
		const res = await whoami();
		if (res.data) userState.set(res.data);
	}

	if (!userState.username) {
		redirect(302, "/login");
	}
}
export async function loginAuth() {
	if (!userState.username) {
		const res = await whoami();
		if (res.data) userState.set(res.data);
	}

	if (userState.username) {
		redirect(302, "/");
	}
}

