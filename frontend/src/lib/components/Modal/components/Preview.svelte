<script lang="ts">
	import { onMount, tick } from "svelte";
	import { getModalContext } from "./modal.svelte";
	let { class: className = "", children } = $props();
	const modal = getModalContext();
</script>

<div class={className} bind:this={modal.preview}>
	{@render children()}
</div>
