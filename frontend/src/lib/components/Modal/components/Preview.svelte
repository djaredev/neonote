<script lang="ts">
	let { class: className = "", children } = $props();
	import { onMount, tick } from "svelte";
	import { getModalContext } from "./modal.svelte";
	const modal = getModalContext();
</script>

<div class={className} bind:this={modal.preview}>
	{@render children()}
</div>
