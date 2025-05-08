import { getUser, setUser } from "$lib/state/user.svelte";
import { whoami } from "@neonote/sdk";
import { redirect } from "@sveltejs/kit";

export async function auth() {
	if (!getUser().username) {
		const res = await whoami();
		if (res.data) setUser(res.data);
	}

	if (!getUser().username) {
		redirect(302, "/login");
	}
}
