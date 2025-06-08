<script lang="ts">
	import { onMount } from "svelte";
	import Note from "$lib/ui/note/Note.svelte";
	import { getNoteState } from "$lib/state/note.svelte";

	let { children } = $props();
	let ontransitionstart: ((event: TransitionEvent) => void) | null = $state(null);
	let ontransitionend: ((event: TransitionEvent) => void) | null = $state(null);

	const notes = $derived(getNoteState().getAll());

	export function masonry() {
		const container = document.getElementById("layout");
		if (!container) return;
		console.log(container.offsetWidth);
		const items: HTMLCollection = container.children;

		const width = 240;

		let columns = 7;

		const heights = Array(columns).fill(0);

		const gap = 10;

		while (columns * width + gap * columns >= container.offsetWidth) {
			columns--;
		}

		for (let i = 0; i < items.length; i++) {
			const column = i % columns;
			const item = items[i] as HTMLElement;
			item.style.top = heights[column] + "px";
			item.style.left = column * (width + gap) + "px";
			heights[column] += item.offsetHeight + gap;
		}
	}

	onMount(() => {
		masonry();
	});

	$effect(() => {
		notes.length;
		console.log("Masonry effect");
		masonry();
	});

	export function waitForTransitions(): Promise<void> {
		return new Promise((resolve) => {
			let activeTransitions = 0;

			ontransitionstart = (event: TransitionEvent) => {
				if (!event.target.classList.contains("note")) return;
				activeTransitions++;
			};

			ontransitionend = (event: TransitionEvent) => {
				if (!event.target.classList.contains("note")) return;
				activeTransitions--;
				if (activeTransitions === 0) {
					ontransitionstart = null;
					ontransitionend = null;
					resolve();
				}
			};
		});
	}

	function onResizeWidth() {
		masonry();
	}
</script>

<svelte:window onresize={masonry} />

<div
	class="layout"
	id="layout"
	{ontransitionstart}
	{ontransitionend}
	bind:clientWidth={null, onResizeWidth}
>
	{@render children()}
</div>

<style>
	.layout {
		position: relative;
		max-width: 1752px;
		flex: 1;
		overflow-y: auto;
	}

	@container content (width < 1700px) {
		.layout {
			max-width: 1502px;
		}
	}
</style>
