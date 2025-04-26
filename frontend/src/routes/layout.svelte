<script lang="ts">
	import { onMount } from "svelte";

	let { notes } = $props();

	function masonry() {
		console.log("masonry updated");
		const items: NodeListOf<HTMLElement> = document.querySelectorAll(".note");

		const width = 240;

		const columns = 5;

		const heights = Array(columns).fill(0);

		const gap = 10;
		items.forEach((item, index) => {
			let column = index % columns;
			item.style.transform = `translate(${column * (width + gap)}px, ${heights[column]}px)`;
			item.style.height = item.offsetHeight + "px"; // It is used to set the height in the CSS (by default it is not set when it is auto) so that the transition can be made correctly
			heights[column] += item.offsetHeight + gap;
		});
	}

	onMount(() => {
		masonry();
	});
</script>

<div class="layout">
	{@render notes(masonry)}
	<div class="overlay"></div>
</div>

<style>
	.layout {
		position: relative;
		width: 100%;
		height: 100vh;
		background: #11111b;
		border: none;
		padding: 0;
		margin: 0;
	}

	.overlay {
		position: fixed;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		opacity: 0;
		pointer-events: none;
		transition: all 0.3s ease;
	}
</style>
