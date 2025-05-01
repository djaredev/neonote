<script lang="ts">
	import { onMount } from "svelte";

	let { notes } = $props();

	function masonry() {
		console.log("masonry updated");
		const items: NodeListOf<HTMLElement> = document.querySelectorAll(".note");

		const width = 240;

		let columns = 7;

		const heights = Array(columns).fill(0);

		const gap = 10;

		while (columns * width + gap * columns + 60 >= window.innerWidth) {
			console.log("Columns: " + columns);
			columns--;
		}

		items.forEach((item, index) => {
			let column = index % columns;
			// item.style.transform = `translate(${column * (width + gap)}px, ${heights[column]}px)`;
			item.style.top = heights[column] + "px";
			item.style.left = column * (width + gap) + "px";
			item.style.height = item.offsetHeight + "px"; // It is used to set the height in the CSS (by default it is not set when it is auto) so that the transition can be made correctly
			heights[column] += item.offsetHeight + gap;
		});
	}

	onMount(() => {
		masonry();
	});
</script>

<svelte:window onresize={masonry} />

<!-- <div class="header"></div> -->
<div class="layout">
	{@render notes(masonry)}
	<div class="overlay"></div>
</div>

<style>
	.header {
		width: 100%;
		height: 100px;
		background: orangered;
	}

	.layout {
		position: relative;
		flex: 1;
		width: 99%;
		height: 100vh;
		background: inherit;
		border: none;
		padding: 0;
		margin: 0;
		overflow-y: visible;
		align-self: center;
	}

	.overlay {
		position: fixed;
		width: 100%;
		height: 100vh;
		background-color: rgba(0, 0, 0, 0.5);
		opacity: 0;
		pointer-events: none;
		transition: all 0.05s ease;
	}
</style>
