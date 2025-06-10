<script lang="ts">
	import { UserCogIcon, WallpaperIcon, Fingerprint } from "@lucide/svelte";

	let { children } = $props();
</script>

<main class="settings">
	<div class="title">
		<h1>Settings</h1>
	</div>
	<div class="settings-content">
		<div class="settings-options">
			<a href="/settings/account" class="settings-option" title="account">
				<UserCogIcon color="#cdd6f4" />
				<span class="option-label">Account</span>
			</a>
			<a href="" class="settings-option" title="apparance">
				<WallpaperIcon color="#cdd6f4" />
				<span class="option-label">Apparance</span>
			</a>
			<a href="/settings/security" class="settings-option" title="security">
				<Fingerprint color="#cdd6f4" />
				<span class="option-label">Security</span>
			</a>
		</div>
		<div class="settings-view">
			{@render children()}
		</div>
	</div>
</main>

<style>
	* {
		box-sizing: border-box;
	}

	.settings {
		display: flex;
		flex-direction: column;
		max-width: 1000px;
		flex: 1;
		background: inherit;

		.title {
			color: #cdd6f4;
			padding: 10px 20px;

			& h1 {
				margin: 0px;
				padding: 0px;
			}
		}

		.settings-content {
			display: flex;
			gap: 50px;
			/* max-width: 1000px; */
			flex: 1;
			background: inherit;

			.settings-options {
				display: flex;
				flex-direction: column;
				gap: 4px;
				padding: 10px;
				width: 220px;
				background: inherit;

				.settings-option {
					color: #cdd6f4;
					display: flex;
					text-decoration: none;
					width: 100%;
					min-width: fit-content;
					block-size: 50px;
					align-items: center;
					gap: 20px;
					outline: 2px solid transparent;
					border-radius: 10px;
					padding: 10px;
					overflow: hidden;

					&:hover {
						background-color: #1e1e2e;
						color: #cdd6f4;
					}

					.option-label {
						white-space: nowrap;
						overflow: hidden;
						transition: opacity 0.3s ease;
					}
				}
			}

			@container content ( width < 750px ) {
				.settings-options {
					flex-direction: row;
					width: 100%;
					height: 80px;
					overflow-x: scroll;
					align-items: center;
				}
			}

			.settings-view {
				display: flex;
				flex-direction: column;
				flex: 1;
				background: inherit;
				padding: 10px;
			}
		}

		@container content ( width < 750px ) {
			& {
				width: 100%;
			}

			.settings-content {
				flex-direction: column;
				width: 100%;
			}
		}
	}
</style>
