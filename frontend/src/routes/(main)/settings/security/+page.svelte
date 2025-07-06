<script lang="ts">
	import Button from "$lib/components/Button.svelte";
	import Field from "$lib/components/Field.svelte";
	import { updatePasswordMe, type UpdatePassword } from "@neonote/sdk";
	import { notify } from "$lib/state/notify.svelte";
	import handler from "$lib/utils/handler";

	const passwords: UpdatePassword = $state({
		current_password: "",
		new_password: ""
	});

	let confirmPassword = $state("");

	const onsubmit = handler(async () => {
		if (passwords.new_password !== confirmPassword) {
			notify.error("New password and confirm new password do not match");
			return;
		}
		const res = await updatePasswordMe({
			body: passwords
		});

		if (res.response.status === 204) {
			notify.success("Password updated");
		}
	});
</script>

<form {onsubmit} class="security">
	<div class="title">Change password</div>
	<label for="currentPassword" class="label">Current password</label>
	<Field id="currentPassword" type="password" bind:value={passwords.current_password} />
	<label for="newPassword" class="label">New password</label>
	<Field id="newPassword" type="password" bind:value={passwords.new_password} />
	<label for="conNewPassword" class="label">Confirm new password</label>
	<Field id="conNewPassword" type="password" bind:value={confirmPassword} />
	{#if passwords.current_password && passwords.new_password && confirmPassword}
		<Button>Update password</Button>
	{:else}
		<Button disabled>Update password</Button>
	{/if}
</form>

<style>
	.security {
		display: flex;
		flex-direction: column;
		gap: 10px;
		border: 1px solid #313244;
		border-radius: 8px;
		padding: 20px;

		.title {
			color: #a6adc8;
			font-size: 24px;
			font-weight: bold;
		}

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
