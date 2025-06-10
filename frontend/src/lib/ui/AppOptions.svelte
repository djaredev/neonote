<script lang="ts">
	import { CircleUserRoundIcon, SettingsIcon, LogOutIcon } from "@lucide/svelte";

	let isOpen = $state(false);
	let dropdown: HTMLElement;

	function onclick() {
		isOpen = !isOpen;
	}

	function onClose(event: MouseEvent) {
		if (dropdown.contains(event.target as Node)) return;
		event.stopPropagation();
		isOpen = false;
	}
</script>

<svelte:window onclick={isOpen ? onClose : null} />

<div class="dropdown" bind:this={dropdown}>
	<button class="dropdown-trigger" {onclick}>
		<CircleUserRoundIcon color="#cdd6f4" size={30} />
	</button>
	<div class={["dropdown-menu", isOpen && "open"]}>
		<div class="dropdown-header">
			<div class="user-name">Admin</div>
			<div class="user-email">admin@example.com</div>
		</div>
		<div class="dropdown-content">
			<button class="dropdown-item">
				<SettingsIcon class="dropdown-icon" />
				<span>Settings</span>
			</button>
			<div class="dropdown-separator"></div>
			<button class="dropdown-item">
				<LogOutIcon class="dropdown-icon" />
				<span>Logout</span>
			</button>
		</div>
	</div>
</div>

<style>
	* {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
	}

	.dropdown {
		position: relative;
		display: inline-block;
		background: #11111b;
		color: #cdd6f4;
	}

	.dropdown-trigger {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 50px;
		height: 50px;
		background: none;
		border: none;
		cursor: pointer;
	}

	.dropdown-trigger:hover {
		border-radius: 10px;
		background: #1e1e2e;
	}

	.dropdown-menu {
		position: absolute;
		top: calc(100% + 4px);
		right: 0;
		min-width: 200px;
		background: inherit;
		border-radius: 8px;
		border: 1px solid #313244;
		box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
		z-index: 1000;
		opacity: 0;
		visibility: hidden;
		transform: translateY(-8px);
		transition: all 0.2s ease;
	}

	.open {
		opacity: 1;
		visibility: visible;
		transform: translateY(0);
	}

	.dropdown-content {
		padding: 0.5rem 10px;
	}

	.dropdown-item {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.625rem 1rem;
		color: inherit;
		/* text-decoration: none; */
		font-size: 0.875rem;
		cursor: pointer;
		transition: all 0.15s ease;
		border: none;
		border-radius: 8px;
		background: inherit;
		width: 100%;
		text-align: left;
	}

	.dropdown-item:hover {
		background-color: #1e1e2e;
	}

	.dropdown-separator {
		height: 1px;
		background-color: #313244;
		margin: 0.5rem 0;
	}

	.dropdown-header {
		padding: 0.75rem 1rem;
		border-bottom: 1px solid #313244;
	}

	.dropdown-header .user-name {
		font-weight: 500;
		color: inherit;
		font-size: 0.875rem;
		font-weight: bold;
	}

	.dropdown-header .user-email {
		color: inherit;
		font-size: 0.75rem;
		margin-top: 0.25rem;
	}

	:global(.dropdown-icon) {
		width: 20px;
		height: 20px;
		color: #cdd6f4;
	}
</style>
