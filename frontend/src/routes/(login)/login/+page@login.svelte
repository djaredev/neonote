<script lang="ts">
	import { goto } from "$app/navigation";
	import Button from "$lib/components/Button.svelte";
	import Field from "$lib/components/Field.svelte";
	import { userState } from "$lib/state/user.svelte";
	import { CircleXIcon, XIcon } from "@lucide/svelte";
	import { authclient, login, type BodyLoginLoginPost } from "@neonote/sdk";
	import { slide } from "svelte/transition";
	import neonote from "$lib/icons/neonote.svg";

	const body: BodyLoginLoginPost = $state({
		username: "",
		password: ""
	});

	let error: unknown = $state("");
	async function onsubmit() {
		try {
			const res = await login({
				client: authclient,
				body: body
			});
			if (res.data) {
				userState.set(res.data);
				goto("/");
			} else if (res.error.detail) {
				error = res.error.detail as unknown;
			}
		} catch {
			error = "An error occurred, please try again";
		}
	}
</script>

<div class="header">
	<img src={neonote} alt="Icono" width="50" height="50" />
</div>
<div class="container">
	<form class="login-form" {onsubmit}>
		<div class="login-header">
			<h2>Login to Neonote</h2>
			{#if error}
				<div class="login-error" transition:slide={{ duration: 200 }}>
					<CircleXIcon />
					{error}
					<button type="button" class="login-error-close" onclick={() => (error = "")}>
						<XIcon size={16} />
					</button>
				</div>
			{/if}
		</div>
		<div class="login-body">
			<Field placeholder="Username" id="username" type="text" required bind:value={body.username} />
			<Field
				placeholder="Password"
				id="password"
				type="password"
				required
				bind:value={body.password}
			/>
			<Button type="submit">Login</Button>
		</div>
	</form>
</div>

<style>
	* {
		box-sizing: border-box;
	}

	.header {
		position: fixed;
		padding: 10px;
	}

	.container {
		display: flex;
		justify-content: center;
		align-items: center;
		flex: 1;
		color: #cdd6f4;

		.login-form {
			display: flex;
			flex-direction: column;
			gap: 20px;
			width: 320px;

			@media (width <= 320px) {
				& {
					width: 100%;
				}
			}
		}

		.login-header {
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;

			.login-error {
				display: flex;
				gap: 10px;
				width: 100%;
				background: #f38ba8;
				color: #11111b;
				font-size: 14px;
				font-weight: bold;
				padding: 10px;
				border-radius: 10px;
				border: 1px solid #313244;
				box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
				align-items: center;

				.login-error-close {
					display: flex;
					justify-content: center;
					align-items: center;
					background: transparent;
					width: 30px;
					height: 30px;
					margin: 0;
					padding: 0;
					border: none;
					border-radius: 100%;
					cursor: pointer;
					color: #11111b;

					&:hover {
						background-color: #db7d97;
					}
				}
			}
		}

		.login-body {
			display: flex;
			flex: 1;
			flex-direction: column;
			gap: 20px;
		}
	}
</style>
