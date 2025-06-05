<script lang="ts">
	import { onMount } from "svelte";
	let { loadData } = $props();
	let lazyLoading: HTMLElement;

	const observer = new IntersectionObserver(
		(entries) => {
			if (entries[0].isIntersecting) {
				loadData();
			}
		},
		{
			rootMargin: "0px",
			threshold: 1
		}
	);

	onMount(() => {
		observer.observe(lazyLoading);
	});
</script>

<div class="lazy-loading" bind:this={lazyLoading}></div>

<style>
	.lazy-loading {
		position: absolute;
		width: 100px;
		height: 200px;
		visibility: hidden;
	}
</style>
