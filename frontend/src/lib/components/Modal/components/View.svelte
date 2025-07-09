<script lang="ts">
	import { getModalContext } from "./modal.svelte";

	let { class: className = "", children } = $props();

	const modalState = getModalContext();
</script>

{#if modalState.isOpen}
	<div
		class={className}
		bind:this={modalState.view}
		bind:clientHeight={null, modalState.contentHeight}
		ontransitionend={modalState.ontransitionend}
		ontransitionstart={modalState.ontransitionstart}
		ontransitioncancel={modalState.ontransitioncancel}
	>
		{@render children()}
	</div>
{/if}

<style>
	.hidden {
		visibility: hidden;
	}
</style>
