<script lang="ts">
	import Button from "$lib/components/Button.svelte";
	import Field from "$lib/components/Field.svelte";
	import { updateUserMe, type UserUpdate } from "@neonote/sdk";
	import { userState } from "$lib/state/user.svelte";
	import { notify } from "$lib/state/notify.svelte";

	const account: UserUpdate = $state({
		username: userState.username,
		email: userState.email
	});

	const onsubmit = async () => {
		try {
			const res = await updateUserMe({
				body: {
					username: account.username !== userState.username ? account.username : undefined,
					email: account.email !== userState.email ? account.email : undefined
				}
			});

			if (res.data) {
				if (res.data.username !== userState.username) {
					notify.success("Updated username");
				}
				if (res.data.email !== userState.email) {
					notify.success("Updated email");
				}
				userState.set(res.data);
			}
		} catch {
			notify.error("Failed to update account");
		}
	};
</script>

<form {onsubmit} class="profile">
	<label for="username" class="label">Username</label>
	<Field id="username" type="text" bind:value={account.username} />
	<label for="email" class="label">Email</label>
	<Field id="email" type="email" bind:value={account.email} />
	{#if account.username === userState.username && account.email === userState.email}
		<Button type="submit" disable={true}>Save</Button>
	{:else}
		<Button type="submit">Save</Button>
	{/if}
</form>

<style>
	.profile {
		display: flex;
		flex-direction: column;
		gap: 10px;
		border: 1px solid #313244;
		border-radius: 8px;
		padding: 20px;

		.label {
			color: #a6adc8;
			text-align: left;
			padding: 2px;
		}

		:global(.button) {
			align-self: end;
		}
	}
</style>
