<script lang="ts">
	import { getModalContext } from "./modal.svelte";

	let { class: className = "", transition } = $props();
	let type = transition.type;
	const modal = getModalContext();
</script>

{#if modal.overlay}
	<div class={className} transition:type={transition.duration}></div>
{/if}
