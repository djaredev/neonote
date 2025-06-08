<script lang="ts">
	let { class: className = "", children } = $props();
	import { onMount, tick } from "svelte";
	import { getModalContext } from "./modal.svelte";

	const modal = getModalContext();

	function onclick() {
		console.log(modal.modal.localName);
	}
</script>

<div class={className} {onclick} bind:this={modal.preview}>
	{@render children()}
</div>
