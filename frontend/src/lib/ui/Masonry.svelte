<script lang="ts">
	import { onMount } from "svelte";
	import Note from "$lib/ui/note/Note.svelte";
	import { getNoteState } from "$lib/state/note.svelte";
	import handler from "$lib/utils/handler";
	import { createCursor } from "$lib/utils/cursor";
	import { getNotes } from "@neonote/sdk";
	import LazyLoading from "./LazyLoading.svelte";

	let { getData = getNotes, NoteType = Note } = $props();
	let ontransitionstart: ((event: TransitionEvent) => void) | null = $state(null);
	let ontransitionend: ((event: TransitionEvent) => void) | null = $state(null);
	const noteState = getNoteState();
	const MAX_LOAD = 100;
	let count = $state(false);
	let layout: HTMLElement;
	let grid: HTMLElement;

	const masonry = () => {
		const content = document.getElementById("content");
		if (!content) return;
		const items: HTMLCollection = grid.children;

		const width = (items[0] as HTMLElement).offsetWidth;

		let columns = 7;

		const heights = Array(columns).fill(0);

		const gap = 10;

		while (columns * width + gap * columns > content.offsetWidth) {
			columns--;
		}

		if (columns > 1) {
			grid.style.maxWidth = `${columns * width + gap * columns}px`;
		}

		for (let i = 0; i < items.length; i++) {
			const column = i % columns;
			const item = items[i] as HTMLElement;
			item.style.top = heights[column] + "px";
			item.style.left = column * (width + gap) + "px";
			heights[column] += item.offsetHeight + gap;
		}
	};

	const waitForTransitions = (): Promise<void> => {
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
	};

	const onResizeWidth = () => {
		masonry();
	};

	const loadMore = handler(async () => {
		const lastNote = noteState.notes[noteState.notes.length - 1];
		const cursor = createCursor(lastNote.id, lastNote.created_at);
		const data = await getData({
			query: {
				cursor: cursor
			}
		});
		if (data.data && data.data.notes.length > 1) {
			let newLength = noteState.notes.length + data.data.notes.length;
			if (noteState.notes.length + data.data.notes.length > MAX_LOAD) {
				noteState.notes.splice(0, newLength - MAX_LOAD);
				count = true;
				waitForTransitions().then(() => {
					noteState.notes.push(...data.data.notes);
					loadMore.restore();
				});
			} else {
				noteState.notes.push(...data.data.notes);
				loadMore.restore();
			}
		} else {
			loadMore.restore();
		}
	});

	const loadPrevious = handler(async () => {
		const content = document.getElementById("layout");
		if (!content) return;
		const previousScrollHeight = content.scrollHeight;
		const previousScrollTop = content.scrollTop;
		const firstNote = noteState.notes[0];
		const cursor = createCursor(firstNote.id, firstNote.created_at);
		const data = await getData({
			query: {
				cursor: cursor,
				direction: "prev"
			}
		});
		if (data.data && data.data.notes.length > 0) {
			noteState.notes.unshift(...data.data.notes.reverse());
			waitForTransitions().then(() => {
				const newScrollHeight = content.scrollHeight;
				const deltaHeight = newScrollHeight - previousScrollHeight;
				content.scrollTop = previousScrollTop + deltaHeight;
				const currentLength = noteState.notes.length;
				if (currentLength > MAX_LOAD) {
					const gap = currentLength - MAX_LOAD;
					noteState.notes.splice(currentLength - gap, gap);
				}
				loadPrevious.restore();
			});
		} else {
			count = false;
			loadPrevious.restore();
		}
	});

	onMount(() => {
		masonry();
	});

	$effect(() => {
		noteState.notes.length;
		console.log("Masonry effect");
		masonry();
	});
</script>

<svelte:window onresize={masonry} />

<div
	class="layout"
	id="layout"
	{ontransitionstart}
	{ontransitionend}
	bind:clientWidth={null, onResizeWidth}
	bind:this={layout}
>
	{#if count}
		<LazyLoading loadData={loadPrevious.once} />
	{/if}
	<div class="grid" id="grid" bind:this={grid}>
		{#each noteState.notes as note (note.id)}
			<NoteType {masonry} id={note.id} />
		{/each}
		<LazyLoading loadData={loadMore.once} />
	</div>
</div>

<style>
	* {
		box-sizing: border-box;
	}
	.layout {
		display: flex;
		position: relative;
		max-width: 1800px;
		flex: 1;
		justify-content: center;
		overflow-y: auto;
		padding: 10px;
	}

	.grid {
		position: relative;
		width: 100%;
		flex: 1;
	}
</style>
