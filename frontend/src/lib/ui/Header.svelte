<script lang="ts">
	import { PanelLeftCloseIcon, PanelLeftOpenIcon } from "@lucide/svelte";
	import AppOptions from "./AppOptions.svelte";

	let { isOpen = $bindable(false) } = $props();

	function onclick() {
		isOpen = !isOpen;
	}
</script>

<header>
	<div class="header-left">
		<button {onclick} class="header-action">
			{#if isOpen}
				<PanelLeftCloseIcon color="#cdd6f4" size={30} />
			{:else}
				<PanelLeftOpenIcon color="#cdd6f4" size={30} />
			{/if}
		</button>
	</div>
	<div class="header-center">
		<div class="barsearch"></div>
	</div>
	<div class="header-right">
		<AppOptions />
	</div>
</header>

<style>
	header {
		display: flex;
		width: 100%;
		height: 80px;
		background: inherit;
		justify-content: center;
		align-items: center;
	}

	.barsearch {
		max-width: 600px;
		overflow: hidden;
		color: white;
		background: #11111b;
		border-radius: 8px;
		border: 1px solid #313244;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		height: 54px;
		flex: 1;
	}

	.header-center {
		display: flex;
		flex: 1;
		justify-content: center;
	}

	.header-left {
		display: flex;
		justify-content: center;
		width: 50px;
	}

	.header-right {
		display: flex;
		justify-content: center;
		width: 50px;
	}

	.header-action {
		background: none;
		border: none;
		cursor: pointer;
	}
</style>
