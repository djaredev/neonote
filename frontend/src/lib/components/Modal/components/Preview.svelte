<script lang="ts">
	let { class: className = "", children } = $props();
	import { onMount, tick } from "svelte";
	import { getModalContext } from "./modal.svelte";

	const modal = getModalContext();

	onMount(() => {
		console.log("Preview mounted");
		console.log("From Preview: ");

		// tick().then(() => {
		// 	console.log(modal.modal);
		// });
	});

	function onclick() {
		console.log(modal.modal.localName);
	}
</script>

<div class={className} {onclick} bind:this={modal.preview}>
	{@render children()}
</div>
